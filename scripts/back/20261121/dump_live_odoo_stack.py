import paramiko

def dump_python_stack():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('fundetaxcol.co', username='root', password='2QoRhncZ', timeout=10)

    print("=== STRACE DE 15444 (2 SEGUNDOS) ===")
    cmd = "timeout 2 strace -p 15444 -f -c 2>&1"
    _, stdout, _ = ssh.exec_command(cmd)
    print(stdout.read().decode('utf-8'))

    print("=== DUMP CON GDB DEL PYTHON CALL STACK ===")
    # Con gdb podemos ejecutar py-bt si python3-dbg o gdb está disponible
    cmd_gdb = "gdb -p 15444 -batch -ex 'thread apply all bt' 2>/dev/null | head -n 45"
    _, stdout2, _ = ssh.exec_command(cmd_gdb)
    print(stdout2.read().decode('utf-8'))

    ssh.close()

if __name__ == '__main__':
    dump_python_stack()
