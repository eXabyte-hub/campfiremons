package campfiremons.mixin;

import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;

import com.llamalad7.mixinextras.injector.wrapoperation.Operation;
import com.llamalad7.mixinextras.injector.wrapoperation.WrapOperation;
import com.simibubi.create.AllBlocks;
import com.simibubi.create.content.kinetics.crusher.CrushingWheelBlock;
import com.tterrag.registrate.util.entry.BlockEntry;

import campfiremons.DiamondCrushing;
import net.minecraft.world.level.block.state.BlockState;

/**
 * Create pairs two wheels (updateControllers) and checks neighbouring wheels (canSurvive) with
 * {@code AllBlocks.CRUSHING_WHEEL.has(state)}. Count our wheel too, so any two wheels pair.
 */
@Mixin(CrushingWheelBlock.class)
abstract class CrushingWheelBlockMixin {
    @WrapOperation(method = {"updateControllers", "canSurvive"}, at = @At(value = "INVOKE",
        target = "Lcom/tterrag/registrate/util/entry/BlockEntry;has(Lnet/minecraft/world/level/block/state/BlockState;)Z"))
    private boolean campfiremons$anyCrushingWheel(BlockEntry<?> entry, BlockState state, Operation<Boolean> original) {
        return entry == AllBlocks.CRUSHING_WHEEL ? DiamondCrushing.isWheel(state) : original.call(entry, state);
    }
}
