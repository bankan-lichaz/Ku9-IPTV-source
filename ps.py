import time
import socket
import ipaddress
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.exceptions import RequestException

ZB_FILE_0 = "ZZ"
ZB_FILE_1 = "ZB1"
ZB_FILE_2 = "ZB2"
ZB_FILE_3 = "ZB3"
ZB_FILE_4 = "ZB4"
ZB_FILE_5 = "ZB5"
ZB_FILE_6 = "ZB6"
ZB_FILE_7 = "ZB7"
ZB_FILE_8 = "ZB8"
ZB_FILE_9 = "ZB9"
ZB_FILE_10 = "ZB10"
ZB_FILE_11 = "ZB11"
ZB_FILE = "ZB"  # 合并后的输出文件

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

START_IP5b = "221.220.128.1"
END_IP5b = "221.220.132.255"
PORT5b = 8012

START_IP5c = "114.254.30.1"
END_IP5c = "114.254.40.255"
PORT5c = 8888

# 新增第五-1段扫描配置
START_IP5_1a = "115.171.216.1"
END_IP5_1a = "115.171.216.255"
PORT5_1a = 4000

# 新增第六段扫描配置
START_IP6 = "112.109.206.1"
END_IP6 = "112.109.206.255"
PORT6 = 9999

# 新增第七段扫描配置
START_IP7a = "124.112.187.1"
END_IP7a = "124.112.190.255"
PORT7a = 4022

START_IP7b = "124.112.240.1"
END_IP7b = "124.112.241.255"
PORT7b = 4022

START_IP7c = "183.162.102.1"
END_IP7c = "183.162.106.255"
PORT7c = 8888

# 新增第八段扫描配置
START_IP8a = "112.115.45.1"
END_IP8a = "112.115.55.255"
PORT8a = 4915

START_IP8b = "106.57.0.1"
END_IP8b = "106.59.3.255"
PORT8b = 55555

# 新增第九段扫描配置
START_IP9a = "113.58.30.1"
END_IP9a = "113.58.32.255"
PORT9a = 8188

START_IP9b = "113.58.6.1"
END_IP9b = "113.58.8.255"
PORT9b = 8188

# 新增第十段扫描配置
START_IP10a = "183.184.40.1"
END_IP10a = "183.184.45.255"
PORT10a = 8001

START_IP10b = "183.184.145.1"
END_IP10b = "183.184.150.255"
PORT10b = 8001

START_IP10c = "60.223.70.1"
END_IP10c = "60.223.75.255"
PORT10c = 8003

# 新增第十-1段扫描配置
START_IP10_1a = "110.178.140.1"
END_IP10_1a = "110.178.150.255"
PORT10_1a = 8188

# 新增第十一段扫描配置
START_IP11a = "116.114.135.1"
END_IP11a = "116.114.145.255"
PORT11a = 8686

START_IP11b = "219.159.28.1"
END_IP11b = "219.159.28.255"
PORT11b = 8188

START_IP11c = "124.67.65.1"
END_IP11c = "124.67.70.255"
PORT11c = 4022

# 新增第十一-1段扫描配置
START_IP11_1a = "1.181.135.1"
END_IP11_1a = "1.181.140.255"
PORT11_1a = 8888

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
    speed_threshold_mbps: float = 0.0,  # 速度合格阈值（单位Mbps），低于则判定不合格
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
        # 如果target是(ip, port)元组，改成这行：
        #url = f"{protocol}://{target[0]}:{target[1]}/rtp/{target_rtp_stream_addr}"
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

# 原有ZZ文件第一行更新函数完全保留，未修改任何逻辑
def update_zb_file_zero(open_targets):
    """
    第一行格式：
    1,IP:PORT,IP:PORT
    如果没有开放端口：lines[0] 清空
    """
    try:
        with open(ZB_FILE_0, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = ["\n"]  # 文件不存在时创建一个空行

    if open_targets:
        # 有开放端口 → 写入 64,IP:PORT...
        new_first_line = "1," + ",".join(open_targets) + "\n"
    #    new_first_line = "\n"
        lines[0] = new_first_line
        print("ZZ 文件已更新：", new_first_line.strip())
    else:
        # ⭐ 没有开放端口 → 第一行清空
        lines[0] = "\n"
        print("未扫描到开放端口，已清空 ZZ 第一行")

    with open(ZB_FILE_0, "w", encoding="utf-8") as f:
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
        lines = ["\n","\n"]  # 文件不存在时创建两个空行


    if open_targets:
        new_first_line = "17," + ",".join(open_targets) + "\n"
        lines[0] = new_first_line
        print("ZB5 文件第一行已更新：", new_first_line.strip())
    else:
        lines[0] = "\n"
        print("第五段未扫描到开放端口，已清空 ZB5 第一行")

    with open(ZB_FILE_5, "w", encoding="utf-8") as f:
        f.writelines(lines)

def update_zb_file_fifth_1(open_targets):
    """
    第二行格式：
    29,IP:PORT,IP:PORT
    如果没有开放端口：lines[1] 清空
    """
    try:
        with open(ZB_FILE_5, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = ["\n","\n"]  # 文件不存在时创建两个空行


    if open_targets:
        new_second_line = "29," + ",".join(open_targets) + "\n"
        lines[1] = new_second_line
        print("ZB5 文件第二行已更新：", new_second_line.strip())
    else:
        lines[1] = "\n"
        print("第五段未扫描到开放端口，已清空 ZB5 第二行")

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

# 新增：ZB7文件第一行更新函数，逻辑与第一行更新完全对齐
def update_zb_file_seventh(open_targets):
    """
    第一行格式：
    21,IP:PORT,IP:PORT
    如果没有开放端口：lines[1] 清空
    """
    try:
        with open(ZB_FILE_7, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = ["\n"]  # 文件不存在时创建一个空行


    if open_targets:
        new_first_line = "21," + ",".join(open_targets) + "\n"
        lines[0] = new_first_line
        print("ZB7 文件第一行已更新：", new_first_line.strip())
    else:
        lines[0] = "\n"
        print("第七段未扫描到开放端口，已清空 ZB7 第一行")

    with open(ZB_FILE_7, "w", encoding="utf-8") as f:
        f.writelines(lines)

# 新增：ZB8文件第一行更新函数，逻辑与第一行更新完全对齐
def update_zb_file_eighth(open_targets):
    """
    第一行格式：
    75,IP:PORT,IP:PORT
    如果没有开放端口：lines[1] 清空
    """
    try:
        with open(ZB_FILE_8, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = ["\n"]  # 文件不存在时创建一个空行


    if open_targets:
        new_first_line = "75," + ",".join(open_targets) + "\n"
        lines[0] = new_first_line
        print("ZB8 文件第一行已更新：", new_first_line.strip())
    else:
        lines[0] = "\n"
        print("第八段未扫描到开放端口，已清空 ZB8 第一行")

    with open(ZB_FILE_8, "w", encoding="utf-8") as f:
        f.writelines(lines)

# 新增：ZB9文件第一行更新函数，逻辑与第一行更新完全对齐
def update_zb_file_nineth(open_targets):
    """
    第一行格式：
    84,IP:PORT,IP:PORT
    如果没有开放端口：lines[1] 清空
    """
    try:
        with open(ZB_FILE_9, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = ["\n"]  # 文件不存在时创建一个空行


    if open_targets:
        new_first_line = "84," + ",".join(open_targets) + "\n"
        lines[0] = new_first_line
        print("ZB9 文件第一行已更新：", new_first_line.strip())
    else:
        lines[0] = "\n"
        print("第九段未扫描到开放端口，已清空 ZB9 第一行")

    with open(ZB_FILE_9, "w", encoding="utf-8") as f:
        f.writelines(lines)

# 新增：ZB10文件第一行更新函数，逻辑与第一行更新完全对齐
def update_zb_file_tenth(open_targets):
    """
    第一行格式：
    79,IP:PORT,IP:PORT
    如果没有开放端口：lines[1] 清空
    """
    try:
        with open(ZB_FILE_10, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = ["\n","\n"]  # 文件不存在时创建两个空行


    if open_targets:
        new_first_line = "79," + ",".join(open_targets) + "\n"
        lines[0] = new_first_line
        print("ZB10 文件第一行已更新：", new_first_line.strip())
    else:
        lines[0] = "\n"
        print("第十段未扫描到开放端口，已清空 ZB10 第一行")

    with open(ZB_FILE_10, "w", encoding="utf-8") as f:
        f.writelines(lines)

def update_zb_file_tenth_1(open_targets):
    """
    第二行格式：
    18,IP:PORT,IP:PORT
    如果没有开放端口：lines[1] 清空
    """
    try:
        with open(ZB_FILE_10, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = ["\n","\n"]  # 文件不存在时创建两个空行


    if open_targets:
        new_second_line = "18," + ",".join(open_targets) + "\n"
        lines[1] = new_second_line
        print("ZB10 文件第二行已更新：", new_second_line.strip())
    else:
        lines[1] = "\n"
        print("第十-1段未扫描到开放端口，已清空 ZB10 第二行")

    with open(ZB_FILE_10, "w", encoding="utf-8") as f:
        f.writelines(lines)

# 新增：ZB11文件第一行更新函数，逻辑与第一行更新完全对齐
def update_zb_file_eleventh(open_targets):
    """
    第一行格式：
    88,IP:PORT,IP:PORT
    如果没有开放端口：lines[1] 清空
    """
    try:
        with open(ZB_FILE_11, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = ["\n","\n"]  # 文件不存在时创建两个空行


    if open_targets:
        new_first_line = "88," + ",".join(open_targets) + "\n"
        lines[0] = new_first_line
        print("ZB11 文件第一行已更新：", new_first_line.strip())
    else:
        lines[0] = "\n"
        print("第十一段未扫描到开放端口，已清空 ZB11 第一行")

    with open(ZB_FILE_11, "w", encoding="utf-8") as f:
        f.writelines(lines)

def update_zb_file_eleventh_1(open_targets):
    """
    第二行格式：
    87,IP:PORT,IP:PORT
    如果没有开放端口：lines[1] 清空
    """
    try:
        with open(ZB_FILE_11, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = ["\n","\n"]  # 文件不存在时创建两个空行


    if open_targets:
        new_second_line = "87," + ",".join(open_targets) + "\n"
        lines[1] = new_second_line
        print("ZB11 文件第二行已更新：", new_second_line.strip())
    else:
        lines[1] = "\n"
        print("第十一-1段未扫描到开放端口，已清空 ZB11 第二行")

    with open(ZB_FILE_11, "w", encoding="utf-8") as f:
        f.writelines(lines)

# -------------------------- 新增合并函数 --------------------------
def merge_zb_files(custom_separators=None):
    """
    合并所有ZB_FILE_1~11到ZB_FILE，每个文件上方插入独立自定义分隔符
    :param custom_separators: 自定义分隔符列表，按顺序对应：
        [ZB_FILE_1上方的分隔符, ZB_FILE_1和2之间的分隔符, ZB_FILE_2和3之间的分隔符, ..., ZB_FILE_11下方的分隔符]
        11个文件对应12个位置的分隔符，长度随意，内容完全自由，支持空字符串（表示不加分隔符）
    """
    # 要合并的文件列表，按你需要的顺序排列即可
    target_files = [ZB_FILE_1, ZB_FILE_2, ZB_FILE_3, ZB_FILE_4, ZB_FILE_5, ZB_FILE_6, ZB_FILE_7, ZB_FILE_8, ZB_FILE_9, ZB_FILE_10, ZB_FILE_11]
    # target_files = [ZB_FILE_2, ZB_FILE_3, ZB_FILE_4, ZB_FILE_5]
    # 处理自定义分隔符，没传的话用默认示例，你可以直接改
    if custom_separators is None:
        custom_separators = [
            "0,ZB1\n",
            "0,ZB2\n",
            "0,ZB3\n",
            "0,ZB4\n",
            "0,ZB5\n",
            "0,ZB6\n",
            "0,ZB7\n",
            "0,ZB8\n", 
            "0,ZB9\n",
            "0,ZB10\n",
            "0,ZB11\n",
            ""
        ]
    
    # 自动补全分隔符长度，不够的补空，多的截断，避免报错
    required_sep_len = len(target_files) + 1
    if len(custom_separators) < required_sep_len:
        custom_separators += [""] * (required_sep_len - len(custom_separators))
    else:
        custom_separators = custom_separators[:required_sep_len]

    merged_content = ""
    for idx, file_path in enumerate(target_files):
        # 先插入当前文件上方的分隔符
        merged_content += custom_separators[idx]

        # 读取文件内容，自动跳过不存在的文件
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                file_content = f.read()
            merged_content += file_content
            # 自动补换行，避免内容和下一个分隔符粘连
            if not file_content.endswith("\n"):
                merged_content += "\n"
            print(f"✅ 成功读取文件：{file_path}")
        except FileNotFoundError:
            print(f"⚠️ 文件 {file_path} 不存在，已跳过该文件内容")
            # 如果希望文件不存在也保留分隔符，删掉下面的continue即可
            continue
        except Exception as e:
            print(f"❌ 读取文件 {file_path} 失败：{str(e)}，已跳过")
            continue

    # 写入合并后的文件
    try:
        with open(ZB_FILE, "w", encoding="utf-8") as f:
            f.write(merged_content)
        print(f"✅ 合并完成，已保存到 {ZB_FILE}")
    except Exception as e:
        print(f"❌ 写入合并文件失败：{str(e)}")

if __name__ == "__main__":
    # 原有第一段扫描逻辑完全保留，无任何修改
    print(f"\n开始扫描第一段 {START_IP}-{END_IP} 端口 {PORT}, {START_IP1b}-{END_IP1b} 端口 {PORT1b} ...")   
    open_targets = scan_all(ip_segments=[
    (START_IP, END_IP, PORT),
    (START_IP1b, END_IP1b, PORT1b)
    ])
    update_zb_file(open_targets)
    update_zb_file_zero(open_targets)

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
    print(f"\n开始扫描第五段 {START_IP5a}-{END_IP5a} 端口 {PORT5a}, {START_IP5b}-{END_IP5b} 端口 {PORT5b}, {START_IP5c}-{END_IP5c} 端口 {PORT5c} ...")
    open_targets5 = scan_all(ip_segments=[
    (START_IP5a, END_IP5a, PORT5a),
    (START_IP5b, END_IP5b, PORT5b),
    (START_IP5c, END_IP5c, PORT5c)
    ])
    open_targets5 = get_verified_rtp_targets(
        open_targets5,
        target_rtp_stream_addr="239.3.1.116:8000"
    )
    update_zb_file_fifth(open_targets5)

    # 新增第五-1段扫描逻辑
    print(f"\n开始扫描第五-1段 {START_IP5_1a}-{END_IP5_1a} 端口 {PORT5_1a} ...")
    open_targets5_1 = scan_all(START_IP5_1a, END_IP5_1a, PORT5_1a)
    open_targets5_1 = get_verified_rtp_targets(
        open_targets5_1,
        target_rtp_stream_addr="225.1.8.22:8002"
    )
    update_zb_file_fifth_1(open_targets5_1)

    # 新增第六段扫描逻辑
    print(f"\n开始扫描第六段 {START_IP6}-{END_IP6} 端口 {PORT6} ...")
    open_targets6 = scan_all(START_IP6, END_IP6, PORT6)
    update_zb_file_sixth(open_targets6)

    # 新增第七段扫描逻辑
    print(f"\n开始扫描第七段 {START_IP7a}-{END_IP7a} 端口 {PORT7a}, {START_IP7b}-{END_IP7b} 端口 {PORT7b}, {START_IP7c}-{END_IP7c} 端口 {PORT7c} ...")
    open_targets7 = scan_all(ip_segments=[
    (START_IP7a, END_IP7a, PORT7a),
    (START_IP7b, END_IP7b, PORT7b),
    (START_IP7c, END_IP7c, PORT7c)
    ])
    open_targets7 = get_verified_rtp_targets(
        open_targets7,
        target_rtp_stream_addr="238.1.79.42:4448"
    )
    update_zb_file_seventh(open_targets7)

    # 新增第八段扫描逻辑
    print(f"\n开始扫描第八段 {START_IP8a}-{END_IP8a} 端口 {PORT8a}, {START_IP8b}-{END_IP8b} 端口 {PORT8b} ...")
    open_targets8 = scan_all(ip_segments=[
    (START_IP8a, END_IP8a, PORT8a),
    (START_IP8b, END_IP8b, PORT8b)
    ])
    open_targets8 = get_verified_rtp_targets(
        open_targets8,
        target_rtp_stream_addr="239.200.200.15:8856"
    )
    update_zb_file_eighth(open_targets8)

    # 新增第九段扫描逻辑
    print(f"\n开始扫描第九段 {START_IP9a}-{END_IP9a} 端口 {PORT9a}, {START_IP9b}-{END_IP9b} 端口 {PORT9b} ...")
    open_targets9 = scan_all(ip_segments=[
    (START_IP9a, END_IP9a, PORT9a),
    (START_IP9b, END_IP9b, PORT9b)
    ])
    open_targets9 = get_verified_rtp_targets(
        open_targets9,
        target_rtp_stream_addr="239.254.96.66:7512"
    )
    update_zb_file_nineth(open_targets9)

    # 新增第十段扫描逻辑
    print(f"\n开始扫描第十段 {START_IP10a}-{END_IP10a} 端口 {PORT10a}, {START_IP10b}-{END_IP10b} 端口 {PORT10b}, {START_IP10c}-{END_IP10c} 端口 {PORT10c} ...")
    open_targets10 = scan_all(ip_segments=[
    (START_IP10a, END_IP10a, PORT10a),
    (START_IP10b, END_IP10b, PORT10b),
    (START_IP10c, END_IP10c, PORT10c)
    ])
    open_targets10 = get_verified_rtp_targets(
        open_targets10,
        target_rtp_stream_addr="226.0.2.237:9808"
    )
    update_zb_file_tenth(open_targets10)

    # 新增第十-1段扫描逻辑
    print(f"\n开始扫描第十-1段 {START_IP10_1a}-{END_IP10_1a} 端口 {PORT10_1a} ...")
    open_targets10_1 = scan_all(START_IP10_1a, END_IP10_1a, PORT10_1a)
    open_targets10_1 = get_verified_rtp_targets(
        open_targets10_1,
        target_rtp_stream_addr="239.1.1.4:8004"
    )
    update_zb_file_tenth_1(open_targets10_1)

    # 新增第十一段扫描逻辑
    print(f"\n开始扫描第十一段 {START_IP11a}-{END_IP11a} 端口 {PORT11a}, {START_IP11b}-{END_IP11b} 端口 {PORT11b}, {START_IP11c}-{END_IP11c} 端口 {PORT11c} ...")
    open_targets11 = scan_all(ip_segments=[
    (START_IP11a, END_IP11a, PORT11a),
    (START_IP11b, END_IP11b, PORT11b),
    (START_IP11c, END_IP11c, PORT11c)
    ])
    open_targets11 = get_verified_rtp_targets(
        open_targets11,
        target_rtp_stream_addr="239.125.2.65:4120"
    )
    update_zb_file_eleventh(open_targets11)

    # 新增第十一-1段扫描逻辑
    print(f"\n开始扫描第十一-1段 {START_IP11_1a}-{END_IP11_1a} 端口 {PORT11_1a} ...")
    open_targets11_1 = scan_all(START_IP11_1a, END_IP11_1a, PORT11_1a)
    open_targets11_1 = get_verified_rtp_targets(
        open_targets11_1,
        target_rtp_stream_addr="239.29.0.116:5000"
    )
    update_zb_file_eleventh_1(open_targets10_1)

    # 新增ZB合并逻辑
    print(f"\n开始合成ZB文件...")
    merge_zb_files()
    
