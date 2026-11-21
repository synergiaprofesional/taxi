import paramiko

def inspect_pid_threads():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=10)

    # 1. Hilos del proceso 2305 y consumo de CPU por hilo
    cmd = "top -H -b -n 1 -p 2305 | head -n 25"
    _, stdout, _ = ssh.exec_command(cmd)
    print("--- TOP HILOS PID 2305 ---")
    print(stdout.read().decode('utf-8'))

    # 2. Strace de 3 segundos sobre el proceso 2305
    cmd2 = "timeout 3 strace -c -p 2305 2>&1"
    _, stdout2, _ = ssh.exec_command(cmd2)
    print("--- STRACE SUMMARY 3s ---")
    print(stdout2.read().decode('utf-8'))

    # 3. Que archivos/sockets tiene abiertos el PID 2305
    cmd3 = "lsof -p 2305 | grep -E '(ESTABLISHED|TCP|REG)' | head -n 25"
    _, stdout3, _ = ssh.exec_command(cmd3)
    print("--- LSOF PID 2305 ---")
    print(stdout3.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    inspect_pid_threads()
