import socket
import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed

HT_FILE = "HT"
HT_FILE_WSJK= "WSJK"

# 原有第一段扫描配置（完全保留，未修改）
START_IP = "39.150.102.1"
END_IP = "39.150.102.255"
PORT = 19901

# 新增第二段扫描配置
START_IP2 = "139.214.177.1"
END_IP2 = "139.214.183.255"
PORT2 = 9901

# 新增第三段扫描配置
START_IP3 = "60.187.244.1"
END_IP3 = "60.187.247.255"
PORT3 = 9901

# 新增第四段扫描配置
START_IP4 = "123.175.209.1"
END_IP4 = "123.175.209.255"
PORT4 = 9003

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
def scan_all(start_ip=START_IP, end_ip=END_IP, port=PORT):
    ip_list = expand_ip_range(start_ip, end_ip)
    open_targets = []

    print(f"总扫描 IP 数量：{len(ip_list)}")

    with ThreadPoolExecutor(max_workers=1000) as executor:
        futures = {executor.submit(scan_single_ip, ip, port): ip for ip in ip_list}

        for i, future in enumerate(as_completed(futures)):
            ip = futures[future]
            try:
                result = future.result()
                if result:
                    open_targets.append(result)
                    print(f"开放：{result}")
            except:
                pass

            if i % 200 == 0:
                print(f"进度：{i}/{len(ip_list)}")

    return open_targets

# 原有HT文件第一行更新函数完全保留，未修改任何逻辑
def update_ht_file(open_targets):
    """
    第一行格式：
    64,IP:PORT,IP:PORT
    如果没有开放端口：lines[0] 清空
    """
    try:
        with open(HT_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = ["\n"]  # 文件不存在时创建一个空行

    if open_targets:
        # 有开放端口 → 写入 64,IP:PORT...
        new_first_line = "64," + ",".join(open_targets) + "\n"
        lines[0] = new_first_line
        print("HT 文件已更新：", new_first_line.strip())
    else:
        # ⭐ 没有开放端口 → 第一行清空
        lines[0] = "\n"
        print("未扫描到开放端口，已清空 HT 第一行")

    with open(HT_FILE, "w", encoding="utf-8") as f:
        f.writelines(lines)

# 新增：HT文件第二行更新函数，逻辑与第一行更新完全对齐
def update_ht_file_second(open_targets):
    """
    第二行格式：
    65,IP:PORT,IP:PORT
    如果没有开放端口：lines[1] 清空
    """
    try:
        with open(HT_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = ["\n", "\n"]  # 文件不存在时创建两行空行

    # 确保文件至少有2行，避免索引越界
    while len(lines) < 2:
        lines.append("\n")

    if open_targets:
        new_second_line = "65," + ",".join(open_targets) + "\n"
        lines[1] = new_second_line
        print("HT 文件第二行已更新：", new_second_line.strip())
    else:
        lines[1] = "\n"
        print("第二段未扫描到开放端口，已清空 HT 第二行")

    with open(HT_FILE, "w", encoding="utf-8") as f:
        f.writelines(lines)

# 新增:WSJK文件第一行更新函数
def update_ht_file_wsjk_first(open_targets):
    """
    第一行格式：
    68,IP:PORT,IP:PORT
    如果没有开放端口：lines[0] 清空
    """
    try:
        with open(HT_FILE_WSJK, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = ["\n"]  # 文件不存在时创建一个空行

    if open_targets:
        # 有开放端口 → 写入 68,IP:PORT...
        new_first_line = "68," + ",".join(open_targets) + "\n"
        lines[0] = new_first_line
        print("WSJK 文件已更新：", new_first_line.strip())
    else:
        # ⭐ 没有开放端口 → 第一行清空
        lines[0] = "\n"
        print("未扫描到开放端口，已清空 WSJK 第一行")

    with open(HT_FILE_WSJK, "w", encoding="utf-8") as f:
        f.writelines(lines)

# 新增：HT文件第三行更新函数，逻辑与第二行更新完全对齐
def update_ht_file_third(open_targets):
    """
    第二行格式：
    66,IP:PORT,IP:PORT
    如果没有开放端口：lines[2] 清空
    """
    try:
        with open(HT_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = ["\n", "\n","\n"]  # 文件不存在时创建三行空行

    # 确保文件至少有3行，避免索引越界
    while len(lines) < 3:
        lines.append("\n")

    if open_targets:
        new_third_line = "66," + ",".join(open_targets) + "\n"
        lines[2] = new_third_line
        print("HT 文件第三行已更新：", new_third_line.strip())
    else:
        lines[2] = "\n"
        print("第三段未扫描到开放端口，已清空 HT 第三行")

    with open(HT_FILE, "w", encoding="utf-8") as f:
        f.writelines(lines)

# 新增：HT文件第四行更新函数，逻辑与第三行更新完全对齐
def update_ht_file_forth(open_targets):
    """
    第二行格式：
    67,IP:PORT,IP:PORT
    如果没有开放端口：lines[3] 清空
    """
    try:
        with open(HT_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = ["\n", "\n","\n","\n"]  # 文件不存在时创建四行空行

    # 确保文件至少有4行，避免索引越界
    while len(lines) < 4:
        lines.append("\n")

    if open_targets:
        new_forth_line = "67," + ",".join(open_targets) + "\n"
        lines[3] = new_forth_line
        print("HT 文件第四行已更新：", new_forth_line.strip())
    else:
        lines[3] = "\n"
        print("第四段未扫描到开放端口，已清空 HT 第四行")

    with open(HT_FILE, "w", encoding="utf-8") as f:
        f.writelines(lines)

if __name__ == "__main__":
    # 原有第一段扫描逻辑完全保留，无任何修改
    print(f"\n开始扫描第一段 {START_IP}-{END_IP} 端口 {PORT} ...")   
    open_targets = scan_all()
    update_ht_file(open_targets)

    # 新增第二段扫描逻辑
    print(f"\n开始扫描第二段 {START_IP2}-{END_IP2} 端口 {PORT2} ...")
    open_targets2 = scan_all(START_IP2, END_IP2, PORT2)
    update_ht_file_second(open_targets2)
    update_ht_file_wsjk_first(open_targets2)

    # 新增第三段扫描逻辑
    print(f"\n开始扫描第三段 {START_IP3}-{END_IP3} 端口 {PORT3} ...")
    open_targets3 = scan_all(START_IP3, END_IP3, PORT3)
    update_ht_file_third(open_targets3)

    # 新增第四段扫描逻辑
    print(f"\n开始扫描第四段 {START_IP4}-{END_IP4} 端口 {PORT4} ...")
    open_targets4 = scan_all(START_IP4, END_IP4, PORT4)
    update_ht_file_forth(open_targets4)
