package campfiremons;

import com.simibubi.create.content.kinetics.crusher.CrushingWheelBlock;
import com.simibubi.create.content.kinetics.crusher.CrushingWheelBlockEntity;

import net.minecraft.world.level.block.entity.BlockEntityType;

/** Create's crushing wheel with our own block entity type (so it gets its own model when it spins). */
public class DiamondTippedCrushingWheelBlock extends CrushingWheelBlock {
    public DiamondTippedCrushingWheelBlock(Properties properties) {
        super(properties);
    }

    @Override
    public BlockEntityType<? extends CrushingWheelBlockEntity> getBlockEntityType() {
        return Campfiremons.DIAMOND_TIPPED_CRUSHING_WHEEL_BE.get();
    }
}
