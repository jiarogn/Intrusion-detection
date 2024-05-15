# -*- coding: utf-8 -*-
"""
工具集
可获取网卡列表, 某个网卡的下载速度上传速度等
"""

import time
import psutil
from platform import system

def get_netcard_name():
    """
    获取网卡MAC地址和网卡名字的对应字典。
    例如：{'9C-B6-D0-0E-70-D9': 'WLAN'}

    :return: 包含网卡MAC地址和名字的字典
    """
    # 创建一个空字典用于存储网卡信息
    netcard_info = {}

    # 获取所有网络接口的信息
    interfaces = psutil.net_if_addrs()

    # 遍历所有接口
    for interface, addrs in interfaces.items():
        # 遍历每个接口的地址信息
        for addr in addrs:
            # 如果地址类型为AF_LINK（即MAC地址），则将其添加到字典中
            if addr.family == psutil.AF_LINK:
                netcard_info[addr.address] = interface

    # 返回包含网卡信息的字典
    return netcard_info

def get_nic_list():
    """
    获取系统信息和网卡列表或字典：
    - 在Linux系统中返回网卡名字列表
    - 在Windows系统中返回网卡名字和NIC信息的字典

    :return: (系统信息, 网卡字典或列表)
    """
    # 获取当前操作系统的名字
    system_name = system()

    # 获取网卡MAC地址和名字的对应字典
    netcard_name = get_netcard_name()

    def process_windows_nic(wmi_obj, netcard_name):
        """
        处理Windows系统的网卡信息，匹配MAC地址和网卡名字，并返回对应字典

        :param wmi_obj: WMI对象
        :param netcard_name: 网卡MAC地址和名字的对应字典
        :return: 包含网卡名字和NIC信息的字典
        """
        data = {}
        for nic in wmi_obj.Win32_NetworkAdapterConfiguration():
            if nic.MACAddress:
                # 格式化MAC地址，替换冒号为短横线
                mac_address = nic.MACAddress.replace(':', '-')
                # 检查MAC地址是否在字典中
                if mac_address in netcard_name:
                    # 获取网卡名字
                    net_card_name = netcard_name[mac_address]
                    # 获取NIC信息，并截取前11个字符之后的部分
                    nic_name = nic.Caption[11:]
                    # 将网卡名字和NIC信息添加到字典中
                    data[net_card_name] = nic_name
        return data

    # 根据操作系统类型返回相应的网卡信息
    if system_name == "Windows":
        import wmi
        # 创建WMI对象
        wmi_obj = wmi.WMI()
        # 返回系统信息和处理后的网卡信息字典
        return system_name, process_windows_nic(wmi_obj, netcard_name)
    elif system_name == "Linux":
        # 返回系统信息和网卡名字列表
        return system_name, list(netcard_name.values())
    else:
        return None

def get_net_flow(net_card):
    """
    获取指定网卡的流量发送和接收信息

    :param net_card: 网卡名字
    :return: 包含接收字节数、发送字节数、接收数据包数、发送数据包数的元组
    """
    # 获取指定网卡的流量统计信息
    net_info = psutil.net_io_counters(pernic=True).get(net_card)

    # 检查是否成功获取网卡信息
    if net_info:
        # 返回接收字节数、发送字节数、接收数据包数、发送数据包数
        return net_info.bytes_recv, net_info.bytes_sent, net_info.packets_recv, net_info.packets_sent
    else:
        # 如果未找到对应网卡信息，返回0值元组
        return 0, 0, 0, 0

def change_format(count):
    """
    将字节数转换为适当的单位格式（B/s, KB/s, MB/s, GB/s）。

    :param count: 字节数
    :return: 格式化后的字符串
    """
    if count < 1024:
        return "%.2f B/s" % count
    elif count < 1048576:
        return "%.2f KB/s" % (count / 1024)
    elif count < 1073741824:
        return "%.2f MB/s" % (count / 1048576)
    else:
        return "%.2f GB/s" % (count / 1073741824)

def get_rate(net_card):
    """
    统计每秒接收和发送的数据大小。

    :param net_card: 网卡名字
    :return: 包含每秒接收和发送的字节数、接收和发送的数据包数的列表
    """
    # 初始化网卡列表和数据计数
    net_cards = []
    old_data = [0, 0, 0, 0]
    new_data = [0, 0, 0, 0]

    # 获取所有网卡的名字，如果net_card为None
    if net_card is None:
        net_cards = psutil.net_io_counters(pernic=True).keys()
    else:
        net_cards.append(net_card)

    # 记录当前的流量数据
    for card in net_cards:
        info = get_net_flow(card)
        for i in range(4):
            old_data[i] += info[i]

    # 等待1秒钟
    time.sleep(1)

    # 记录1秒后的流量数据
    for card in net_cards:
        info = get_net_flow(card)
        for i in range(4):
            new_data[i] += info[i]

    # 计算每秒的流量数据
    info = [new_data[i] - old_data[i] for i in range(4)]
    return info

def get_formal_rate(info):
    """
    获取格式化的每秒速率信息。

    :param info: 包含接收字节数、发送字节数、接收包数、发送包数的列表
    :return: 格式化后的速率信息
    """
    recv_bytes = change_format(info[0])  # 每秒接收的字节数
    sent_bytes = change_format(info[1])  # 每秒发送的字节数
    recv_pak = f"{info[2]} pak/s"  # 每秒接收的数据包数
    sent_pak = f"{info[3]} pak/s"  # 每秒发送的数据包数
    return recv_bytes, sent_bytes, recv_pak, sent_pak

def time_to_formal(time_stamp):
    """
    将时间戳转换为标准的时间字符串。
    例如：2018-10-21 20:27:53.123456

    :param time_stamp: 时间戳，单位为秒
    :return: 格式化后的时间字符串
    """
    # 获取时间戳的小数部分
    delta_ms = str(time_stamp - int(time_stamp))
    # 将时间戳转换为时间元组
    time_temp = time.localtime(time_stamp)
    # 格式化时间字符串
    my_time = time.strftime("%Y-%m-%d %H:%M:%S", time_temp)
    # 添加毫秒部分
    my_time += delta_ms[1:8]
    return my_time