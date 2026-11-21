import subprocess
import os

def test_print():
    # ESC/POS Commands:
    # ESC @: Initialize printer: \x1b\x40
    # ESC a 1: Center align: \x1b\x61\x01
    # Double height/width text for Title: \x1d\x21\x11
    # Normal text: \x1d\x21\x00
    # Line feeds: \x0a
    # GS V 66 0: Partial Cut with feed: \x1d\x56\x42\x00
    
    bytes_data = bytearray()
    bytes_data.extend(b'\x1b\x40') # Init
    bytes_data.extend(b'\x1b\x61\x01') # Center
    bytes_data.extend(b'\x1b\x45\x01') # Bold ON
    bytes_data.extend(b'FUNDETAXCOL\n')
    bytes_data.extend(b'SYNERGIA MOVIL\n')
    bytes_data.extend(b'\x1b\x45\x00') # Bold OFF
    bytes_data.extend(b'PRUEBA DE IMPRESION DIRECTA\n')
    bytes_data.extend(b'--------------------------------\n')
    bytes_data.extend(b'\x1b\x61\x00') # Align Left
    bytes_data.extend(b'Impresora: TIQUETES (USB001)\n')
    bytes_data.extend(b'Estado:    CONECTADA Y NORMAL\n')
    bytes_data.extend(b'Placa:     WGN121\n')
    bytes_data.extend(b'Conductor: CARLOS RAMIREZ\n')
    bytes_data.extend(b'Bahia:     BAHIA 29D\n')
    bytes_data.extend(b'Turno:     #125\n')
    bytes_data.extend(b'--------------------------------\n')
    bytes_data.extend(b'\x1b\x61\x01') # Center
    bytes_data.extend(b'*** IMPRESION EXITOSA ***\n\n\n\n')
    bytes_data.extend(b'\x1d\x56\x42\x00') # Cut

    test_bin = r"C:\Workspaces\synergia_movil\scripts\test_ticket.bin"
    with open(test_bin, "wb") as f:
        f.write(bytes_data)
    print(f"Generado {len(bytes_data)} bytes en {test_bin}")

    # Send to printer via raw_print_windows.ps1
    ps_cmd = f'powershell -ExecutionPolicy Bypass -File "C:\\Workspaces\\synergia_movil\\scripts\\raw_print_windows.ps1" -PrinterName "TIQUETES" -FilePath "{test_bin}"'
    print(f"Ejecutando: {ps_cmd}")
    res = subprocess.run(ps_cmd, shell=True, capture_output=True, text=True)
    print("STDOUT:", res.stdout)
    print("STDERR:", res.stderr)
    print("Return code:", res.returncode)

if __name__ == '__main__':
    test_print()
