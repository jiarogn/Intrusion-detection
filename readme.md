# 网卡流量分析工具

此Python工具用于分析和监控网络接口的流量信息。它包括获取网卡名称和MAC地址、统计网络流量速率、格式化流量速率和时间戳等功能。

## 函数列表
- `get_netcard_name()`
- `get_nic_list()`
- `get_net_flow(net_card)`
- `change_format(count)`
- `get_rate(net_card)`
- `get_formal_rate(info)`
- `time_to_formal(time_stamp)`

### 函数详细说明

#### get_netcard_name()
 获取网卡MAC地址和网卡名字的对应字典。\
 例如：{'9C-B6-D0-0E-70-D9': 'WLAN'}

    :return: 包含网卡MAC地址和名字的字典

#### get_nic_list()
获取系统信息和网卡列表或字典：\
    - 在Linux系统中返回网卡名字列表\
    - 在Windows系统中返回网卡名字和NIC信息的字典

    :return: (系统信息, 网卡字典或列表)

#### get_net_flow(net_card)
获取指定网卡的流量发送和接收信息

    :param net_card: 网卡名字
    :return: 包含接收字节数、发送字节数、接收数据包数、发送数据包数的元组

#### change_format(count)
将字节数转换为适当的单位格式（B/s, KB/s, MB/s, GB/s）。

    :param count: 字节数
    :return: 格式化后的字符串

#### get_rate(net_card)
统计每秒接收和发送的数据大小。

    :param net_card: 网卡名字
    :return: 包含每秒接收和发送的字节数、接收和发送的数据包数的列表

#### get_formal_rate(info)
获取格式化的每秒速率信息。

    :param info: 包含接收字节数、发送字节数、接收包数、发送包数的列表
    :return: 格式化后的速率信息

#### time_to_formal(time_stamp)
将时间戳转换为标准的时间字符串。\
例如：2018-10-21 20:27:53.123456

    :param time_stamp: 时间戳，单位为秒
    :return: 格式化后的时间字符串