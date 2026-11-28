package campfiremons.mixin;

import java.util.List;

import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;

import com.llamalad7.mixinextras.injector.wrapoperation.Operation;
import com.llamalad7.mixinextras.injector.wrapoperation.WrapOperation;
import com.simibubi.create.content.kinetics.crusher.CrushingWheelControllerBlockEntity;
import com.simibubi.create.content.processing.recipe.StandardProcessingRecipe;

import campfiremons.DiamondCrushing;
import net.minecraft.util.RandomSource;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.entity.BlockEntity;

/** The crushing itself: faster processing and better odds when both wheels are diamond-tipped. */
@Mixin(CrushingWheelControllerBlockEntity.class)
abstract class CrushingWheelControllerBlockEntityMixin {
    // tick() works out this tick's progress as Mth.clamp(speed / log2(stack size), .25, 20); it is the only
    // Mth.clamp in tick().
    @WrapOperation(method = "tick", at = @At(value = "INVOKE", target = "Lnet/minecraft/util/Mth;clamp(FFF)F"))
    private float campfiremons$diamondSpeed(float value, float min, float max, Operation<Float> original) {
        float progress = original.call(value, min, max);
        BlockEntity self = (BlockEntity) (Object) this;
        return DiamondCrushing.isDiamondPair(self.getLevel(), self.getBlockPos())
            ? progress * DiamondCrushing.SPEED_MULTIPLIER : progress;
    }

    // applyRecipe() rolls the recipe once per item in the stack.
    @WrapOperation(method = "applyRecipe", at = @At(value = "INVOKE",
        target = "Lcom/simibubi/create/content/processing/recipe/StandardProcessingRecipe;rollResults(Lnet/minecraft/util/RandomSource;)Ljava/util/List;"))
    private List<ItemStack> campfiremons$diamondOdds(StandardProcessingRecipe<?> recipe, RandomSource random,
        Operation<List<ItemStack>> original) {
        BlockEntity self = (BlockEntity) (Object) this;
        if (!DiamondCrushing.isDiamondPair(self.getLevel(), self.getBlockPos()))
            return original.call(recipe, random);
        return recipe.rollResults(DiamondCrushing.boost(recipe.getRollableResults()), random);
    }
}
