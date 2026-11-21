# 🧭 Concepto: Jerarquía Gremial y Matriz de Visibilidad de Flota

Este concepto articula la convivencia armónica entre las estructuras gremiales organizadas (organigramas, jerarquías) y la dualidad de la flota de conductores (Públicos vs Privados), junto con los mecanismos de vinculación de los pasajeros.

---

## 1. Matriz de Emparejamiento y Despacho

```text
┌────────────────────────┬─────────────────────────────┬─────────────────────────────┐
│ TIPO DE CLIENTE        │ CONDUCTOR PÚBLICO           │ CONDUCTOR PRIVADO (CONVENIO)│
├────────────────────────┼─────────────────────────────┼─────────────────────────────┤
│ 🙋 Pasajero Público     │ ✅ Emparejamiento Directo   │ ❌ Oculto en Radar          │
│   (Ciudadano en calle) │    (Por proximidad o cola)  │    (Reservado para convenio)│
├────────────────────────┼─────────────────────────────┼─────────────────────────────┤
│ 🏢 Pasajero Corporativo │ ⚠️ Fallback Secundario      │ ✅ Prioridad Absoluta       │
│   (Hotel / Empresa)    │    (Si no hay flota privada)│    (Flota VIP / Asignada)   │
├────────────────────────┼─────────────────────────────┼─────────────────────────────┤
│ 🏷️ Cliente Vinculado   │ ⭐ Prioridad al Referido    │ ⭐ Prioridad al Referido    │
│   (Por código de taxi) │    (Si está libre y cerca)  │    (Si está asignado)       │
└────────────────────────┴─────────────────────────────┴─────────────────────────────┘
```

---

## 2. Implicaciones Arquitectónicas en Firebase Firestore

### Colección `/organizaciones/{orgId}`
```json
{
  "id": "fundetaxcol",
  "nombre": "Fundación de Taxistas de Colombia",
  "nit": "900.542.188-4",
  "organigrama": {
    "gerencia": ["uid_gerente_1"],
    "coordinadores": ["uid_coord_norte", "uid_coord_aeropuerto"],
    "cajeros_garita": ["uid_cajero_1", "uid_cajero_2"]
  },
  "bahias_reguladas": ["aeropuerto_1", "terminal_1", "bocagrande_hotel"]
}
```

### Colección `/conductores/{uid}`
```json
{
  "uid": "drv_12345",
  "nombre": "Carlos Mendoza",
  "organizacion_id": "fundetaxcol",
  "tipo_flota": "publica", // "publica" | "privada_corporativa"
  "convenio_asignado_id": null, // o "hotel_hilton_01" si fuera privado
  "propietario_vehiculo_uid": "prop_9988",
  "estado_operativo": "libre_calle",
  "ahorro_acumulado": 1450000.0,
  "calificacion": 4.95
}
```

### Colección `/usuarios/{uid}` (Pasajero)
```json
{
  "uid": "usr_7788",
  "telefono": "+573001234567",
  "nombre": "Andrea Gómez",
  "tipo_cliente": "corporativo", // "publico_general" | "corporativo" | "vinculado_referido"
  "organizacion_afiliada_id": "fundetaxcol",
  "convenio_activo_id": "hotel_hilton_01",
  "conductor_frecuente_preferido_uid": "drv_12345"
}
```

---

## 3. Beneficios Estratégicos de Esta Arquitectura
1. **Protección del Negocio Institucional:** Los gremios pueden negociar contratos millonarios con hoteles y grandes empresas, garantizando una flota privada dedicada de alta calidad sin mezclarla con el despacho público aleatorio.
2. **Fidelización Efectiva:** El taxista gana incentivos reales al compartir su código con pasajeros frecuentes, creando su propia cartera de clientes respaldada por la seguridad del gremio.
3. **Escalabilidad Multi-Gremio:** Varios gremios pueden convivir en la plataforma sin que sus datos contables, conductores o convenios privados se filtren entre organizaciones.
