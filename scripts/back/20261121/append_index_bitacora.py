new_index = """---

### [2026-10-17 23:05] Parseo Polimórfico de Placas (Odoo get_all Map) e Inyección Binaria RAW Spooler Windows ("TIQUETES" USB001)
* **Problema:** Los turnos mostraban el conductor pero salían con `'SIN-PLACA'` debido a que Odoo retorna Many2one como Diccionarios (`Map`) en `get_all` y no Listas; y la impresora física no expulsaba papel porque `TipoImpresora.spoolerWindows` tenía un stub vacío.
* **Solución:** Implementado parseo polimórfico en `TurnoModel.fromJson` soportando `Map`, `List`, `String`, anónimos y regex fallback en `name`. Implementada inyección RAW directa al spooler Win32 (`winspool.drv` / `WritePrinter`) verificada con prueba física real en la impresora `"TIQUETES"` (código de salida 0). Actualizados binarios Windows y APK instalado en tablet.
* **Enlaces:** [Bitácora Diaria 17/10/2026](file:///c:/Workspaces/synergia_movil/Bitacoras/Bitacora%2017102026.md) | [Bitácora Sesión 230500](file:///c:/Workspaces/synergia_movil/Bitacoras/Bitacora%2020261017%20230500.md) | [SDD](file:///c:/Workspaces/synergia_movil/docs/sdd-turnos-placas-impresion-20261017.md)
"""

with open(r"C:\Workspaces\synergia_movil\Bitacoras\bitacoras.md", "a", encoding="utf-8") as f:
    f.write(new_index)
print("Updated bitacoras.md")
