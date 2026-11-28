package campfiremons;

import java.util.ArrayList;
import java.util.List;

import com.simibubi.create.AllBlocks;
import com.simibubi.create.content.processing.recipe.ProcessingOutput;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;

/**
 * What a pair of Diamond-Tipped Crushing Wheels does differently. A pair with one normal wheel works like a
 * normal pair.
 */
public final class DiamondCrushing {
    /** Added to every output that has a chance (0.75 becomes 1.0, 0.25 becomes 0.5). */
    public static final float CHANCE_BONUS = 0.25f;
    /** Processing speed at the same RPM. Create caps a normal pair at 20 per tick; this pair reaches 30. */
    public static final float SPEED_MULTIPLIER = 1.5f;

    private DiamondCrushing() {
    }

    /** Stands in for Create's "is this a crushing wheel" check, so either wheel pairs with either. */
    public static boolean isWheel(BlockState state) {
        return state.is(AllBlocks.CRUSHING_WHEEL.get()) || state.is(Campfiremons.DIAMOND_TIPPED_CRUSHING_WHEEL.get());
    }

    /** True when every wheel driving the crushing space at {@code controllerPos} is diamond-tipped. */
    public static boolean isDiamondPair(Level level, BlockPos controllerPos) {
        if (level == null)
            return false;
        int wheels = 0;
        for (Direction side : Direction.values()) {
            BlockState state = level.getBlockState(controllerPos.relative(side));
            // Same test as Create's controller: a wheel whose axle points at the controller doesn't drive it.
            if (!isWheel(state) || state.getValue(BlockStateProperties.AXIS) == side.getAxis())
                continue;
            if (!state.is(Campfiremons.DIAMOND_TIPPED_CRUSHING_WHEEL.get()))
                return false;
            wheels++;
        }
        return wheels >= 2;
    }

    public static List<ProcessingOutput> boost(List<ProcessingOutput> outputs) {
        List<ProcessingOutput> boosted = new ArrayList<>(outputs.size());
        for (ProcessingOutput output : outputs) {
            float chance = output.getChance();
            boosted.add(chance >= 1f ? output
                : new ProcessingOutput(output.getStack(), Math.min(1f, chance + CHANCE_BONUS)));
        }
        return boosted;
    }
}
