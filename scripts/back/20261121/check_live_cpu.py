import paramiko

def check_live_cpu():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=10)

    print("=== LIVE CPU CON 2 MUESTRAS (1 SEG INTERVALO) ===")
    cmd = "top -b -n 2 -d 1 | tail -n 20"
    _, stdout, _ = ssh.exec_command(cmd)
    print(stdout.read().decode('utf-8'))

    print("=== TIEMPOS DE RESPUESTA HTTP EXTERNOS (DESDE LOCAL O CURL) ===")
    cmd_curl = "curl -o /dev/null -s -w 'Time connect: %{time_connect}s | Time TTFB: %{time_starttransfer}s | Total: %{time_total}s\\n' http://127.0.0.1:80/web/login"
    _, stdout, _ = ssh.exec_command(cmd_curl)
    print(stdout.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    check_live_cpu()
