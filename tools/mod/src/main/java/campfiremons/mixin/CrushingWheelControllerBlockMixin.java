package campfiremons.mixin;

import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;

import com.llamalad7.mixinextras.injector.wrapoperation.Operation;
import com.llamalad7.mixinextras.injector.wrapoperation.WrapOperation;
import com.simibubi.create.AllBlocks;
import com.simibubi.create.content.kinetics.crusher.CrushingWheelControllerBlock;
import com.tterrag.registrate.util.entry.BlockEntry;

import campfiremons.DiamondCrushing;
import net.minecraft.world.level.block.state.BlockState;

/**
 * The crushing space between two wheels takes its speed from a neighbouring {@code AllBlocks.CRUSHING_WHEEL}
 * (in the lambda inside updateSpeed). Let our wheel drive it too.
 */
@Mixin(CrushingWheelControllerBlock.class)
abstract class CrushingWheelControllerBlockMixin {
    // Create 6.0.10 compiles the updateSpeed lambda to lambda$updateSpeed$1 (checked with javap).
    @WrapOperation(method = "lambda$updateSpeed$1", at = @At(value = "INVOKE",
        target = "Lcom/tterrag/registrate/util/entry/BlockEntry;has(Lnet/minecraft/world/level/block/state/BlockState;)Z"))
    private static boolean campfiremons$anyCrushingWheel(BlockEntry<?> entry, BlockState state,
        Operation<Boolean> original) {
        return entry == AllBlocks.CRUSHING_WHEEL ? DiamondCrushing.isWheel(state) : original.call(entry, state);
    }
}
