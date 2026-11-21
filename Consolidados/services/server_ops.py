"""
Servicio de consulta remota en modo estricto de solo lectura para el servidor de producción.
"""
from Consolidados.core.db import ReadOnlyServerClient

class ServerOps:
    """Consultas operativas de estado en producción sin mutaciones."""

    def __init__(self):
        self.client = ReadOnlyServerClient()

    def get_health(self) -> dict:
        out_uptime, _ = self.client.execute_read_command("uptime")
        out_ports, _ = self.client.execute_read_command("ss -tulpn | grep -E '(80|443|3000|8069)'")
        out_services, _ = self.client.execute_read_command(
            "systemctl is-active caddy odoo_80 2>/dev/null || echo 'check systemd'"
        )
        return {
            "uptime": out_uptime,
            "active_ports": out_ports.splitlines(),
            "services_status": out_services.splitlines()
        }

    def close(self):
        self.client.close()
