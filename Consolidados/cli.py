#!/usr/bin/env python3
"""
CLI Maestro Unificado del Proyecto Taxi (Consolidados/cli.py).
Doble interfaz: Menú interactivo (sin argumentos) y subcomandos automatizados por flags.
"""
import sys
from pathlib import Path

# Asegurar que la raíz del proyecto esté en sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import argparse
from Consolidados.core.config import config
from Consolidados.services.reference_ops import ReferenceOps
from Consolidados.services.server_ops import ServerOps

def show_interactive_menu():
    print("=" * 65)
    print(f"  🚕 TOOLKIT MAESTRO UNIFICADO - PROYECTO TAXI (v{config.version})")
    print("=" * 65)
    print("1. Consultar estado del repositorio local de referencia (reference/)")
    print("2. Mapear modelos Odoo de referencia (para migración a Firebase)")
    print("3. Consultar salud y estado del servidor de producción (READ-ONLY)")
    print("4. Ver configuración tipada del sistema (.env / config)")
    print("5. Salir")
    print("-" * 65)
    
    choice = input("Seleccione una opción [1-5]: ").strip()
    if choice == "1":
        cmd_reference_status()
    elif choice == "2":
        cmd_reference_models()
    elif choice == "3":
        cmd_server_health()
    elif choice == "4":
        cmd_show_config()
    elif choice == "5":
        print("Saliendo...")
        sys.exit(0)
    else:
        print("[!] Opción inválida.")

def cmd_reference_status():
    ops = ReferenceOps()
    status = ops.get_status()
    print("\n📦 ESTADO DE REFERENCIA LOCAL:")
    print(f"  Ruta: {status['path']}")
    print(f"  Existe: {status['reference_exists']}")
    print(f"  Módulos Addons ({status['addons_found']}): {', '.join(status['addons_list'])}")
    print(f"  Server RT Odoo presente: {status['server_rt_odoo']}")
    print(f"  Archivos de config respaldados: {', '.join(status['config_files'])}\n")

def cmd_reference_models():
    ops = ReferenceOps()
    models = ops.list_models_in_reference()
    print("\n📊 MODELOS DE REFERENCIA ENCONTRADOS (CANDIDATOS A FIREBASE):")
    for m in models:
        print(f"  - {m}")
    print(f"Total: {len(models)} modelos mapeados.\n")

def cmd_server_health():
    print("\n🔍 CONSULTANDO SERVIDOR (MODO ESTRICTO SOLO LECTURA)...")
    ops = ServerOps()
    try:
        health = ops.get_health()
        print(f"  Uptime: {health['uptime']}")
        print("  Servicios:")
        for s in health['services_status']:
            print(f"    * {s}")
        print("  Puertos Activos:")
        for p in health['active_ports']:
            print(f"    * {p}")
        print("  [OK] Servidor consultado sin mutaciones.\n")
    except Exception as e:
        print(f"[!] Error al consultar servidor: {e}\n")
    finally:
        ops.close()

def cmd_show_config():
    print("\n⚙️ CONFIGURACIÓN TIPADA DEL PROYECTO:")
    print(f"  Entorno: {config.env}")
    print(f"  Versión: {config.version}+{config.build_number}")
    print(f"  Base Dir: {config.base_dir}")
    print(f"  Reference Dir: {config.reference_dir}")
    print(f"  Servidor Prod Host: {config.server.host} (Read-Only: {config.server.read_only})")
    print(f"  Firebase Project: {config.firebase.project_id or '[Pendiente de configuración]'}\n")

def main():
    parser = argparse.ArgumentParser(description="Toolkit Maestro Unificado - Taxi")
    subparsers = parser.add_subparsers(dest="command", help="Comandos disponibles")

    subparsers.add_parser("status", help="Estado de la carpeta de referencia")
    subparsers.add_parser("models", help="Mapeo de modelos Odoo a migrar")
    subparsers.add_parser("health", help="Estado del servidor de producción (READ-ONLY)")
    subparsers.add_parser("config", help="Mostrar configuración tipada")

    if len(sys.argv) == 1:
        show_interactive_menu()
    else:
        args = parser.parse_args()
        if args.command == "status":
            cmd_reference_status()
        elif args.command == "models":
            cmd_reference_models()
        elif args.command == "health":
            cmd_server_health()
        elif args.command == "config":
            cmd_show_config()
        else:
            parser.print_help()

if __name__ == "__main__":
    main()
