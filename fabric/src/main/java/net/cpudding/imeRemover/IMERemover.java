package net.cpudding.imeRemover;

import net.fabricmc.api.ModInitializer;

public class IMERemover implements ModInitializer {

    // 由 Fabric 加载器在模组加载时调用
    @Override
    public void onInitialize() {
        Constants.LOG.info("IMERemover loaded.");
    }
}