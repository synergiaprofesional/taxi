# 🏛️ Entidad: Servidor de Producción (`fundetaxcol.co`)

## 1. Identificación y Parámetros de Red
- **Dominio:** `fundetaxcol.co`
- **IP Pública:** `149.22.88.135`
- **Usuario SSH:** `root`
- **Régimen de Operación:** **ESTRICTAMENTE SOLO LECTURA (READ-ONLY)**.
- **Prohibición Expresa:** Prohibido modificar, crear o alterar archivos o servicios en este servidor.

## 2. Pila Tecnológica en Producción
- **Reverse Proxy:** Caddy (`/etc/caddy/Caddyfile`) gestionando HTTP (80) y HTTPS (443).
- **ERP:** Odoo 11 EE en `127.0.0.1:8069` (servicio `odoo_80.service`).
- **Servicio Realtime / Socket.IO:** Node.js Express en `127.0.0.1:3000` (`/opt/server_rt_odoo/`).
- **Base de Datos:** PostgreSQL 9.6/10 (`fundetaxcol`).

## 3. Módulos y Código de Referencia Descargados Localmente
Respaldados en `reference/`:
- `reference/addons_fundetaxcol/`:
  - `fundetaxcol`: Módulo central de turnos, vehículos, pagos y conceptos.
  - `fundetaxcol_movil`: Extensiones y vistas para terminales móviles.
  - `fundetaxcol_whatsapp`: Integración de mensajería.
  - `ft_informe`, `mensajeria`, `print_javascript`.
- `reference/server_rt_odoo/`: Código de pasarela Socket.IO.
- `reference/config/`: `Caddyfile`, `odoo_80.conf`, `odoo_80.service`.
