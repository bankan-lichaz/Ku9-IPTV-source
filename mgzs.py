import requests
from urllib.parse import urlparse
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

print("Content-Type: text/plain; charset=utf-8")

# ========== 通用请求头 ==========
HEADERS = {
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
}

# ========== 检测 m3u8 是否可播放 ==========
def check_m3u8_playable(url, timeout=8):
    """
    检测 m3u8 是否可播放：
    - 状态码 == 200
    - 内容包含 #EXTM3U
    """
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

        # 只读取前面一点内容判断是否是 m3u8
        for chunk in resp.iter_content(chunk_size=64):
            if b"#EXTM3U" in chunk:
                return True
            break

        return False

    except Exception:
        return False

# ========== 获取真实流（重试 + 兜底拼接） ==========
def get_final_url(api):
    """
    优先真实跳转（最多 5 次）
    失败后尝试从异常中提取 host+port+path 拼接
    """
    last_exception = None

    # 第一步：最多重试 5 次真实跳转
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

    # 第二步：跳转失败 → 尝试兜底拼接
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

# ========== 处理单个频道（供多线程调用） ==========
def process_channel(line):
    """
    输入：一行 'name,api'
    输出： (name, final_url) 或 None
    """
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

    # 检测是否可播放
    playable = check_m3u8_playable(final_url)
    if not playable:
        print(f"  ❌ {name}：final_url 不可播放\n")
        return None

    print(f"  ✔ {name}：可播放：{final_url}\n")
    return name, final_url

# ========== 主流程：读取 3.txt，多线程生成 MGZS ==========
def main():
    # 读取 3.txt
    try:
        with open("3.txt", "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
    except:
        print("无法读取 3.txt")
        return

    print("================= 开始多线程处理 =================\n")

    results = []

    # 线程池大小（你可以根据源站情况调整）
    max_workers = 8

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_line = {executor.submit(process_channel, line): line for line in lines}

        for future in as_completed(future_to_line):
            res = future.result()
            if res:
                results.append(res)

    # 生成 MGZS：name,final_url
    mgzs_file = "MGZS"
    with open(mgzs_file, "w", encoding="utf-8") as f:
        for name, final_url in results:
            f.write(f"{name},{final_url}\n")

    print(f"\nMGZS 文件已生成：{mgzs_file}")
    print(f"有效频道数量：{len(results)}")


if __name__ == "__main__":
    main()
