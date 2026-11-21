# 📱 Entidad: Plataformas y Dispositivos de Despliegue

La plataforma **Taxi** está diseñada con un enfoque multiplataforma basado en Flutter, optimizando la experiencia de usuario y el rendimiento según las dimensiones físicas y capacidades de hardware de cada dispositivo.

---

## 1. Mapa de Plataformas y Formatos

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   ECOSISTEMA DE DISPOSITIVOS TAXI                      │
├───────────────────────────────────┬────────────────────────────────────┤
│ 📱 Android Smartphones            │ 📲 Android Tablets (Garita/Terminal│
├───────────────────────────────────┼────────────────────────────────────┤
│ - Conductores y Pasajeros         │ - Despacho táctil en bahías        │
│ - Diseño vertical responsivo      │ - Diseño split-view / tablero      │
│ - GPS y notificaciones push (FCM) │ - Botones táctiles amplios         │
│ - Consumo energético eficiente    │ - Impresión Bluetooth/WiFi directa │
├───────────────────────────────────┴────────────────────────────────────┤
│ 🖥️ Desktop Windows (Consola Maestra de Administración)                  │
├────────────────────────────────────────────────────────────────────────┤
│ - Administración del sistema, parametrización, liquidación y reportes  │
│ - Pantalla completa con atajos de teclado y alta densidad de datos     │
│ - Impresión térmica ESC/POS nativa vía Win32/TCP                       │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Requerimientos de UX y Hardware por Plataforma

### 📱 1. Android Móvil (Smartphones)
* **Target:** Conductores y Pasajeros.
* **Ergonomía:** Interfaces de alta legibilidad, controles táctiles al alcance de una sola mano, soporte de modo oscuro/alto contraste para conducción nocturna y bajo sol directo.
* **Hardware Crítico:** GPS de precisión en segundo plano (Location Services), conectividad de datos intermitente (soporte offline de Firestore), notificaciones sonoras push de alta prioridad.

### 📲 2. Android Tablet (Garitas y Terminales)
* **Target:** Operadores de Despacho en garita y supervisores de punto fijo.
* **Ergonomía:** Vista horizontal de alta densidad con disposición tipo *Split-View*:
  * Panel izquierdo: Lista de bahías y vehículos en cola.
  * Panel derecho: Formulario de despacho rápido, cobro de recaudo y atajos táctiles.
* **Hardware Crítico:** Conexión permanente por cable/WiFi, enlace Bluetooth SPP a impresoras térmicas de tickets y soporte para escáneres o lectores auxiliares.

### 🖥️ 3. Windows Desktop (Consola Administrativa)
* **Target:** Administradores, auditores, liquidadores y gerencia.
* **Ergonomía:** Dashboards con tablas de datos paginadas, filtros multidimensionales, gráficas de rendimiento y generación masiva de reportes contables/operativos en PDF y Excel.
* **Hardware Crítico:** Compatibilidad nativa con impresoras de matriz o térmicas USB/COM mediante DLLs Win32 optimizadas.
