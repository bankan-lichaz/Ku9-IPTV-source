#!/usr/bin/env python3
"""
端口扫描工具：扫描输入的IP:PORT列表，返回可连接的合法列表
输出格式：逗号分隔的有效IP:PORT字符串
"""
import os
import sys
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

def scan_single_port(ipport: str, timeout: int) -> str | None:
    """扫描单个IP:端口，有效返回原ipport，无效返回None"""
    ipport = ipport.strip()
    if not ipport:
        return None
    
    # 拆分IP和端口，兼容IPv4/IPv6（用最后一个冒号分割，避免IPv6多冒号问题）
    try:
        ip_part, port_part = ipport.rsplit(':', 1)
        port = int(port_part)
    except ValueError:
        print(f"⚠️ 跳过格式错误的IP:PORT：{ipport}", file=sys.stderr)
        return None
    
    # 处理IPv6地址的中括号格式
    ip = ip_part.strip()
    if ip.startswith('[') and ip.endswith(']'):
        ip = ip[1:-1]
    
    # TCP端口扫描
    try:
        # 自动识别IPv4/IPv6协议族
        family = socket.AF_INET6 if ':' in ip else socket.AF_INET
        with socket.socket(family, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            # connect_ex返回0表示端口开放
            if s.connect_ex((ip, port)) == 0:
                print(f"✅ 有效：{ip}:{port}", file=sys.stderr)
                return ipport
            else:
                print(f"❌ 无效：{ip}:{port}", file=sys.stderr)
                return None
    except Exception as e:
        print(f"⚠️ 扫描 {ip}:{port} 出错：{str(e)}", file=sys.stderr)
        return None

def main():
    # 读取配置：优先读命令行参数，其次读环境变量
    input_ipports = sys.argv[1] if len(sys.argv) > 1 else os.environ.get('IPPORTS', '')
    scan_timeout = int(os.environ.get('SCAN_TIMEOUT', 2))  # 默认超时2秒
    max_threads = int(os.environ.get('MAX_WORKERS', 20))   # 默认20线程并发
    
    # 空输入直接返回空
    if not input_ipports.strip():
        print("")
        return
    
    # 处理输入列表
    ipport_list = [x.strip() for x in input_ipports.split(',') if x.strip()]
    valid_list = []

    # 多线程扫描提升速度
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = {executor.submit(scan_single_port, ipport, scan_timeout): ipport for ipport in ipport_list}
        for future in as_completed(futures):
            res = future.result()
            if res:
                valid_list.append(res)
    
    # 输出逗号分隔的有效列表
    print(','.join(valid_list))

if __name__ == "__main__":
    main()
