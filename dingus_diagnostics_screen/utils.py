import subprocess


def get_comp_stats():
    cmd = "hostname -I | cut -d' ' -f1"
    ip = "IP: " + subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = 'cut -f 1 -d " " /proc/loadavg'
    cpu = "CPU: " + subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%s MB %.2f%%\", $3,$2,$3*100/$2 }'"
    mem = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = 'df -h | awk \'$NF=="/"{printf "Disk: %d/%d GB %s", $3,$2,$5}\''
    disk = subprocess.check_output(cmd, shell=True).decode("utf-8")

    return [ip, cpu, mem, disk]
