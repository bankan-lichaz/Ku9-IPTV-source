import socket
import ipaddress

ZB_FILE = "ZB"  # 你的 ZB 文件名，可改成 zb.txt 或其他

START_IP = "116.2.160.1"
END_IP = "116.2.180.255"
PORT = 4010

def expand_ip_range(start_ip, end_ip):
    start = ipaddress.IPv4Address(start_ip)
    end = ipaddress.IPv4Address(end_ip)
    return [str(ipaddress.IPv4Address(ip)) for ip in range(int(start), int(end) + 1)]

def scan_single_ip(ip, port, timeout=1):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        sock.close()
        if result == 0:
            return ip
    except:
        pass
    return None

def scan_all():
    ip_list = expand_ip_range(START_IP, END_IP)
    open_ips = []

    for ip in ip_list:
        result = scan_single_ip(ip, PORT)
        if result:
            open_ips.append(result)

    return open_ips

def update_zb_file(open_ips):
    """
    写入 ZB 文件第一行：
    格式：5,IP1|IP2|IP3
    如果 open_ips 为空，则不修改文件
    """
    try:
        with open(ZB_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = ["5,\n"]  # 如果文件不存在，创建一个默认第一行

    if open_ips:
        new_first_line = "5," + "|".join(open_ips) + "\n"
        lines[0] = new_first_line

        with open(ZB_FILE, "w", encoding="utf-8") as f:
            f.writelines(lines)

        print("ZB 文件已更新：", new_first_line.strip())
    else:
        print("未扫描到开放端口，ZB 文件保持不变")

if __name__ == "__main__":
    print("开始扫描端口 4010 ...")
    open_ips = scan_all()
    update_zb_file(open_ips)
