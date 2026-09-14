import socket
import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Union, Dict, Any

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

START_IP5b = "114.254.30.1"
END_IP5b = "114.254.40.255"
PORT5b = 8888

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
def filter_valid_status(
    open_targets: List[Union[str, Dict[str, Any]]],
    # 输入格式兼容参数
    result_format: str = "str",  # 输入结果类型：str=原始是"IP:PORT"字符串，dict=原始是包含ip/port的字典
    ip_key: str = "ip",          # dict格式时IP对应的字段名
    port_key: str = "port",      # dict格式时端口对应的字段名
    # 请求配置参数
    path: str = "/status",       # 要访问的接口路径
    use_https: bool = False,     # 是否用HTTPS访问
    timeout: int = 5,            # 单次请求超时时间（秒）
    max_workers: int = 100,      # 并发线程数，避免触发目标限流
    # 过滤规则参数
    exclude_json: Dict[str, str] = {"detail": "Not Found"},  # 匹配到这个JSON就过滤删除
    ignore_case: bool = False,   # 匹配JSON时是否忽略大小写
    exclude_on_error: bool = False, # 请求失败（超时/连接错误等）是否也过滤，默认保留
    # 功能开关
    deduplicate: bool = True,    # 是否按IP:端口去重，避免重复请求
    debug: bool = False          # 是否打印过滤原因的调试信息
) -> List[Union[str, Dict[str, Any]]]:
    """
    过滤scan_all返回的结果：仅保留访问/status接口响应不等于{"detail":"Not Found"}的目标
    返回格式和输入open_targets完全一致，保留原始所有字段
    """
    # 空输入直接返回
    if not open_targets:
        print("输入的开放目标列表为空，无需过滤")
        return []

    # -------------------------- 第一步：解析输入结果，提取IP:Port对，保留原始条目 --------------------------
    parsed_pairs = []  # 存储 (原始结果项, IP, 端口) 元组，保证返回和输入格式完全一致
    seen = set()       # 用于去重

    for item in open_targets:
        # 解析IP和端口
        if result_format == "str":
            # 兼容IPv4/IPv6：从右往左找最后一个冒号拆分端口，避免IPv6多冒号解析错误
            last_colon = item.rfind(":")
            if last_colon == -1:
                if debug: print(f"跳过格式错误条目：{item}，无法解析端口")
                continue
            ip = item[:last_colon]
            port_str = item[last_colon+1:]
            if not port_str.isdigit():
                if debug: print(f"跳过端口非法条目：{item}")
                continue
            port = int(port_str)
        
        elif result_format == "dict":
            ip = item.get(ip_key, "")
            port = item.get(port_key, "")
            if not ip or not port:
                if debug: print(f"跳过缺少IP/端口的字典条目：{item}")
                continue
            port = int(port)
        
        else:
            raise ValueError(f"不支持的result_format：{result_format}，可选值为'str'或'dict'")
        
        # 去重逻辑
        if deduplicate:
            pair_key = (ip, port)
            if pair_key in seen:
                if debug: print(f"跳过重复条目：{ip}:{port}")
                continue
            seen.add(pair_key)
        
        parsed_pairs.append( (item, ip, port) )
    
    total = len(parsed_pairs)
    if total == 0:
        print("解析后无有效待校验条目")
        return []
    
    print(f"共有 {total} 个IP:端口需要校验/status接口...")
    valid_results = []

    # -------------------------- 辅助函数：构造URL，自动兼容IPv6 --------------------------
    def build_url(ip: str, port: int) -> str:
        scheme = "https" if use_https else "http"
        # IPv6地址需要加方括号包裹，避免URL解析错误
        if ":" in ip:
            return f"{scheme}://[{ip}]:{port}{path}"
        else:
            return f"{scheme}://{ip}:{port}{path}"

    # -------------------------- 第二步：单个目标校验逻辑 --------------------------
    def check_single(item: Union[str, Dict], ip: str, port: int):
        url = build_url(ip, port)
        try:
            resp = requests.get(url, timeout=timeout)
            # 尝试解析为JSON
            try:
                resp.encoding = resp.apparent_encoding
                resp_json = resp.json()
            except requests.exceptions.JSONDecodeError:
                # 响应不是合法JSON，保留
                return item
            
            # 处理大小写匹配
            target_json = exclude_json.copy()
            current_json = resp_json.copy()
            if ignore_case:
                # 键和值都转小写比较
                target_json = {k.lower(): v.lower() if isinstance(v, str) else v for k, v in target_json.items()}
                current_json = {k.lower(): v.lower() if isinstance(v, str) else v for k, v in current_json.items()}
            
            # 精确匹配到要排除的JSON，过滤掉
            if current_json == target_json:
                if debug:
                    print(f"过滤 {url}：响应匹配到排除规则 {exclude_json}")
                return None
        
        except Exception as e:
            # 请求异常处理
            if exclude_on_error:
                if debug:
                    print(f"过滤 {url}：请求失败 {type(e).__name__}: {str(e)}")
                return None
            else:
                # 默认保留请求失败的目标
                return item
        
        # 其他所有情况都保留
        return item

    # -------------------------- 第三步：并发执行，收集结果 --------------------------
    max_workers = min(max_workers, total)  # 避免任务少时开过多线程浪费资源
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(check_single, item, ip, port): (item, ip, port)
            for (item, ip, port) in parsed_pairs
        }
        completed = 0
        for future in as_completed(futures):
            res = future.result()
            if res is not None:
                valid_results.append(res)
            completed += 1
            # 进度提示，和scan_all风格一致
            if completed % 100 == 0 or completed == total:
                print(f"校验进度：{completed}/{total}，剩余合格目标 {len(valid_results)} 个")
    
    print(f"过滤完成，共保留 {len(valid_results)}/{total} 个合格目标")
    return valid_results

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
    (START_IP5b, END_IP5b, PORT5b)
    ])
    open_targets5 = filter_valid_status(open_targets5)
    update_zb_file_fifth(open_targets5)

    # 新增第六段扫描逻辑
    print(f"\n开始扫描第六段 {START_IP6}-{END_IP6} 端口 {PORT6} ...")
    open_targets6 = scan_all(START_IP6, END_IP6, PORT6)
    update_zb_file_sixth(open_targets6)
