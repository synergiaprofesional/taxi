"""
Clientes y conectores protegidos para consulta e infraestructura de Taxi.
"""
import paramiko
from Consolidados.core.config import config

class ReadOnlyServerClient:
    """Cliente SSH seguro y estricto de SOLO LECTURA hacia el servidor de producción."""
    
    def __init__(self):
        self.host = config.server.host
        self.user = config.server.user
        self.password = config.server.password
        self._client = None

    def connect(self) -> paramiko.SSHClient:
        if not self._client:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(self.host, username=self.user, password=self.password, timeout=12)
            self._client = client
        return self._client

    def execute_read_command(self, cmd: str) -> tuple[str, str]:
        """Ejecuta un comando de lectura. Rechaza cualquier comando de escritura sospechoso."""
        forbidden_tokens = ["rm ", "rmdir", "mkfs", ">", ">>", "truncate", "drop ", "delete "]
        cmd_lower = cmd.lower()
        for token in forbidden_tokens:
            if token in cmd_lower and not ("grep" in cmd_lower or "2>/dev/null" in cmd_lower):
                raise PermissionError(f"Comando denegado por Regla de Solo Lectura: contiene token prohibido '{token}'")
        
        client = self.connect()
        stdin, stdout, stderr = client.exec_command(cmd)
        out = stdout.read().decode("utf-8", errors="ignore").strip()
        err = stderr.read().decode("utf-8", errors="ignore").strip()
        return out, err

    def close(self):
        if self._client:
            self._client.close()
            self._client = None
