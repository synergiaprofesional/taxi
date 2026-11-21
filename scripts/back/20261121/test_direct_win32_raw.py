import win32print

try:
    pname = "TIQUETES"
    hPrinter = win32print.OpenPrinter(pname)
    print(f"Abierto {pname} con exito!")
    win32print.ClosePrinter(hPrinter)
    print("Soporta win32print RAW perfectamente!")
except Exception as e:
    print("Error:", e)
