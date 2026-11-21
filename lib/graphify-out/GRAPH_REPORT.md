# Graph Report - C:\Workspaces\synergia_movil\lib  (2026-11-02)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 695 nodes · 916 edges · 31 communities (30 shown, 1 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
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
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]

## God Nodes (most connected - your core abstractions)
1. `BahiaModel` - 3 edges
2. `PagoRecaudoModel` - 3 edges
3. `bahiaSesionId` - 3 edges
4. `ConductorModel` - 3 edges
5. `VehiculoModel` - 3 edges
6. `LoginDialog` - 3 edges
7. `_LoginDialogState` - 3 edges
8. `LoginView` - 3 edges
9. `_LoginViewState` - 3 edges
10. `TurnoFormView` - 3 edges

## Surprising Connections (you probably didn't know these)
- `TurnoController` --inherits--> `GetxController`  [EXTRACTED]
  None → None  _Bridges community 17 → community 7_
- `ThemeController` --references--> `static const String`  [EXTRACTED]
  None → None  _Bridges community 2 → community 17_
- `LoginDialog` --inherits--> `StatefulWidget`  [EXTRACTED]
  ui/views/auth/login_dialog.dart → None  _Bridges community 16 → community 27_
- `LoginView` --inherits--> `StatefulWidget`  [EXTRACTED]
  ui/views/auth/login_view.dart → None  _Bridges community 27 → community 13_
- `HomeView` --inherits--> `StatefulWidget`  [EXTRACTED]
  ui/views/home/home_view.dart → None  _Bridges community 27 → community 8_

## Import Cycles
- None detected.

## Communities (31 total, 1 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.04
Nodes (53): static const Color, accent, AppColors, background, cardBorder, darkBackground, darkCardBorder, darkSurface (+45 more)

### Community 1 - "Community 1"
Cohesion: 0.04
Nodes (45): ../core/network/network_config.dart, dart:convert, GetxService, ../models/tarifa_sector_model.dart, ../models/vehicle_model.dart, NetworkConfig, package:flutter/foundation.dart, package:http/http.dart (+37 more)

### Community 2 - "Community 2"
Cohesion: 0.05
Nodes (44): AppVersion, display, environment, shortDisplay, ticketFooter, versionCode, versionName, dart:io (+36 more)

### Community 3 - "Community 3"
Cohesion: 0.05
Nodes (42): bool get, Color get, int get, bahiaBaseId, bahiaNombre, colorEstado, conductorId, conductorNombre (+34 more)

### Community 4 - "Community 4"
Cohesion: 0.05
Nodes (40): _abrirAgregarConcepto, build, _cargarConceptosPorDefecto, _conductorCtrl, _conductorSeleccionado, createState, currencyFormat, dispose (+32 more)

### Community 5 - "Community 5"
Cohesion: 0.05
Nodes (40): double get, AhorroModel, ahorros, bahiaId, bahiaNombre, cantidad, company, CompanyModel (+32 more)

### Community 6 - "Community 6"
Cohesion: 0.05
Nodes (37): _aplicaRecargoNocturno, build, _buildFormDespachar, _buildFormEnturnar, _calcularRecargoNocturnoAutomatico, _cancelarTurno, _conductorCtrl, _conductorSeleccionado (+29 more)

### Community 7 - "Community 7"
Cohesion: 0.05
Nodes (37): autoConnectSockets, bahiaIdActual, bahiasDisponibles, bahiaSeleccionada, buscarPagosHistoricosRemotos, cambiarBahia, cancelarTurno, cargarBahiasDesdeServidor (+29 more)

### Community 8 - "Community 8"
Cohesion: 0.06
Nodes (33): autoConnectSockets, build, _buildDesktopLayout, _buildMetricTile, _buildMobileLayout, _buildStatusChip, _buildTabletLayout, _buildTurnoAtencionWidget (+25 more)

### Community 9 - "Community 9"
Cohesion: 0.06
Nodes (32): package:synergia_movil/controllers/turno_controller.dart, package:synergia_movil/core/config/app_version.dart, package:synergia_movil/core/utils/local_storage.dart, package:synergia_movil/models/bay_model.dart, package:synergia_movil/models/printer_config_model.dart, package:synergia_movil/services/odoo_service.dart, package:synergia_movil/services/printer_service.dart, package:synergia_movil/services/socket_service.dart (+24 more)

### Community 10 - "Community 10"
Cohesion: 0.06
Nodes (30): DateTime, activa, bahiaId, BahiaModel, bahiaNombre, codigo, estado, fechaInicio (+22 more)

### Community 11 - "Community 11"
Cohesion: 0.09
Nodes (22): IconData, T, _abrirBuscador, build, _buildItemTile, createState, dispose, _ejecutarBusqueda (+14 more)

### Community 12 - "Community 12"
Cohesion: 0.10
Nodes (20): _agregarConcepto, bahiaId, bahiaNombre, build, _cargarConceptos, _catalogoConceptos, _conductorCtrl, conductorInicial (+12 more)

### Community 13 - "Community 13"
Cohesion: 0.11
Nodes (19): _bahias, build, _buildBahiasGrid, _buildForm, _buildHeader, _buildTwoColumnLayout, _buildVerticalLayout, createState (+11 more)

### Community 14 - "Community 14"
Cohesion: 0.10
Nodes (19): ../bahia/bahia_selector_dialog.dart, ../form/turno_form_view.dart, ../list/despacho_list_view.dart, ../list/pago_list_view.dart, ../list/turno_list_view.dart, _abrirDialogoEnturnar, _abrirFormularioDespacho, _abrirSelectorBahia (+11 more)

### Community 15 - "Community 15"
Cohesion: 0.11
Nodes (18): build, _cantidadCtrl, _cargarCatalogo, _conceptos, _conceptoSeleccionado, createState, dispose, _formKey (+10 more)

### Community 16 - "Community 16"
Cohesion: 0.12
Nodes (16): build, createState, dispose, _errorMessage, _iniciarSesion, initState, _isLoading, LoginDialog (+8 more)

### Community 17 - "Community 17"
Cohesion: 0.13
Nodes (15): controllers/theme_controller.dart, _loadTheme, onInit, setThemeMode, _storageKey, themeMode, core/theme/app_theme.dart, ../core/utils/local_storage.dart (+7 more)

### Community 18 - "Community 18"
Cohesion: 0.16
Nodes (12): ../core/theme/app_colors.dart, ../form/payment_form_view.dart, build, onNuevoRecaudoPressed, searchQuery, ../models/payment_model.dart, PagoRecaudoModel, VoidCallback? (+4 more)

### Community 19 - "Community 19"
Cohesion: 0.17
Nodes (11): ../models/turno_model.dart, package:intl/intl.dart, build, onLongPress, onTap, turno, build, _calcularTiempoEspera (+3 more)

### Community 20 - "Community 20"
Cohesion: 0.15
Nodes (12): package:shared_preferences/shared_preferences.dart, static SharedPreferences?, clear, getBool, getInt, getString, initialize, _prefs (+4 more)

### Community 21 - "Community 21"
Cohesion: 0.18
Nodes (10): ../../../controllers/turno_controller.dart, build, searchQuery, build, onEnturnarPressed, searchQuery, package:get/get.dart, ../../widgets/despacho_card_widget.dart (+2 more)

### Community 22 - "Community 22"
Cohesion: 0.18
Nodes (10): bahiaActualId, _bahias, build, _cargarBahias, createState, initState, _isLoading, odooService (+2 more)

### Community 23 - "Community 23"
Cohesion: 0.20
Nodes (9): anchoPapel, autoCorte, fromJson, nombreODireccion, puerto, tipo, TipoImpresora, toJson (+1 more)

### Community 24 - "Community 24"
Cohesion: 0.25
Nodes (7): build, controller, createState, dispose, _searchController, _searchQuery, TextEditingController

### Community 25 - "Community 25"
Cohesion: 0.29
Nodes (6): autoConnectSockets, build, ../home/home_view.dart, login_view.dart, OdooService, ../services/odoo_service.dart

### Community 26 - "Community 26"
Cohesion: 0.29
Nodes (6): ../core/config/app_version.dart, ../services/socket_service.dart, build, _buildInfoCard, _buildSectionHeader, _buildTile

### Community 27 - "Community 27"
Cohesion: 0.29
Nodes (7): _PaymentConceptFormState, _PaymentFormViewState, TurnoFormView, _PagoDialogState, _SettingsViewState, State, StatefulWidget

### Community 28 - "Community 28"
Cohesion: 0.50
Nodes (3): app_colors.dart, package:flutter/material.dart, AppTheme

### Community 29 - "Community 29"
Cohesion: 0.50
Nodes (4): despacho_list_view.dart, SynergiaMovilApp, StatelessWidget, PagoCardWidget

## Knowledge Gaps
- **534 isolated node(s):** `_storageKey`, `onInit`, `_loadTheme`, `setThemeMode`, `autoConnectSockets` (+529 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `BahiaModel` connect `Community 10` to `Community 8`, `Community 14`?**
  _High betweenness centrality (0.020) - this node is a cross-community bridge._
- **Why does `bahiaSesionId` connect `Community 10` to `Community 3`, `Community 5`?**
  _High betweenness centrality (0.014) - this node is a cross-community bridge._
- **Why does `PagoRecaudoModel` connect `Community 18` to `Community 4`, `Community 5`?**
  _High betweenness centrality (0.012) - this node is a cross-community bridge._
- **What connects `_storageKey`, `onInit`, `_loadTheme` to the rest of the system?**
  _534 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.037037037037037035 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.044444444444444446 - nodes in this community are weakly interconnected._
- **Should `Community 2` be split into smaller, more focused modules?**
  _Cohesion score 0.045454545454545456 - nodes in this community are weakly interconnected._