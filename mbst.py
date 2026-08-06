import requests
from urllib.parse import urlparse
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

print("Content-Type: text/plain; charset=utf-8")

HEADERS = {
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
}

def check_m3u8_playable(url, timeout=8):
    try:
        resp = requests.get(
            url,
            headers=HEADERS,
            timeout=timeout,
            allow_redirects=True,
            stream=True,
            verify=False
        )

        if resp.status_code != 200:
            return False

        for chunk in resp.iter_content(chunk_size=64):
            if b"#EXTM3U" in chunk:
                return True
            break

        return False

    except Exception:
        return False


def get_final_url(api):
    last_exception = None

    for i in range(5):
        try:
            print(f"    第 {i+1} 次尝试跳转")
            resp = requests.get(
                api,
                headers=HEADERS,
                timeout=10,
                allow_redirects=True,
                verify=False
            )
            final_url = resp.url
            print(f"    ✔ 跳转成功：{final_url}")
            return final_url

        except Exception as e:
            last_exception = e
            print(f"    ⚠ 跳转失败：{e}")
            time.sleep(0.5)

    msg = str(last_exception)
    host_match = re.search(r"host='([^']+)'", msg)
    port_match = re.search(r"port=(\d+)", msg)
    url_match = re.search(r"url: ([^\s]+)", msg)

    if host_match and port_match and url_match:
        host = host_match.group(1)
        port = port_match.group(1)
        path = url_match.group(1)
        final_url = f"http://{host}:{port}{path}"
        print(f"    ⚠ 使用兜底拼接：{final_url}")
        return final_url

    print("    ❌ 跳转失败 + 拼接失败")
    return None


def process_channel(index, line):
    try:
        name, api = line.split(",", 1)
    except ValueError:
        print(f"行格式错误：{line}")
        return None

    print(f"正在处理：{name} ({api})")

    final_url = get_final_url(api)
    if not final_url:
        print(f"  ❌ {name}：无法获取 final_url\n")
        return None

    playable = check_m3u8_playable(final_url)
    if not playable:
        print(f"  ⚠ {name}：final_url 不可播放，但仍写入\n")
    else:
        print(f"  ✔ {name}：可播放：{final_url}\n")

    # ⭐ 无论是否可播放，都写入
    return index, name, final_url


def main():
    try:
        with open("2.txt", "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
    except:
        print("无法读取 2.txt")
        return

    print("================= 开始多线程处理 =================\n")

    results = []

    max_workers = 8

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_index = {
            executor.submit(process_channel, idx, line): idx
            for idx, line in enumerate(lines)
        }

        for future in as_completed(future_to_index):
            res = future.result()
            if res:
                results.append(res)

    # ⭐ 按 index 排序，保证频道顺序不变
    results.sort(key=lambda x: x[0])

    mbst_file = "MBST"
    with open(mbst_file, "w", encoding="utf-8") as f:
        for _, name, final_url in results:
            f.write(f"{name},{final_url}\n")

    print(f"\nMBST 文件已生成：{mbst_file}")
    print(f"有效频道数量：{len(results)}")


if __name__ == "__main__":
    main()
