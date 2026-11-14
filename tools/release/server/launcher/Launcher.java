package campfiremons;

import java.io.IOException;
import java.io.InputStream;
import java.lang.instrument.Instrumentation;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;
import java.security.MessageDigest;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HexFormat;
import java.util.List;
import java.util.Properties;
import java.util.jar.JarFile;

/**
 * Campfiremons server launcher: the one jar a host starts (`java -Xmx10G -jar campfiremons-server.jar`). On every start it
 *
 * <ol>
 *   <li>installs the NeoForge server, once per version (checksum-verified),
 *   <li>syncs mods and configs from the pack's release branch (packwiz-installer, server-side files only),
 *   <li>starts NeoForge in this same JVM through NeoForged's ServerStarterJar, so the host's memory and JVM flags apply to
 *       the server itself.
 * </ol>
 *
 * <p>The pack URL can be overridden with {@code -Dcampfiremons.packUrl=...} or the PACK_URL environment variable, and
 * {@code --sync-only} stops after step 2. Built by tools/release/build.py; see DEVELOPMENT.md "Running the server".
 */
public final class Launcher {
    private static final String STARTER_AGENT = "net.neoforged.serverstarterjar.Agent";
    private static final String STARTER_MAIN = "net.neoforged.serverstarterjar.Main8";
    private static final HttpClient HTTP = HttpClient.newBuilder().followRedirects(HttpClient.Redirect.NORMAL).build();

    private static Instrumentation instrumentation;

    /** Launcher-Agent-Class: the JVM calls this before main when the jar is started with -jar. */
    public static void agentmain(String args, Instrumentation inst) {
        instrumentation = inst;
    }

    public static void premain(String args, Instrumentation inst) {
        agentmain(args, inst);
    }

    public static void main(String[] args) throws Throwable {
        Properties config = new Properties();
        try (InputStream in = Launcher.class.getResourceAsStream("/campfiremons/launcher.properties")) {
            config.load(in);
        }
        List<String> serverArgs = new ArrayList<>(Arrays.asList(args));
        boolean syncOnly = serverArgs.remove("--sync-only");
        Path dir = Path.of("").toAbsolutePath();

        installNeoForge(dir, config.getProperty("neoforge.version"), config.getProperty("neoforge.sha256"));
        sync(dir, config);
        if (syncOnly) {
            return;
        }
        if (!serverArgs.contains("nogui")) {
            serverArgs.add("nogui");
        }
        launch(dir, config.getProperty("serverstarter.version"), serverArgs.toArray(new String[0]));
    }

    private static void installNeoForge(Path dir, String version, String sha256) throws Exception {
        if (Files.exists(dir.resolve("libraries/net/neoforged/neoforge/" + version + "/unix_args.txt"))) {
            return;
        }
        log("Installing the NeoForge " + version + " server");
        String name = "neoforge-" + version + "-installer.jar";
        Path installer = dir.resolve(name);
        download("https://maven.neoforged.net/releases/net/neoforged/neoforge/" + version + "/" + name, sha256, installer);
        run(dir, "-Xmx1G", "-jar", name, "--installServer");
        Files.deleteIfExists(installer);
        Files.deleteIfExists(dir.resolve(name + ".log"));
    }

    private static void sync(Path dir, Properties config) throws Exception {
        String packUrl = firstSet(System.getProperty("campfiremons.packUrl"), System.getenv("PACK_URL"),
                config.getProperty("pack.url"));
        Path bootstrap = dir.resolve("packwiz-installer-bootstrap.jar");
        if (!Files.exists(bootstrap)) {
            download(config.getProperty("bootstrap.url"), config.getProperty("bootstrap.sha256"), bootstrap);
        }
        log("Syncing the pack from " + packUrl);
        try {
            run(dir, "-Xmx1G", "-jar", bootstrap.getFileName().toString(), "-g", "-s", "server", packUrl);
        } catch (IOException e) {
            if (!Files.exists(dir.resolve("packwiz.json"))) {
                throw e;
            }
            log("Sync failed (" + e.getMessage() + "); starting with the files from the last sync");
        }
    }

    /** Hands over to ServerStarterJar, which reads NeoForge's run.sh and args files and starts it in this JVM. */
    private static void launch(Path dir, String starterVersion, String[] serverArgs) throws Throwable {
        if (instrumentation == null) {
            throw new IllegalStateException("start the launcher with `java -jar campfiremons-server.jar`");
        }
        Path starter = dir.resolve(".campfiremons/serverstarter-" + starterVersion + ".jar");
        Files.createDirectories(starter.getParent());
        try (InputStream in = Launcher.class.getResourceAsStream("/campfiremons/serverstarter.jar")) {
            Files.copy(in, starter, StandardCopyOption.REPLACE_EXISTING);
        }
        instrumentation.appendToSystemClassLoaderSearch(new JarFile(starter.toFile()));
        ClassLoader loader = ClassLoader.getSystemClassLoader();

        Method agent = Class.forName(STARTER_AGENT, true, loader).getDeclaredMethod("agentmain", String.class,
                Instrumentation.class);
        agent.setAccessible(true);
        agent.invoke(null, "", instrumentation);

        log("Starting the server");
        try {
            Class.forName(STARTER_MAIN, true, loader).getMethod("main", String[].class).invoke(null, (Object) serverArgs);
        } catch (InvocationTargetException e) {
            throw e.getCause();
        }
    }

    /** Runs a short-lived Java tool (installer, packwiz) in a child JVM with its own small heap. */
    private static void run(Path dir, String... args) throws IOException, InterruptedException {
        String exe = System.getProperty("os.name").startsWith("Windows") ? "java.exe" : "java";
        List<String> command = new ArrayList<>();
        command.add(Path.of(System.getProperty("java.home"), "bin", exe).toString());
        command.addAll(Arrays.asList(args));
        Process process = new ProcessBuilder(command).directory(dir.toFile())
                .redirectOutput(ProcessBuilder.Redirect.INHERIT).redirectError(ProcessBuilder.Redirect.INHERIT).start();
        process.getOutputStream().close(); // the console belongs to the server, not to these tools
        int code = process.waitFor();
        if (code != 0) {
            throw new IOException(args[args.length > 2 ? 2 : 0] + " exited with code " + code);
        }
    }

    private static void download(String url, String sha256, Path target) throws Exception {
        HttpResponse<byte[]> response = HTTP.send(HttpRequest.newBuilder(URI.create(url)).build(),
                HttpResponse.BodyHandlers.ofByteArray());
        if (response.statusCode() != 200) {
            throw new IOException(url + " returned HTTP " + response.statusCode());
        }
        String actual = HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(response.body()));
        if (!actual.equals(sha256)) {
            throw new IOException(url + " doesn't match its pinned sha256 (got " + actual + ")");
        }
        Files.write(target, response.body());
    }

    private static String firstSet(String... values) {
        for (String value : values) {
            if (value != null && !value.isBlank()) {
                return value;
            }
        }
        throw new IllegalStateException("no pack URL configured");
    }

    private static void log(String message) {
        System.out.println("[campfiremons] " + message);
        System.out.flush();
    }

    private Launcher() {
    }
}
