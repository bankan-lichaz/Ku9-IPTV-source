import socket
import ipaddress
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.exceptions import RequestException

ZB_FILE_1 = "ZB1"
ZB_FILE_2 = "ZB2"
ZB_FILE_3 = "ZB3"
ZB_FILE_4 = "ZB4"
ZB_FILE_5 = "ZB5"
ZB_FILE_6 = "ZB6"

# 原有第一段扫描配置（完全保留，未修改）
START_IP = "116.2.160.1"
END_IP = "116.2.180.255"
PORT = 4010

START_IP1b = "123.191.12.1"
END_IP1b = "123.191.12.255"
PORT1b = 1111

# 新增第二段扫描配置
START_IP2 = "220.167.170.1"
END_IP2 = "220.167.170.255"
PORT2 = 4000

# 新增第三段扫描配置
START_IP3 = "112.192.72.1"
END_IP3 = "112.192.73.255"
PORT3 = 8484

# 新增第四段扫描配置
START_IP4a = "39.77.160.1"
END_IP4a = "39.77.170.255"
PORT4a = 4002

START_IP4b = "39.77.20.1"
END_IP4b = "39.77.30.255"
PORT4b = 4002

# 新增第五段扫描配置
START_IP5a = "111.196.125.1"
END_IP5a = "111.196.135.255"
PORT5a = 20000

START_IP5b = "221.220.130.1"
END_IP5b = "221.220.132.255"
PORT5b = 8012

START_IP5c = "114.254.30.1"
END_IP5c = "114.254.40.255"
PORT5c = 8888

# 新增第六段扫描配置
START_IP6 = "112.109.206.1"
END_IP6 = "112.109.206.255"
PORT6 = 9999


def expand_ip_range(start_ip, end_ip):
    start = ipaddress.IPv4Address(start_ip)
    end = ipaddress.IPv4Address(end_ip)
    return [str(ipaddress.IPv4Address(ip)) for ip in range(int(start), int(end) + 1)]

def scan_single_ip(ip, port, timeout=0.3):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        sock.close()
        if result == 0:
            return f"{ip}:{port}"
    except:
        pass
    return None

# 原有scan_all函数仅增加默认参数，原有调用逻辑完全不变，功能完全一致
#def scan_all(start_ip=START_IP, end_ip=END_IP, port=PORT):
#    ip_list = expand_ip_range(start_ip, end_ip)
#    open_targets = []

#    print(f"总扫描 IP 数量：{len(ip_list)}")

#    with ThreadPoolExecutor(max_workers=1000) as executor:
#        futures = {executor.submit(scan_single_ip, ip, port): ip for ip in ip_list}

#        for i, future in enumerate(as_completed(futures)):
#            ip = futures[future]
#            try:
#                result = future.result()
#                if result:
#                    open_targets.append(result)
#                    print(f"开放：{result}")
#            except:
#                pass

#            if i % 200 == 0:
#                print(f"进度：{i}/{len(ip_list)}")

#    return open_targets

# 可扫多个IP段的scan_all函数，完全兼容原有单个ip段扫描逻辑
def scan_all(start_ip=START_IP, end_ip=END_IP, port=PORT, ip_segments=None):
    """
    支持单段/多段扫描
    参数：
    - 单段调用：传start_ip/end_ip/port（和原来用法完全一致）
    - 多段调用：传ip_segments，格式为 [(段1start, 段1end, 段1port), (段2start, 段2end, 段2port), ...]
    """
    # 收集所有要扫描的IP段
    segments = []
    # 兼容原来的单段参数调用
    if start_ip != START_IP or end_ip != END_IP or port != PORT:
        segments.append((start_ip, end_ip, port))
    # 添加多段参数
    if ip_segments:
        segments.extend(ip_segments)
    # 如果没传任何参数，用默认段
    if not segments:
        segments.append((START_IP, END_IP, PORT))

    # 预处理所有段的IP，统计总数
    all_ip_port_pairs = []  # 存储所有(ip, port)待扫描对
    total_ips = 0
    for seg_start, seg_end, seg_port in segments:
        current_ip_list = expand_ip_range(seg_start, seg_end)
        all_ip_port_pairs.extend([(ip, seg_port) for ip in current_ip_list])
        total_ips += len(current_ip_list)
        print(f"已加载IP段 {seg_start}-{seg_end} 端口 {seg_port}，共 {len(current_ip_list)} 个IP")
    
    print(f"\n总待扫描 IP:端口 数量：{total_ips}")
    open_targets = []

    # 线程数可以根据总IP数动态调整，避免IP少时开太多线程浪费资源
    max_workers = min(1000, total_ips) if total_ips > 0 else 1000
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交所有扫描任务
        futures = {
            executor.submit(scan_single_ip, ip, port): (ip, port)
            for ip, port in all_ip_port_pairs
        }

        completed = 0
        for future in as_completed(futures):
            ip, port = futures[future]
            try:
                result = future.result()
                if result:
                    open_targets.append(result)
                    print(f"开放：{result}")
            except Exception as e:
                # 建议保留错误打印，方便排查扫描失败的问题，不需要可以删掉
                # print(f"扫描 {ip}:{port} 失败：{str(e)}")
                pass

            completed += 1
            if completed % 200 == 0:
                print(f"总进度：{completed}/{total_ips}")

    # 这里可以加之前说的去重、排序逻辑，按需开启即可
    # 去重（字符串结果示例）
    # open_targets = list(set(open_targets))
    # 按IP+端口排序
    # open_targets = sorted(open_targets, key=lambda x: (socket.inet_aton(x["ip"]), x["port"]))

    return open_targets

# 过滤 open_targets结果 删除无效结果
def filter_valid_targets(open_targets, max_workers=50, timeout=5, retries=1, scheme="http", verify=False, print_progress=True):
    """
    过滤scan_all返回的开放目标，保留访问/status接口不返回Not Found的目标
    :param open_targets: scan_all返回的开放目标列表，每个元素支持两种格式：
        1. "ip:port" 格式的字符串（比如 "192.168.1.1:8080"）
        2. 包含ip、port字段的字典（比如 {"ip": "192.168.1.1", "port": 8080}）
    :param max_workers: 并发请求线程数，默认50（根据自身网络和目标承受能力调整）
    :param timeout: 单次请求超时时间（秒），默认5
    :param retries: 请求失败重试次数，默认1（避免网络波动误判）
    :param scheme: 请求协议，默认http，若目标用https可改为"https"
    :param verify: 是否验证SSL证书，默认False，https场景下需要验证可设为True
    :param print_progress: 是否打印处理进度，默认True
    :return: 过滤后的合格目标列表
    """
    if not open_targets:
        return []
    
    valid_targets = []
    total = len(open_targets)
    # 默认请求头，避免被服务器拦截默认的python-requests请求
    default_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    def check_target(target):
        """单个目标校验逻辑"""
        # 兼容解析目标格式
        if isinstance(target, str):
            parts = target.split(":")
            if len(parts) != 2:
                return None
            ip, port = parts[0], parts[1]
        elif isinstance(target, dict):
            ip = target.get("ip")
            port = target.get("port")
            if not ip or not port:
                return None
        else:
            return None
        
        url = f"{scheme}://{ip}:{port}/status"
        
        # 重试逻辑
        for _ in range(retries + 1):
            try:
                response = requests.get(
                    url, 
                    timeout=timeout, 
                    verify=verify,
                    headers=default_headers
                )
                # 判断响应内容是否不含Not Found（区分大小写，不需要区分可以改成.lower()后判断）
                if b"Not Found" not in response.content:
                    return target
                # 包含Not Found直接判定为不合格，不需要重试
                return None
            except RequestException:
                # 请求失败继续重试
                continue
        # 重试都失败判定为不合格
        return None

    # 多线程并发校验
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(check_target, target): target for target in open_targets}
        
        for i, future in enumerate(as_completed(futures)):
            result = future.result()
            if result:
                valid_targets.append(result)
                if print_progress:
                    print(f"合格目标：{result}")
            
            if print_progress and i % 200 == 0:
                print(f"过滤进度：{i}/{total}，当前合格数：{len(valid_targets)}")
    
    return valid_targets

# 测速筛选 获取有效结果
def get_verified_rtp_targets(
    open_targets: list,  # 直接传scan_all返回的open_targets
    target_rtp_stream_addr: str,  # 你指定的新参数，比如"239.3.1.116:8000"
    max_workers: int = 100,  # 测速阶段线程数，可根据机器性能调整
    speed_threshold_mbps: float = 2.0,  # 速度合格阈值（单位Mbps），低于则判定不合格
    request_timeout: int = 5,  # 单次请求超时时间（秒），超时直接判定不合格
    use_https: bool = False  # 是否用HTTPS访问，默认HTTP
) -> list:
    """
    对scan_all返回的开放ip:port列表做RTP接口验证+测速，返回合格的ip:port列表
    """
    if not open_targets:
        print("输入的open_targets为空，直接返回空列表")
        return []
    
    print(f"\n开始对 {len(open_targets)} 个开放目标做RTP接口测速验证...")
    qualified_targets = []
    total = len(open_targets)
    protocol = "https" if use_https else "http"

    def _verify_single(target: str) -> str | None:
        """单个目标验证逻辑，合格返回原target，不合格返回None"""
        # 拼接符合要求的URL，比如 http://192.168.1.10:554/rtp/239.3.1.116:8000
        url = f"{protocol}://{target}/rtp/{target_rtp_stream_addr}"
        try:
            start_time = time.time()
            # 开启流式读取，用于测实际下载速度
            resp = requests.get(url, timeout=request_timeout, stream=True)
            if resp.status_code != 200:
                return None
            
            # 读取1秒内的数据计算实际下载速度
            downloaded_bytes = 0
            end_time = start_time + 1.0  # 测速时长1秒，可调整
            for chunk in resp.iter_content(chunk_size=1024):
                if time.time() >= end_time:
                    break
                downloaded_bytes += len(chunk)
            
            # 字节转Mbps：1字节=8比特，1Mbps=1e6比特/秒
            elapsed = time.time() - start_time
            if elapsed <= 0:
                return None
            speed_mbps = (downloaded_bytes * 8) / (elapsed * 1e6)
            
            # 速度达标才返回合格
            if speed_mbps >= speed_threshold_mbps:
                return target
        except Exception:
            # 任何异常（超时、连接失败、404/500等）都判定为不合格
            pass
        return None

    # 多线程批量验证，和原scan_all的并发逻辑一致
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(_verify_single, target): target for target in open_targets}
        
        for i, future in enumerate(as_completed(futures)):
            result = future.result()
            if result:
                qualified_targets.append(result)
                print(f"验证合格：{result}")
            
            # 进度打印风格和原scan_all完全统一
            if (i + 1) % 200 == 0:
                print(f"验证进度：{i+1}/{total}，当前合格数：{len(qualified_targets)}")

    print(f"验证完成，共 {len(qualified_targets)}/{total} 个目标合格")
    return qualified_targets

# 原有ZB文件第一行更新函数完全保留，未修改任何逻辑
def update_zb_file(open_targets):
    """
    第一行格式：
    64,IP:PORT,IP:PORT
    如果没有开放端口：lines[0] 清空
    """
    try:
        with open(ZB_FILE_1, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = ["\n"]  # 文件不存在时创建一个空行

    if open_targets:
        # 有开放端口 → 写入 64,IP:PORT...
        new_first_line = "71," + ",".join(open_targets) + "\n"
    #    new_first_line = "\n"
        lines[0] = new_first_line
        print("ZB1 文件已更新：", new_first_line.strip())
    else:
        # ⭐ 没有开放端口 → 第一行清空
        lines[0] = "\n"
        print("未扫描到开放端口，已清空 ZB1 第一行")

    with open(ZB_FILE_1, "w", encoding="utf-8") as f:
        f.writelines(lines)

# 新增：ZB2文件第一行更新函数，逻辑与第一行更新完全对齐
def update_zb_file_second(open_targets):
    """
    第一行格式：
    13,IP:PORT,IP:PORT
    如果没有开放端口：lines[1] 清空
    """
    try:
        with open(ZB_FILE_2, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = ["\n"]  # 文件不存在时创建一个空行


    if open_targets:
        new_first_line = "13," + ",".join(open_targets) + "\n"
        lines[0] = new_first_line
        print("ZB2 文件第一行已更新：", new_first_line.strip())
    else:
        lines[0] = "\n"
        print("第二段未扫描到开放端口，已清空 ZB2 第一行")

    with open(ZB_FILE_2, "w", encoding="utf-8") as f:
        f.writelines(lines)

# 新增：ZB3文件第一行更新函数，逻辑与第一行更新完全对齐
def update_zb_file_third(open_targets):
    """
    第一行格式：
    40,IP:PORT,IP:PORT
    如果没有开放端口：lines[1] 清空
    """
    try:
        with open(ZB_FILE_3, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = ["\n"]  # 文件不存在时创建一个空行


    if open_targets:
        new_first_line = "40," + ",".join(open_targets) + "\n"
        lines[0] = new_first_line
        print("ZB3 文件第一行已更新：", new_first_line.strip())
    else:
        lines[0] = "\n"
        print("第三段未扫描到开放端口，已清空 ZB3 第一行")

    with open(ZB_FILE_3, "w", encoding="utf-8") as f:
        f.writelines(lines)

# 新增：ZB4文件第一行更新函数，逻辑与第一行更新完全对齐
def update_zb_file_forth(open_targets):
    """
    第一行格式：
    26,IP:PORT,IP:PORT
    如果没有开放端口：lines[1] 清空
    """
    try:
        with open(ZB_FILE_4, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = ["\n"]  # 文件不存在时创建一个空行


    if open_targets:
        new_first_line = "26," + ",".join(open_targets) + "\n"
        lines[0] = new_first_line
        print("ZB4 文件第一行已更新：", new_first_line.strip())
    else:
        lines[0] = "\n"
        print("第四段未扫描到开放端口，已清空 ZB4 第一行")

    with open(ZB_FILE_4, "w", encoding="utf-8") as f:
        f.writelines(lines)

# 新增：ZB5文件第一行更新函数，逻辑与第一行更新完全对齐
def update_zb_file_fifth(open_targets):
    """
    第一行格式：
    17,IP:PORT,IP:PORT
    如果没有开放端口：lines[1] 清空
    """
    try:
        with open(ZB_FILE_5, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = ["\n"]  # 文件不存在时创建一个空行


    if open_targets:
        new_first_line = "17," + ",".join(open_targets) + "\n"
        lines[0] = new_first_line
        print("ZB5 文件第一行已更新：", new_first_line.strip())
    else:
        lines[0] = "\n"
        print("第五段未扫描到开放端口，已清空 ZB5 第一行")

    with open(ZB_FILE_5, "w", encoding="utf-8") as f:
        f.writelines(lines)

# 新增：ZB6文件第一行更新函数，逻辑与第一行更新完全对齐
def update_zb_file_sixth(open_targets):
    """
    第一行格式：
    73,IP:PORT,IP:PORT
    如果没有开放端口：lines[1] 清空
    """
    try:
        with open(ZB_FILE_6, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = ["\n"]  # 文件不存在时创建一个空行


    if open_targets:
        new_first_line = "73," + ",".join(open_targets) + "\n"
        lines[0] = new_first_line
        print("ZB6 文件第一行已更新：", new_first_line.strip())
    else:
        lines[0] = "\n"
        print("第六段未扫描到开放端口，已清空 ZB6 第一行")

    with open(ZB_FILE_6, "w", encoding="utf-8") as f:
        f.writelines(lines)

if __name__ == "__main__":
    # 原有第一段扫描逻辑完全保留，无任何修改
    print(f"\n开始扫描第一段 {START_IP}-{END_IP} 端口 {PORT}, {START_IP1b}-{END_IP1b} 端口 {PORT1b} ...")   
    open_targets = scan_all(ip_segments=[
    (START_IP, END_IP, PORT),
    (START_IP1b, END_IP1b, PORT1b)
    ])
    update_zb_file(open_targets)

    # 新增第二段扫描逻辑
    print(f"\n开始扫描第二段 {START_IP2}-{END_IP2} 端口 {PORT2} ...")
    open_targets2 = scan_all(START_IP2, END_IP2, PORT2)
    update_zb_file_second(open_targets2)

    # 新增第三段扫描逻辑
    print(f"\n开始扫描第三段 {START_IP3}-{END_IP3} 端口 {PORT3} ...")
    open_targets3 = scan_all(START_IP3, END_IP3, PORT3)
    update_zb_file_third(open_targets3)

    # 新增第四段扫描逻辑
    print(f"\n开始扫描第四段 {START_IP4a}-{END_IP4a} 端口 {PORT4a}, {START_IP4b}-{END_IP4b} 端口 {PORT4b} ...")
    open_targets4 = scan_all(ip_segments=[
    (START_IP4a, END_IP4a, PORT4a),
    (START_IP4b, END_IP4b, PORT4b)
    ])                         
    update_zb_file_forth(open_targets4)

    # 新增第五段扫描逻辑
    print(f"\n开始扫描第五段 {START_IP5a}-{END_IP5a} 端口 {PORT5a}, {START_IP5b}-{END_IP5b} 端口 {PORT5b} ...")
    open_targets5 = scan_all(ip_segments=[
    (START_IP5a, END_IP5a, PORT5a),
    (START_IP5b, END_IP5b, PORT5b),
    (START_IP5c, END_IP5c, PORT5c)
    ])
    open_targets5 = get_verified_rtp_targets(
        open_targets,
        target_rtp_stream_addr="239.3.1.116:8000"
    )
    update_zb_file_fifth(open_targets5)

    # 新增第六段扫描逻辑
    print(f"\n开始扫描第六段 {START_IP6}-{END_IP6} 端口 {PORT6} ...")
    open_targets6 = scan_all(START_IP6, END_IP6, PORT6)
    update_zb_file_sixth(open_targets6)
