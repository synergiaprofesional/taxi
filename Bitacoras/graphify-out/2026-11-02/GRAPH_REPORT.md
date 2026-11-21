# Graph Report - C:\Workspaces\synergia_movil\Bitacoras  (2026-11-02)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 32 nodes · 26 edges · 9 communities (5 shown, 4 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 1 edges (avg confidence: 1.0)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]

## God Nodes (most connected - your core abstractions)
1. `TurnoController` - 6 edges
2. `TurnoController` - 4 edges
3. `BahiaSelectedView` - 4 edges
4. `Synergia Móvil` - 3 edges
5. `addons_fundetaxcol (Odoo 11)` - 3 edges
6. `PrinterService` - 3 edges
7. `OdooService` - 2 edges
8. `Caddy Reverse Proxy` - 2 edges
9. `OdooService` - 2 edges
10. `SocketService` - 2 edges

## Surprising Connections (you probably didn't know these)
- `Fail2ban Defense` --conceptually_related_to--> `Caddy Reverse Proxy`  [INFERRED]
  Bitacora 20261017 183200.md → Bitacora 20261017 175430.md
- `TurnoController` --calls--> `OdooService`  [EXTRACTED]
  Bitacora 20261017 190133.md → Bitacora 20261017 192500.md
- `TurnoController` --calls--> `PrinterService`  [EXTRACTED]
  Bitacora 20261017 190133.md → Bitacora 20261017 192500.md
- `TurnoController` --calls--> `SocketService`  [EXTRACTED]
  Bitacora 20261017 190133.md → Bitacora 20261017 192500.md
- `TurnoController` --shares_data_with--> `PaymentModel`  [EXTRACTED]
  Bitacora 20261017 190133.md → Bitacora 20261018 114135.md

## Import Cycles
- None detected.

## Communities (9 total, 4 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.29
Nodes (7): server_rt_odoo (Node.js/Socket.IO), NetworkConfig, TurnoController, OdooService, SocketService, AuthGatekeeper / LoginView, PaymentModel

### Community 1 - "Community 1"
Cohesion: 0.33
Nodes (6): addons_fundetaxcol (Odoo 11), Caddy Server v2, fundetaxcol_flutter, OdooService, server_rt_odoo (WebSockets), Synergia Móvil

### Community 2 - "Community 2"
Cohesion: 0.33
Nodes (6): PrinterService, BahiaSelectedView, TurnoCardWidget, C:\proxyServer (Hardware Proxy), AppVersion, DespachoCardWidget

### Community 3 - "Community 3"
Cohesion: 0.50
Nodes (4): BahiaSelectedView, PagoRecaudoModel, TurnoController, TurnoModel

### Community 4 - "Community 4"
Cohesion: 0.67
Nodes (3): Caddy Reverse Proxy, odoo_80.service (Systemd), Fail2ban Defense

## Knowledge Gaps
- **21 isolated node(s):** `fundetaxcol_flutter`, `server_rt_odoo (WebSockets)`, `Caddy Server v2`, `PrinterService`, `BahiaSelectedView` (+16 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `TurnoController` connect `Community 0` to `Community 2`?**
  _High betweenness centrality (0.112) - this node is a cross-community bridge._
- **Why does `BahiaSelectedView` connect `Community 2` to `Community 0`?**
  _High betweenness centrality (0.053) - this node is a cross-community bridge._
- **What connects `fundetaxcol_flutter`, `server_rt_odoo (WebSockets)`, `Caddy Server v2` to the rest of the system?**
  _21 weakly-connected nodes found - possible documentation gaps or missing edges._