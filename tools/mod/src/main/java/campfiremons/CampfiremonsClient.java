package campfiremons;

import com.simibubi.create.content.kinetics.base.KineticBlockEntityRenderer;
import com.simibubi.create.content.kinetics.base.SingleAxisRotatingVisual;
import com.simibubi.create.content.kinetics.crusher.CrushingWheelBlockEntity;
import com.simibubi.create.foundation.item.ItemDescription;
import com.simibubi.create.foundation.item.KineticStats;
import com.simibubi.create.foundation.item.TooltipModifier;

import dev.engine_room.flywheel.lib.model.baked.PartialModel;
import dev.engine_room.flywheel.lib.visualization.SimpleBlockEntityVisualizer;
import net.createmod.catnip.lang.FontHelper;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.Item;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.neoforged.fml.event.lifecycle.FMLClientSetupEvent;
import net.neoforged.neoforge.client.event.EntityRenderersEvent;

/** Rendering and tooltips, set up the way Create sets up its own crushing wheel. */
@Mod(value = Campfiremons.MODID, dist = Dist.CLIENT)
public final class CampfiremonsClient {
    // Must exist before models load, so it is created when this class loads (mod construction).
    static final PartialModel DIAMOND_WHEEL = PartialModel.of(
        ResourceLocation.fromNamespaceAndPath(Campfiremons.MODID, "block/diamond_tipped_crushing_wheel/block"));

    public CampfiremonsClient(IEventBus modBus) {
        modBus.addListener(CampfiremonsClient::clientSetup);
        modBus.addListener(CampfiremonsClient::registerRenderers);
    }

    private static void clientSetup(FMLClientSetupEvent event) {
        SimpleBlockEntityVisualizer.builder(Campfiremons.DIAMOND_TIPPED_CRUSHING_WHEEL_BE.get())
            .factory(SingleAxisRotatingVisual.<CrushingWheelBlockEntity>of(DIAMOND_WHEEL))
            .skipVanillaRender(be -> true)
            .apply();
        event.enqueueWork(() -> {
            Item item = Campfiremons.DIAMOND_TIPPED_CRUSHING_WHEEL_ITEM.get();
            TooltipModifier.REGISTRY.register(item,
                new ItemDescription.Modifier(item, FontHelper.Palette.STANDARD_CREATE)
                    .andThen(TooltipModifier.mapNull(KineticStats.create(item))));
        });
    }

    private static void registerRenderers(EntityRenderersEvent.RegisterRenderers event) {
        // Used when Flywheel's visuals are off.
        event.registerBlockEntityRenderer(Campfiremons.DIAMOND_TIPPED_CRUSHING_WHEEL_BE.get(),
            KineticBlockEntityRenderer::new);
    }
}
