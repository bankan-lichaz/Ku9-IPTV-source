import os
import re
import requests
import sys

# 配置项
M3U_URL = "http://izihao.cn:7123"
ICON_SAVE_DIR = "tv_icons"
INVALID_FILENAME_CHARS = r'[\\/:*?"<>|]'

def get_m3u_content(url: str) -> str | None:
    """请求m3u内容"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "*/*"
    }
    try:
        print(f"[INFO] 正在请求 M3U: {url}")
        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
        resp.encoding = resp.apparent_encoding
        print(f"[INFO] M3U 获取成功，大小: {len(resp.text)} bytes")
        return resp.text
    except Exception as e:
        print(f"[ERROR] 请求m3u失败: {str(e)}")
        sys.exit(1)

def parse_m3u(content: str) -> list[tuple[str, str]]:
    """解析m3u内容"""
    pattern = r'#EXTINF:-1.*?tvg-logo="([^"]+)".*?,(.+)$'
    matches = re.findall(pattern, content, flags=re.MULTILINE)
    print(f"[INFO] 解析到 {len(matches)} 个频道")
    return matches

def download_icon(logo_url: str, save_path: str) -> bool:
    """下载图标"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    try:
        resp = requests.get(logo_url, headers=headers, timeout=15)
        resp.raise_for_status()
        
        # 验证是否为有效图片
        if len(resp.content) < 100:
            print(f"[WARN] 文件过小，可能不是有效图片: {logo_url}")
            return False
            
        with open(save_path, 'wb') as f:
            f.write(resp.content)
        return True
    except Exception as e:
        print(f"[ERROR] 下载失败 {logo_url}: {str(e)}")
        return False

def main():
    # 创建保存目录
    os.makedirs(ICON_SAVE_DIR, exist_ok=True)
    print(f"[INFO] 保存目录: {os.path.abspath(ICON_SAVE_DIR)}")
    
    # 获取m3u内容
    m3u_content = get_m3u_content(M3U_URL)
    
    # 解析图标信息
    icon_list = parse_m3u(m3u_content)
    if not icon_list:
        print("[WARN] 未找到任何频道图标信息")
        sys.exit(0)
    
    success_cnt = 0
    skip_cnt = 0
    fail_cnt = 0
    downloaded_files = []

    for logo_url, channel_name in icon_list:
        clean_name = re.sub(INVALID_FILENAME_CHARS, '', channel_name.strip())
        if not clean_name:
            print(f"[WARN] 跳过无效频道名: {channel_name}")
            fail_cnt += 1
            continue
        
        save_path = os.path.join(ICON_SAVE_DIR, f"{clean_name}.webp")
        
        if os.path.exists(save_path):
            print(f"[SKIP] 已存在: {clean_name}.webp")
            skip_cnt += 1
            success_cnt += 1
            downloaded_files.append(f"{clean_name}.webp")
            continue
        
        print(f"[DOWN] 正在下载: {clean_name} -> {logo_url}")
        if download_icon(logo_url, save_path):
            file_size = os.path.getsize(save_path)
            print(f"[OK] 下载成功: {clean_name}.webp ({file_size} bytes)")
            success_cnt += 1
            downloaded_files.append(f"{clean_name}.webp")
        else:
            fail_cnt += 1
    
    # 输出统计
    print("\n" + "="*60)
    print(f"下载统计: 总计 {len(icon_list)} | 成功 {success_cnt} | 跳过 {skip_cnt} | 失败 {fail_cnt}")
    print(f"保存位置: {os.path.abspath(ICON_SAVE_DIR)}")
    
    # 列出所有已下载文件（用于CI日志）
    if downloaded_files:
        print(f"\n已下载文件列表 ({len(downloaded_files)} 个):")
        for f in downloaded_files[:10]:  # 只显示前10个避免日志过长
            print(f"  - {f}")
        if len(downloaded_files) > 10:
            print(f"  ... 还有 {len(downloaded_files)-10} 个文件")

if __name__ == "__main__":
    main()
