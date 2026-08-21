# IME Remover

去除来自 `Minecraft 26.1-snapshot-8` 添加的 `游戏内输入法` 的 `自动切换中英文` 部分

也就是只会加载该Mod后 游戏内不会再自动切换输入法中英文状态了

## Install

* 直接下载 [Release](https://github.com/CPuddingOwO/IMERemover/releases) 

* 从Github仓库编译 参考 [Build](https://github.com/CPuddingOwO/IMERemover#Build) 章节

## Build

* 先Clone仓库

```bash
git clone https://github.com/CPuddingOwO/IMERemover.git
cd IMERemover
```
* 确定自己要编译Minecraft版本

使用 `fetch_versions.py` 获取对应Minecraft版本的Fabric+Neoforge相关最新版本号

```bash
python fetch_versions.py -v 26.2 
# -v <Minecraft版本>
# -i 插入 versions.json 用于CI构建
```

* 将对应的版本号填入项目根目录的 `gradle.properties` 

`minecraft` -> `minecraft_version`  
`fabric_loader` -> `fabric_loader_version`  
`fabric_api` -> `fabric_version`  
`neoforge` -> `neoforge_version`  
`nroform` -> `neo_form_version`  

* 运行编译命令  

```bash
./gradlew build
```

构建产物会出现在各自的 `build/libs` 中

`fabric` -> `fabric/build/libs`  
`neoforge` -> `neoforge/build/libs`




