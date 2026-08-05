import requests
from urllib.parse import urlparse
import re
import time

print("Content-Type: text/plain; charset=utf-8")

# 读取文件
try:
    with open("3.txt", "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
except:
    print("无法读取 3.txt")
    exit()

results = []

HEADERS = {
    "Connection": "keep-alive",
    "User-Agent": "okhttp/5.3.2"
}

def get_final_url(api):
    """
    优先真实跳转，失败自动重试 5 次。
    如果仍失败，再使用 host+port+path 拼接作为兜底。
    """

    # ⭐ 第 1 步：最多重试 5 次真实跳转
    for i in range(5):
        try:
            resp = requests.get(api, headers=HEADERS, timeout=10, allow_redirects=True)
            return resp.url  # 成功跳转，直接返回真实流
        except Exception as e:
            print(f"  ⚠ 第 {i+1} 次跳转失败：{e}")
            time.sleep(0.5)

    # ⭐ 第 2 步：5 次都失败 → 尝试从异常中提取 host+port+path 拼接
    msg = str(e)

    host_match = re.search(r"host='([^']+)'", msg)
    port_match = re.search(r"port=(\d+)", msg)
    url_match = re.search(r"url: ([^\s]+)", msg)

    if host_match and port_match and url_match:
        host = host_match.group(1)
        port = port_match.group(1)
        path = url_match.group(1)
        final_url = f"http://{host}:{port}{path}"
        print(f"  ⚠ 已使用兜底拼接真实流地址：{final_url}")
        return final_url

    print("  ❌ 无法获取真实流地址（跳转失败 + 拼接失败）")
    return None


print("================= 开始处理 =================\n")

for line in lines:
    name, api = line.split(",", 1)
    print(f"正在处理：{name} ({api})")

    final_url = get_final_url(api)
    if not final_url:
        print("  ❌ 跳过：无法获取真实流地址\n")
        continue

    print(f"  ✔ 最终流地址：{final_url}\n")

    results.append({
        "name": name,
        "final": final_url
    })


# ⭐ 生成 MGZS 文件：name,final_url
mgzs_file = "MGZS"

with open(mgzs_file, "w", encoding="utf-8") as f:
    for r in results:
        f.write(f"{r['name']},{r['final']}\n")

print(f"\nMGZS 文件已生成：{mgzs_file}")
