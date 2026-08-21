package net.cpudding.imeRemover.mixin;

import com.mojang.blaze3d.platform.TextInputManager;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

// 阻止 Minecraft 自动切换系统 IME 语言(26.1-snapshot-8 起引入)。
// 取消 tick() 与 setIMEInputMode(boolean) 后,游戏不再通过
// glfwSetInputMode(handle, GLFW_IME, ...) 启用/禁用 GLFW IME,
// 输入法保持系统默认状态,避免中文用户被锁在英文输入模式。
@Mixin(TextInputManager.class)
public class MixinTextInputManager {

    @Inject(method = "tick()V", at = @At("HEAD"), cancellable = true)
    private void imer$cancelTick(CallbackInfo ci) {
        ci.cancel();
    }

    @Inject(method = "setIMEInputMode(Z)V", at = @At("HEAD"), cancellable = true)
    private void imer$cancelSetIMEInputMode(boolean value, CallbackInfo ci) {
        ci.cancel();
    }
}