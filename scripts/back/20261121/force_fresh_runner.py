import os
import subprocess

exe_path = r"c:\Workspaces\synergia_movil\build\windows\x64\runner\Release\synergia_movil.exe"
if os.path.exists(exe_path):
    os.remove(exe_path)
    print("Old synergia_movil.exe removed successfully.")

# Also touch main.cpp to force runner rebuild
main_cpp = r"c:\Workspaces\synergia_movil\windows\runner\main.cpp"
if os.path.exists(main_cpp):
    with open(main_cpp, "a", encoding="utf-8") as f:
        f.write("\n// build trigger\n")
    print("main.cpp touched.")
