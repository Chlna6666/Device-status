import os
import time
import psutil
import json
import datetime
import pynvml
import socket

keys = '114514'

pynvml.nvmlInit()
handle = pynvml.nvmlDeviceGetHandleByIndex(0)  # 指定显卡号

def get_status():
    # CPU逻辑数量
    cpu_thread = psutil.cpu_count(logical=True)

    # CPU物理核心
    cpu_count = psutil.cpu_count(logical=False)

    # CPU使用率
    cpu_percent = psutil.cpu_percent()

    # CPU温度///

    # 总内存
    memory_total = round(psutil.virtual_memory().total / 1024 / 1024 / 1024, 2)

    # 已用内存
    memory_used = round(psutil.virtual_memory().used / 1024 / 1024 / 1024, 2)

    # 空闲内存
    memory_free = round(psutil.virtual_memory().free / 1024 / 1024 / 1024, 2)

    # 使用内存占比
    memory_percent = psutil.virtual_memory().percent

    # 总交换内存
    swap_total = round(psutil.swap_memory().total / 1024 / 1024 / 1024, 2)

    # 已用交换内存
    swap_used = round(psutil.swap_memory().used / 1024 / 1024 / 1024, 2)

    # 空闲交换内存
    swap_free = round(psutil.swap_memory().free / 1024 / 1024 / 1024, 2)

    # 使用交换内存占比
    swap_percent = psutil.swap_memory().percent

    sent_before = psutil.net_io_counters().bytes_sent  # 已发送的流量
    recv_before = psutil.net_io_counters().bytes_recv  # 已接收的流量
    time.sleep(1)
    sent_now = psutil.net_io_counters().bytes_sent
    recv_now = psutil.net_io_counters().bytes_recv
    sent = (sent_now - sent_before) / 1024  # 算出1秒后的差值
    recv = (recv_now - recv_before) / 1024

    # 启动时间
    start_time = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")

    gpu_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
    # GPU总的显存
    gpu_total = round(gpu_info.total / (1024 ** 3), 2)

    # GPU已用显存
    gpu_used = round(gpu_info.used / (1024 ** 3), 2)

    # GPU剩余显存
    gpu_free = round(gpu_info.free / (1024 ** 3), 2)

    # GPU温度
    gpu_temperature = pynvml.nvmlDeviceGetTemperature(handle, 0)

    # GPU风扇速率
    gpu_fanSpeed = pynvml.nvmlDeviceGetFanSpeed(handle)

    # GPU供电状态
    gpu_powerState = pynvml.nvmlDeviceGetPowerState(handle)

    # GPU利用率
    gpu_utilRate = pynvml.nvmlDeviceGetUtilizationRates(handle).gpu

    # GPU显存利用率
    gpu_memoryRate = pynvml.nvmlDeviceGetUtilizationRates(handle).memory

    result = {
        "status": "200",
        "data": {
            "cpu_thread": cpu_thread,
            "cpu_count": cpu_count,
            "cpu_percent": cpu_percent,
            "memory_total": memory_total,
            "memory_used": memory_used,
            "memory_free": memory_free,
            "memory_percent": memory_percent,
            "swap_total": swap_total,
            "swap_used": swap_used,
            "swap_free": swap_free,
            "swap_percent": swap_percent,
            "network_sent": round(sent, 2),
            "network_recv": round(recv, 2),
            "start_time": start_time,
            "gpu_total": gpu_total,
            "gpu_used": gpu_used,
            "gpu_free": gpu_free,
            "gpu_temperature": gpu_temperature,
            "gpu_fanSpeed": gpu_fanSpeed,
            "gpu_powerState": gpu_powerState,
            "gpu_utilRate": gpu_utilRate,
            "gpu_memoryRate": gpu_memoryRate,
        }
    }
    return result

def send_response(data, address):
    response = json.dumps(data).encode('utf-8')
    sock.sendto(response, address)

def handle_request(data, address):
    key = data.get("key")
    if key == keys:
        status = get_status()
        send_response(status, address)
    else:
        response = {
            "status": "404"
        }
        send_response(response, address)

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', 8080))
    print("Server started and listening on port 8080")

    while True:
        data, address = sock.recvfrom(1024)
        data = json.loads(data.decode('utf-8'))
        handle_request(data, address)
