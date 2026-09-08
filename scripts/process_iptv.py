#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
处理 IPTV 组播源：
- 从固定远程 URL 下载原始 zubo.txt
- 按照题目要求进行分组去重 & 频道格式转换
- 把结果写入仓库根目录的 JXZB.txt
"""

import sys
import os
import requests

# ----------------- 配置区 -----------------
# 你给定的原始文件地址（可随时修改）
SOURCE_URL = (
    "https://raw.githubusercontent.com/Wind5170/IPTV/"
    "c9871285ca010815afdc807879d66752cfc0b59d/output/zubo_all.txt"
)
OUTPUT_FILE = "JXZB.txt"  # 相对于仓库根目录
# ----------------------------------------


def fetch_remote_content(url: str) -> str:
    """下载远程文件并返回解码后的文本内容"""
    try:
        print(f"⬇️  正在下载远程文件：{url}")
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        # 自动检测编码，避免乱码（国内 IPTV 常见 gbk）
        encoding = resp.apparent_encoding or "utf-8"
        content = resp.content.decode(encoding)
        print("✅ 远程文件下载成功")
        return content
    except requests.RequestException as e:
        print(f"❌ 下载远程文件失败：{e}")
        sys.exit(1)


def process_iptv_content(content: str) -> list[str]:
    """核心处理逻辑：分组去重 + 频道格式转换"""
    lines = content.splitlines()
    out: list[str] = []

    current_group: str | None = None          # 当前频道所属的原始完整分组名
    seen_provinces: set[str] = set()          # 已输出过的省份前缀（用于 genre 行去重）

    for raw in lines:
        line = raw.strip()
        if not line:
            continue  # 跳过空行

        # ---------- 分组行（含 #genre#） ----------
        if "#genre#" in line:
            # 原始分组名 = 第个逗号前的全部
            original_group = line.split(",#genre#")[0].strip()
            # 省份标识 = 前两个字（不足两位则取全部）
            province = original_group[:2] if len(original_group) >= 2 else original_group

            # 同省份只保留第一个分组行
            if province not in seen_provinces:
                new_genre = f"{province}组播,#genre#"
                out.append(new_genre)
                seen_provinces.add(province)

            # 即使本行被去重，也要把当前分组映射更新为原始全名，
            # 这样后续的频道才能正确归属到该分组
            current_group = original_group
            continue

        # ---------- 频道行 ----------
        if not current_group:
            print(f"⚠️  警告：发现无分组的频道行，已跳过：{line}")
            continue
        if "," not in line:
            print(f"⚠️  警告：格式错误的频道行，已跳过：{line}")
            continue

        # 只在第一个逗号处切分，防止 URL 本身包含逗号
        channel_name, url = line.split(",", 1)
        new_line = f"{channel_name},{url}${current_group}"
        out.append(new_line)

    return out


def main() -> None:
    # 1. 下载原始内容
    raw_content = fetch_remote_content(SOURCE_URL)

    # 2. 处理内容
    processed = process_iptv_content(raw_content)

    # 3. 写入结果文件（相对仓库根目录）
    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(processed))
        print(f"\n✅ 处理完成！共生成 {len(processed)} 行内容")
        print(f"📄 结果已写入：{os.path.abspath(OUTPUT_FILE)}")
    except OSError as e:
        print(f"❌ 写入文件失败：{e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
