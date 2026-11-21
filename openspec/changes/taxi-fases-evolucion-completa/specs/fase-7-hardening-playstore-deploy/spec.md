## ADDED Requirements

### Requirement: Compilación Multiplataforma (.apk y .exe)
El sistema SHALL compilar limpiamente tanto para Android (APK y App Bundle `.aab`) como para Windows Desktop (`taxi.exe`), compartiendo la misma base de código reactiva sobre Firebase.

#### Scenario: Compilación Dual Sin Errores
- **WHEN** se ejecutan los comandos de compilación para Android y Windows Desktop
- **THEN** ambos entornos producen artefactos ejecutables funcionales con cero errores de análisis estático

### Requirement: Catálogo y Cobertura TDD
El sistema SHALL someter todos los modelos y servicios a pruebas unitarias y de integración, catalogando cada suite en `tests/COMPENDIO_TESTS.md` con cero fallos tolerados.

#### Scenario: Ejecución de Arneses de Prueba
- **WHEN** se ejecuta `flutter test`
- **THEN** la totalidad de las pruebas unitarias pasan con éxito antes de cualquier despliegue
