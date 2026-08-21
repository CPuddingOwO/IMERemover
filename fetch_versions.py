#!/usr/bin/env python3
"""查询指定 Minecraft 版本所需的 Fabric / NeoForge 依赖版本,并可写入 versions.json。

用法:
    python fetch_versions.py -v 26.2              # 仅打印
    python fetch_versions.py -v 26.2 -i           # 打印并插入/更新 versions.json

数据来源:
    - Fabric Loader: https://meta.fabricmc.net
    - Fabric API:    https://maven.fabricmc.net
    - NeoForge:      https://maven.neoforged.net
    - NeoForm:       https://maven.neoforged.net
"""

import argparse
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET

FABRIC_META_LOADER = "https://meta.fabricmc.net/v2/versions/loader/{mc}"
FABRIC_META_ALL_LOADERS = "https://meta.fabricmc.net/v2/versions/loader"
FABRIC_API_MAVEN = "https://maven.fabricmc.net/net/fabricmc/fabric-api/fabric-api/maven-metadata.xml"
NEOFORGE_MAVEN = "https://maven.neoforged.net/releases/net/neoforged/neoforge/maven-metadata.xml"
NEOFORM_MAVEN = "https://maven.neoforged.net/releases/net/neoforged/neoform/maven-metadata.xml"


def fetch(url):
    with urllib.request.urlopen(url, timeout=30) as resp:
        return resp.read().decode("utf-8")


def fetch_json(url):
    return json.loads(fetch(url))


def fetch_maven_versions(maven_url):
    root = ET.fromstring(fetch(maven_url))
    return [v.text for v in root.iter("version")]


def get_fabric_loader(mc):
    try:
        data = fetch_json(FABRIC_META_LOADER.format(mc=mc))
        loaders = [e["loader"]["version"] for e in data if e.get("loader", {}).get("stable")]
        if loaders:
            return loaders[0]
    except Exception:
        pass
    data = fetch_json(FABRIC_META_ALL_LOADERS)
    for entry in data:
        if entry.get("stable"):
            return entry["version"]
    raise RuntimeError(f"无法获取 Minecraft {mc} 的 Fabric Loader 版本")


def get_fabric_api(mc):
    versions = fetch_maven_versions(FABRIC_API_MAVEN)
    matches = [
        v for v in versions
        if v.endswith("+" + mc) and "beta" not in v and "alpha" not in v
    ]
    if not matches:
        raise RuntimeError(f"未找到匹配 Minecraft {mc} 的 Fabric API 版本(快照版本通常没有对应的 Fabric API)")
    def numeric_key(v):
        return [int(x) for x in v.split("+")[0].split(".") if x.isdigit()]
    return sorted(matches, key=numeric_key)[-1]


def get_neoforge(mc):
    versions = fetch_maven_versions(NEOFORGE_MAVEN)
    parts = mc.split(".")
    prefix = ".".join(parts + (["0"] if len(parts) == 2 else [])) + "."
    stable = [v for v in versions if v.startswith(prefix) and "-beta" not in v
              and "-alpha" not in v and "snapshot" not in v and "craftmine" not in v]
    if not stable:
        stable = [v for v in versions if v.startswith(prefix)]
    if not stable:
        raise RuntimeError(f"未找到匹配 Minecraft {mc} 的 NeoForge 版本")
    def numeric_key(v):
        return [int(x) for x in re.split(r"[-+]", v)[0].split(".") if x.isdigit()]
    return sorted(stable, key=numeric_key)[-1]


def get_neoform(mc):
    versions = fetch_maven_versions(NEOFORM_MAVEN)
    matches = [v for v in versions if v.startswith(mc + "-") and not v.endswith("-SNAPSHOT")]
    if not matches:
        raise RuntimeError(f"未找到匹配 Minecraft {mc} 的 NeoForm 版本")
    return matches[-1]


def load_versions_file(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"versions": []}


def save_versions_file(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def main():
    parser = argparse.ArgumentParser(
        description="查询指定 Minecraft 版本所需的 Fabric / NeoForge 依赖版本")
    parser.add_argument("-v", "--version", "--Version", dest="mc", required=True,
                        help="Minecraft 版本,例如 26.2")
    parser.add_argument("-i", "--insert", "--Insert", action="store_true",
                        help="将结果插入到 versions.json(已存在则更新,否则追加)")
    parser.add_argument("--file", default="versions.json",
                        help="versions.json 路径(默认 versions.json)")
    args = parser.parse_args()

    mc = args.mc
    deps = {
        "minecraft": mc,
        "fabric_loader": get_fabric_loader(mc),
        "fabric_api": get_fabric_api(mc),
        "neoforge": get_neoforge(mc),
        "neoform": get_neoform(mc),
    }

    print(json.dumps(deps, ensure_ascii=False, indent=2))

    if args.insert:
        data = load_versions_file(args.file)
        versions = data["versions"]
        for i, entry in enumerate(versions):
            if entry["minecraft"] == mc:
                versions[i] = deps
                break
        else:
            versions.append(deps)
        save_versions_file(args.file, data)
        print(f"已写入 {args.file}")


if __name__ == "__main__":
    main()