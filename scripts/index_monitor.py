import psutil
import requests


# monitor api
cpu_monitor_api = 'http://127.0.0.1/api/monitor/monitor-cpu'
memory_monitor_api = 'http://127.0.0.1/api/monitor/monitor-memory'
disk_monitor_api = 'http://127.0.0.1/api/monitor/monitor-disk'


# hostname
hostname = 'cmdb'


# timeout
time_out = 3


# cpu 使用率
cpu = (str)(psutil.cpu_percent(1))
requests.post(cpu_monitor_api, data={"usage_rate": cpu,"host": hostname}, timeout=time_out)


# memory 使用率
free = str(round(psutil.virtual_memory().free/(1024.0*1024.0*1024.0), 2))
total = str(round(psutil.virtual_memory().total/(1024.0*1024.0*1024.0), 2))
usage = str(round((psutil.virtual_memory().total-psutil.virtual_memory().free)/(1024.0*1024.0*1024.0), 2))
memory = int(psutil.virtual_memory().total-psutil.virtual_memory().free)/float(psutil.virtual_memory().total)
requests.post(memory_monitor_api, data={"usage": usage, "free": free, "host": hostname}, timeout=time_out)


# disk 使用率
# io = psutil.disk_partitions()
o = psutil.disk_usage('/')
usage = str(round(o.used/(1024.0*1024.0*1024.0), 1))
free = str(round(o.free/(1024.0*1024.0*1024.0), 1))
requests.post(disk_monitor_api, data={"usage": usage, "free": free, "host": hostname}, timeout=time_out)

