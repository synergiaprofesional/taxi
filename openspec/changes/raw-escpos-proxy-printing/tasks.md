# Tasks: Inyección Directa RAW ESC/POS

- [x] 1. Diagnóstico de endpoints y capacidades Win32 de `C:\proxyServer`
- [ ] 2. Implementar endpoint `POST /hw_proxy/print_raw` en `C:\proxyServer\src\routes.py`
- [ ] 3. Reiniciar servicio `C:\proxyServer` y probar endpoint con script de prueba
- [ ] 4. Ajustar `PrinterService._imprimirPorUrl` en la app móvil para preferir `/hw_proxy/print_raw`
- [ ] 5. Verificar con `flutter analyze`
- [ ] 6. Compilar Windows Release (`synergia_movil.exe`) y APK Release (`app-release.apk`)
- [ ] 7. Desplegar en la tablet `HA27VLYC` vía ADB
- [ ] 8. Documentar en Bitácora Dual (`Bitacoras/`) y registrar en Engram
