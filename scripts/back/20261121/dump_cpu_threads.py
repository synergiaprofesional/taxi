import paramiko

def dump_python_stack():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=15)

    # Dump python stack with gdb if installed, or check strace of 2330 specifically
    cmd = "timeout 4 strace -p 2330 -s 200 2>&1"
    _, stdout, _ = ssh.exec_command(cmd)
    print("--- STRACE THREAD 2330 (4s) ---")
    print(stdout.read().decode('utf-8'))

    cmd2 = "timeout 4 strace -p 2331 -s 200 2>&1"
    _, stdout2, _ = ssh.exec_command(cmd2)
    print("--- STRACE THREAD 2331 (4s) ---")
    print(stdout2.read().decode('utf-8'))

    # Let's check with gdb if available
    cmd3 = "gdb -p 2305 -batch -ex 'thread apply all bt 5' 2>&1 | head -n 40 || echo 'gdb no disponible'"
    _, stdout3, _ = ssh.exec_command(cmd3)
    print("--- GDB BACKTRACE ---")
    print(stdout3.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    dump_python_stack()
