# ⚖️ Entidad: Tarifas Legales Estandarizadas y Matriz de Sectores

En el sistema **Taxi**, las tarifas son un **invariante no negociable de legalidad y confianza**: deben ser estrictamente **estandarizadas, oficiales y verificables**, erradicando la arbitrariedad, el regateo callejero y las tarifas dinámicas especulativas.

---

## 1. Principio Fundamental: Cero Arbitrariedad Tarifaria

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   PRINCIPIO DE TRANSPARENCIA TARIFARIA                 │
├────────────────────────────────────────────────────────────────────────┤
│ ❌ PROHIBIDO                                                           │
│   - Tarifas dinámicas especulativas (multiplicadores 2x, 3x por lluvia)│
│   - Cobro arbitrario o a criterio discrecional del conductor          │
│   - Regateo o sobrecostos ocultos al finalizar el trayecto             │
├────────────────────────────────────────────────────────────────────────┤
│ ✅ OBLIGATORIO                                                         │
│   - Tarifa calculada según Decreto Distrital de Transporte             │
│   - Matriz fija Origen ➔ Destino (Sectores y Barrios)                 │
│   - Recargos legales explícitos y desglosados en pantalla              │
│   - Mismo valor visible simultáneamente para Conductor y Pasajero      │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Estructura de la Matriz Oficial (Herencia Odoo $\rightarrow$ Firestore)

Mapeado directamente desde `fundetaxcol.tarifa.sector`, `fundetaxcol.barrio.sector` y decretos distritales en `/tarifas_sector/{sectorId}`:

### Desglose Paramétrico del Valor del Viaje:
$$\text{Tarifa Total} = \text{Valor Base (Sector)} + \text{Recargo Nocturno} + \text{Recargo Festivo/Dominical} + \text{Recargo Terminal/Aeropuerto}$$

1. **Valor Base por Sector (`valor_base`):**  
   Fijado por la autoridad de transporte para la carrera mínima o para el par origen-destino (ej: Bocagrande $\rightarrow$ Aeropuerto, Manga $\rightarrow$ Centro).
2. **Recargo Nocturno (`recargo_nocturno`):**  
   Aplicable estrictamente en la ventana legal horaria (típicamente 20:00 a 05:00). El sistema evalúa el timestamp en el servidor (Firebase Cloud Functions), impidiendo la activación fraudulenta fuera de horario.
3. **Recargo Festivo / Dominical (`recargo_festivo`):**  
   Verificado automáticamente contra el calendario oficial de días festivos en Colombia.
4. **Recargo de Bahía Especial / Terminal (`recargo_aeropuerto`):**  
   Sobrecosto reglamentado para recogidas en terminales aéreas o marítimas.

---

## 3. Modelo de Datos Firestore (`/tarifas_sector/{id}`)

```json
{
  "id": "sec_bocagrande_aeropuerto",
  "origen_sector_id": "sec_bocagrande",
  "destino_sector_id": "sec_crespo_aeropuerto",
  "valor_base": 18000.0,
  "recargo_nocturno": 3000.0,
  "recargo_festivo": 3000.0,
  "recargo_aeropuerto": 4000.0,
  "activo": true,
  "decreto_autoridad": "Decreto Distrital 0284 / DATT",
  "fecha_vigencia": "2026-01-01T00:00:00Z"
}
```

---

## 4. Experiencia de Usuario Bidireccional (Pantalla Espejo)

* **Antes de Iniciar el Viaje:**  
  El pasajero conoce la cotización oficial desglosada y el conductor ve la misma cifra exacta al aceptar el servicio.
* **Al Finalizar el Viaje:**  
  La pantalla de cobro del conductor y la pantalla de pago del pasajero muestran exactamente el mismo monto. 
* **Tiquete y Auditoría:**  
  En despachos presenciales de garita se imprime el ticket físico ESC/POS con el valor regulado. En despachos digitales por app se emite el comprobante digital en Firestore. Cualquier intento de cobro por encima de la tarifa oficial es causal de sanción administrativa y bloqueo en el gremio.
