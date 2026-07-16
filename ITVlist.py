import multiprocessing
import asyncio
import aiohttp
import re
import datetime
import requests
import os
import time
from urllib.parse import urljoin

URL_FILE = "https://raw.githubusercontent.com/bankan-lichaz/Ku9-IPTV-source/refs/heads/main/ZGHT"

CHANNEL_CATEGORIES = {
    "央视频道": [
        "CCTV1", "CCTV2", "CCTV3", "CCTV4", "CCTV4欧洲", "CCTV4美洲", "CCTV5", "CCTV5+", "CCTV6", "CCTV7",
        "CCTV8", "CCTV9", "CCTV10", "CCTV11", "CCTV12", "CCTV13", "CCTV14", "CCTV15", "CCTV16", "CCTV17",
        "兵器科技", "风云音乐", "风云足球", "风云剧场", "怀旧剧场", "第一剧场", "女性时尚", "世界地理", "央视台球", "高尔夫网球",
        "央视文化精品", "卫生健康", "电视指南", "老故事", "中学生", "发现之旅", "书法频道", "国学频道", "环球奇观"
    ],
    "卫视频道": [
        "湖南卫视", "浙江卫视", "江苏卫视", "东方卫视", "深圳卫视", "北京卫视", "广东卫视", "广西卫视", "东南卫视", "海南卫视",
        "河北卫视", "河南卫视", "湖北卫视", "江西卫视", "四川卫视", "重庆卫视", "贵州卫视", "云南卫视", "天津卫视", "安徽卫视",
        "山东卫视", "辽宁卫视", "黑龙江卫视", "吉林卫视", "内蒙古卫视", "宁夏卫视", "山西卫视", "陕西卫视", "甘肃卫视", "青海卫视",
        "新疆卫视", "西藏卫视", "三沙卫视", "兵团卫视", "延边卫视", "安多卫视", "康巴卫视", "农林卫视", "山东教育卫视",
        "中国教育1台", "中国教育2台", "中国教育3台", "中国教育4台", "早期教育"
    ],
    "数字频道": [
        "CHC动作电影", "CHC家庭影院", "CHC影迷电影", "淘电影", "淘精彩", "淘剧场", "淘4K", "淘娱乐", "淘BABY", "淘萌宠", "重温经典",
        "星空卫视", "CHANNEL[V]", "凤凰卫视中文台", "凤凰卫视资讯台", "凤凰卫视香港台", "凤凰卫视电影台", "求索纪录", "求索科学",
        "求索生活", "求索动物", "纪实人文", "金鹰纪实", "纪实科教", "睛彩青少", "睛彩竞技", "睛彩篮球", "睛彩广场舞", "魅力足球", "五星体育",
        "劲爆体育", "快乐垂钓", "茶频道", "先锋乒羽", "天元围棋", "汽摩", "梨园频道", "文物宝库", "武术世界",
        "乐游", "生活时尚", "都市剧场", "欢笑剧场", "游戏风云", "金色学堂", "动漫秀场", "新动漫", "卡酷少儿", "金鹰卡通", "优漫卡通", "哈哈炫动", "嘉佳卡通", 
        "优优宝贝", "中国交通", "中国天气", "海看大片", "经典电影", "精彩影视", "喜剧影院", "动作影院", "精品剧场"
    ],
}

CHANNEL_MAPPING = {
    "CCTV13": ["CCTV-13", "CCTV13-新闻", "CCTV新闻", "CCTV-新闻"],
    "CCTV14": ["CCTV-14", "CCTV14-少儿", "CCTV少儿", "CCTV-少儿"],
    # 你的其他映射保持不变……
}

RESULTS_PER_CHANNEL = 20


def load_urls():
    try:
        resp = requests.get(URL_FILE, timeout=5)
        resp.raise_for_status()
        urls = [line.strip() for line in resp.text.splitlines() if line.strip()]
        print(f"📡 已加载 {len(urls)} 个基础 URL")
        return urls
    except Exception as e:
        print(f"❌ 下载 {URL_FILE} 失败: {e}")
        exit()


async def generate_urls(url):
    modified_urls = []
    ip_start = url.find("//") + 2
    ip_end = url.find(":", ip_start)

    base = url[:ip_start]
    ip_prefix = url[ip_start:ip_end].rsplit('.', 1)[0]
    port = url[ip_end:]

    json_paths = [
        "/iptv/live/1000.json?key=txiptv",
        "/iptv/live/1001.json?key=txiptv",
    ]

    for i in range(1, 256):
        ip = f"{base}{ip_prefix}.{i}{port}"
        for path in json_paths:
            modified_urls.append(f"{ip}{path}")

    return modified_urls


async def check_url(session, url, semaphore):
    async with semaphore:
        try:
            async with session.get(url, timeout=1) as resp:
                if resp.status == 200:
                    return url
        except:
            return None


async def fetch_json(session, url, semaphore):
    async with semaphore:
        try:
            async with session.get(url, timeout=2) as resp:
                data = await resp.json()
                results = []
                for item in data.get('data', []):
                    name = item.get('name')
                    urlx = item.get('url')
                    if not name or not urlx or ',' in urlx:
                        continue

                    if not urlx.startswith("http"):
                        urlx = urljoin(url, urlx)

                    for std_name, aliases in CHANNEL_MAPPING.items():
                        if name in aliases:
                            name = std_name
                            break

                    results.append((name, urlx))
                return results
        except:
            return []


async def fetch_streamer(session, base_url, semaphore):
    async with semaphore:
        url = base_url.replace("/iptv/live/1000.json?key=txiptv", "/streamer/list")
        url = url.replace("/iptv/live/1001.json?key=txiptv", "/streamer/list")

        try:
            async with session.get(url, timeout=2) as resp:
                data = await resp.json()
                if not isinstance(data, list):
                    return []

                results = []
                for item in data:
                    name = item.get("name", "").strip()
                    key = item.get("key", "").strip()
                    if not name or not key:
                        continue

                    full_url = f"{base_url.split('/iptv/')[0]}/hls/{key}/index.m3u8"
                    results.append((name, full_url))

                return results
        except:
            return []


async def measure_speed(session, url, semaphore):
    async with semaphore:
        start = time.time()
        try:
            async with session.get(url, timeout=0.8) as resp:
                if resp.status != 200:
                    return 999999
                await resp.content.read(32768)
                return int((time.time() - start) * 1000)
        except:
            return 999999


def is_valid_stream(url):
    if url.startswith(("rtp://", "udp://", "rtsp://")):
        return False
    if "239." in url:
        return False
    if url.startswith(("http://10.", "http://192.168.", "http://127.")):
        return False
    if "/paiptv/" in url or "/00/SNM/" in url or "/00/CHANNEL" in url:
        return False
    if not (url.endswith(".m3u8") or ".m3u8?" in url or ".ts" in url):
        return False
    return True


async def main():
    print("🚀 开始运行 ITVlist 脚本")

    CPU = multiprocessing.cpu_count()
    semaphore = asyncio.Semaphore(80 + CPU * 20)

    urls = load_urls()

    async with aiohttp.ClientSession() as session:
        all_urls = []
        for url in urls:
            modified_urls = await generate_urls(url)
            all_urls.extend(modified_urls)

        print(f"🔍 生成待扫描 URL 共: {len(all_urls)} 个")

        print("⏳ 开始检测可用 JSON API...")
        tasks = [check_url(session, u, semaphore) for u in all_urls]
        valid_urls = [r for r in await asyncio.gather(*tasks) if r]

        print(f"✅ 可用 JSON 地址: {len(valid_urls)} 个")

        print("📥 开始抓取节目单 JSON + Streamer...")
        results = []
        for u in valid_urls:
            json_result = await fetch_json(session, u, semaphore)
            if json_result:
                results.extend(json_result)
                continue

            streamer_result = await fetch_streamer(session, u, semaphore)
            if streamer_result:
                print(f"🔄 {u} 使用 Streamer 接口成功，共 {len(streamer_result)} 条")
                results.extend(streamer_result)
            else:
                print(f"❌ {u} JSON 和 Streamer 都失败")

        final_results = [(name, url, 0) for name, url in results]
        final_results = [(name, url, speed) for name, url, speed in final_results if is_valid_stream(url)]

        print("🚀 开始测速频道源...")
        speed_tasks = [measure_speed(session, url, semaphore) for (_, url, _) in final_results]
        speeds = await asyncio.gather(*speed_tasks)

        final_results = [(name, url, speed) for (name, url, _), speed in zip(final_results, speeds)]
        final_results.sort(key=lambda x: (x[2], x[0]))

        itv_dict = {cat: [] for cat in CHANNEL_CATEGORIES}
        for name, url, speed in final_results:
            for cat, channels in CHANNEL_CATEGORIES.items():
                if name in channels:
                    itv_dict[cat].append((name, url, speed))
                    break

        beijing_now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")
        disclaimer_url = "https://aegis-cloudfront-1.tubi.video/bb1fc6ad-9948-42ea-aaf3-20acfcdeecac/playlist720p.m3u8"

        with open("itvlist.txt", 'w', encoding='utf-8') as f:
            f.write(f"更新时间: {beijing_now}（北京时间）\n\n")
            f.write("更新时间,#genre#\n")
            f.write(f"更新时间：{beijing_now},{disclaimer_url}\n\n")

            for cat in CHANNEL_CATEGORIES:
                f.write(f"{cat},#genre#\n")
                for ch in CHANNEL_CATEGORIES[cat]:
                    ch_items = [x for x in itv_dict[cat] if x[0] == ch]
                    ch_items = ch_items[:RESULTS_PER_CHANNEL]
                    for item in ch_items:
                        f.write(f"{item[0]},{item[1]}\n")

    print("🎉 itvlist.txt 已生成完成！")


if __name__ == "__main__":
    asyncio.run(main())
