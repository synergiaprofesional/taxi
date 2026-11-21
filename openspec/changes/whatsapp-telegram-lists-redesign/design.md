# Design: Arquitectura Visual y Cromática de Listas WhatsApp / Telegram

## Contexto y Decisiones Arquitectónicas

### 1. Eliminación de Cards Flotantes a favor de Edge-to-Edge
- **Problema:** `Card` introducía un margen horizontal de 10px a cada lado, más radios de esquina y elevación que sumaban 20px de ancho y 8px de alto de espacio muerto por ítem.
- **Solución:** `InkWell` de borde a borde con `Padding(horizontal: 16, vertical: 10)` combinado con `Divider` sangrado a 74px (`ListView.separated`).
- **Resultado:** Apariencia de mensajería moderna, limpia y con alto aprovechamiento del ancho de pantalla.

### 2. Formato del Avatar y Subtítulo Informativo
- **Avatar Protagonista:** `CircleAvatar(radius: 24)` alojando el número secuencial (`numeroTurno`), con verde esmeralda `#00A884` para el turno actual y fondos neutros para los turnos en espera.
- **Segunda Línea (Opción B):** `${conductor} • Espera: ${tiempo}`. El cálculo de tiempo se efectúa comparando `DateTime.now()` con `turno.fechaCreacion` para mostrar minutos transcurridos (`< 1 min`, `14 min`, `1h 10m`).
- **Despachos:** La misma fila sustituye la espera por el nombre del destino y la columna derecha exhibe el valor total en verde WhatsApp.

### 3. Buscador en Cápsula sin Botones Inferiores
- **Problema:** Las interfaces convencionales saturan el área debajo de los buscadores con botones de filtro rápido que restan altura a la lista.
- **Decisión del Usuario:** **Cero botones debajo del buscador**.
- **Diseño:** Un contenedor con `BorderRadius.circular(24)` integrado arriba en `BahiaSelectedView`. La lista arranca inmediatamente debajo, ganando más de 50px de viewport.

---

## Paleta Cromática Dual Fiel

```
┌────────────────────────────────────────────────────────────────────────┐
│                        ESQUEMA DUAL WHATSAPP                           │
├─────────────────────────┬──────────────────────┬───────────────────────┤
│ Propiedad               │ Modo Oscuro          │ Modo Claro            │
├─────────────────────────┼──────────────────────┼───────────────────────┤
│ Fondo de Lista          │ #0B141A              │ #FFFFFF               │
│ Fondo AppBar / Header   │ #111B21              │ #FFFFFF               │
│ Campo de Búsqueda       │ #20272B              │ #F0F2F5               │
│ Texto Principal (Placa) │ #E9EDEF              │ #111B21               │
│ Texto Secundario        │ #8696A0              │ #667781               │
│ Verde Activo (Turno/FAB)│ #00A884              │ #008069               │
│ Verde Valor / Badge     │ #25D366              │ #008069               │
│ Doble Check             │ #53BDEB              │ #53BDEB               │
│ Separador Sangrado      │ #222D34              │ #E9EDEF               │
└─────────────────────────┴──────────────────────┴───────────────────────┘
```

---

## Diagrama Estructural de la Fila (TurnoCardWidget)

```
┌────────────────────────────────────────────────────────────────────────┐
│  [ 1 ]   TLZ-892                                        10:50 a. m.    │
│ (Avatar)  ✓✓ Carlos Ramírez • Espera: 12 min          [ TURNO ACTUAL ] │
└────────────────────────────────────────────────────────────────────────┘
 ├── 74px ───────────────────────────────────────────────────────────────┤ (Divider)
```
