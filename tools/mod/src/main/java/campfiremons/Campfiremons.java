package campfiremons;

import com.simibubi.create.AllCreativeModeTabs;
import com.simibubi.create.api.stress.BlockStressValues;
import com.simibubi.create.content.kinetics.crusher.CrushingWheelBlockEntity;
import com.simibubi.create.content.processing.sequenced.SequencedAssemblyItem;

import net.minecraft.core.registries.Registries;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.material.MapColor;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.neoforged.fml.event.lifecycle.FMLCommonSetupEvent;
import net.neoforged.neoforge.event.BuildCreativeModeTabContentsEvent;
import net.neoforged.neoforge.registries.DeferredBlock;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredItem;
import net.neoforged.neoforge.registries.DeferredRegister;

/**
 * The Campfiremons pack's own content. So far: Diamond-Tipped Crushing Wheels, a Create crushing wheel that, when
 * both wheels of a pair are diamond-tipped, crushes faster and makes chance outputs more likely (see
 * {@link DiamondCrushing}).
 */
@Mod(Campfiremons.MODID)
public final class Campfiremons {
    public static final String MODID = "campfiremons";

    /** Stress per RPM. Create's crushing wheel is 8. */
    public static final double DIAMOND_WHEEL_STRESS = 12.0;

    private static final DeferredRegister.Blocks BLOCKS = DeferredRegister.createBlocks(MODID);
    private static final DeferredRegister.Items ITEMS = DeferredRegister.createItems(MODID);
    private static final DeferredRegister<BlockEntityType<?>> BLOCK_ENTITY_TYPES =
        DeferredRegister.create(Registries.BLOCK_ENTITY_TYPE, MODID);

    // Create's wheel copies andesite's properties (SharedProperties.stone).
    public static final DeferredBlock<DiamondTippedCrushingWheelBlock> DIAMOND_TIPPED_CRUSHING_WHEEL =
        BLOCKS.register("diamond_tipped_crushing_wheel", () -> new DiamondTippedCrushingWheelBlock(
            BlockBehaviour.Properties.ofFullCopy(Blocks.ANDESITE).mapColor(MapColor.DIAMOND).noOcclusion()));

    public static final DeferredItem<BlockItem> DIAMOND_TIPPED_CRUSHING_WHEEL_ITEM =
        ITEMS.registerSimpleBlockItem(DIAMOND_TIPPED_CRUSHING_WHEEL);

    public static final DeferredItem<SequencedAssemblyItem> INCOMPLETE_DIAMOND_TIPPED_CRUSHING_WHEEL =
        ITEMS.register("incomplete_diamond_tipped_crushing_wheel",
            () -> new SequencedAssemblyItem(new Item.Properties()));

    // Create's own block entity class, so everything in Create that looks for a CrushingWheelBlockEntity finds it.
    public static final DeferredHolder<BlockEntityType<?>, BlockEntityType<CrushingWheelBlockEntity>> DIAMOND_TIPPED_CRUSHING_WHEEL_BE =
        BLOCK_ENTITY_TYPES.register("diamond_tipped_crushing_wheel", () -> BlockEntityType.Builder.of(
            (pos, state) -> new CrushingWheelBlockEntity(Campfiremons.DIAMOND_TIPPED_CRUSHING_WHEEL_BE.get(), pos, state),
            Campfiremons.DIAMOND_TIPPED_CRUSHING_WHEEL.get()).build(null));

    public Campfiremons(IEventBus modBus) {
        BLOCKS.register(modBus);
        ITEMS.register(modBus);
        BLOCK_ENTITY_TYPES.register(modBus);
        modBus.addListener(Campfiremons::commonSetup);
        modBus.addListener(Campfiremons::addToCreativeTab);
    }

    private static void commonSetup(FMLCommonSetupEvent event) {
        event.enqueueWork(() -> BlockStressValues.IMPACTS.register(DIAMOND_TIPPED_CRUSHING_WHEEL.get(),
            () -> DIAMOND_WHEEL_STRESS));
    }

    private static void addToCreativeTab(BuildCreativeModeTabContentsEvent event) {
        if (event.getTabKey() == AllCreativeModeTabs.BASE_CREATIVE_TAB.getKey())
            event.accept(DIAMOND_TIPPED_CRUSHING_WHEEL_ITEM.get());
    }
}
