import socket
import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed

ZB_FILE = "ZB"

START_IP = "116.2.160.1"
END_IP = "116.2.180.255"
PORT = 4010

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

def scan_all():
    ip_list = expand_ip_range(START_IP, END_IP)
    open_targets = []

    print(f"总扫描 IP 数量：{len(ip_list)}")

    with ThreadPoolExecutor(max_workers=1000) as executor:
        futures = {executor.submit(scan_single_ip, ip, PORT): ip for ip in ip_list}

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

def update_zb_file(open_targets):
    """
    第一行格式：
    5,IP:PORT,IP:PORT,IP:PORT
    如果只有一个：5,IP:PORT
    如果没有开放端口：保持原样
    """
    try:
        with open(ZB_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = ["5,\n"]

    if open_targets:
        # 不加末尾逗号
        new_first_line = "5," + ",".join(open_targets) + "\n"
        lines[0] = new_first_line

        with open(ZB_FILE, "w", encoding="utf-8") as f:
            f.writelines(lines)

        print("ZB 文件已更新：", new_first_line.strip())
    else:
        print("未扫描到开放端口，ZB 文件保持不变")

if __name__ == "__main__":
    print("开始扫描端口 4010 ...")
    open_targets = scan_all()
    update_zb_file(open_targets)
