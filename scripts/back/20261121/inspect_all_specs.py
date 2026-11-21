from pathlib import Path

specs_dir = Path(r"c:\Workspaces\synergia_movil\openspec\specs")
for p in sorted(specs_dir.glob("*/spec.md")):
    cap_name = p.parent.name
    content = p.read_text(encoding="utf-8", errors="ignore")
    lines = content.splitlines()
    print(f"\n=================== {cap_name} ({len(lines)} lines) ===================")
    for l in lines[:25]:
        print(f"  {l}")
    if len(lines) > 25:
        print(f"  ... ({len(lines)-25} lines more)")
