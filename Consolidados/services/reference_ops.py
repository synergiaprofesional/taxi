"""
Servicio para inspección y validación del repositorio local de referencia (reference/).
"""
import os
from pathlib import Path
from Consolidados.core.config import config

class ReferenceOps:
    """Operaciones de análisis sobre el código base de referencia descargado."""

    def __init__(self, reference_path: Path = None):
        self.ref_dir = reference_path or config.reference_dir

    def get_status(self) -> dict:
        exists = self.ref_dir.exists()
        addons_dir = self.ref_dir / "addons_fundetaxcol"
        rt_dir = self.ref_dir / "server_rt_odoo"
        config_dir = self.ref_dir / "config"

        modules = []
        if addons_dir.exists():
            modules = [d.name for d in addons_dir.iterdir() if d.is_dir()]

        return {
            "reference_exists": exists,
            "path": str(self.ref_dir),
            "addons_found": len(modules),
            "addons_list": modules,
            "server_rt_odoo": rt_dir.exists(),
            "config_files": [f.name for f in config_dir.glob("*")] if config_dir.exists() else []
        }

    def list_models_in_reference(self) -> list[str]:
        """Extrae los modelos Odoo definidos en los módulos de referencia para mapeo a Firebase."""
        models = []
        addons_dir = self.ref_dir / "addons_fundetaxcol"
        if not addons_dir.exists():
            return models

        for py_file in addons_dir.glob("**/models/*.py"):
            try:
                content = py_file.read_text(encoding="utf-8", errors="ignore")
                for line in content.splitlines():
                    if "_name = " in line:
                        model_name = line.split("_name = ")[1].strip().strip('"').strip("'")
                        models.append(f"{py_file.parent.parent.name} -> {model_name}")
            except Exception:
                continue
        return sorted(list(set(models)))
