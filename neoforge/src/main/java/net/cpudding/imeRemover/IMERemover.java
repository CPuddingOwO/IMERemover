package net.cpudding.imeRemover;

import net.neoforged.fml.common.Mod;

@Mod(Constants.MOD_ID)
public class IMERemover {

    // 由 NeoForge 加载器在模组加载时调用
    public IMERemover() {
        Constants.LOG.info("IMERemover 已加载 (NeoForge)");
    }
}