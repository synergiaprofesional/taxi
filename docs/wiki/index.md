# 📚 Índice Maestro - LLM Wiki (Proyecto Taxi)

Este catálogo indexa la memoria ontológica del proyecto `Taxi`: reglas de negocio, esquemas de datos, contratos de infraestructura e invariantes arquitectónicos.

---

## 🌟 Documentos Maestros de Contexto y Conceptualización
* [`CONTEXTO_MAESTRO_PROYECTO_TAXI.md`](file:///c:/Workspaces/taxi/docs/CONTEXTO_MAESTRO_PROYECTO_TAXI.md): Documento integral y autosuficiente para transferir todo el contexto del proyecto a cualquier sesión de chat de Gemini.
* [`conceptualizaci_n_del_ecosistema_taxi.md`](file:///c:/Workspaces/taxi/docs/conceptualizaci_n_del_ecosistema_taxi.md): Manifiesto conceptual de la visión humana, el taxista como anfitrión urbano, el cliente de a pie y el eje vertical con aliados (hoteles, restaurantes, recreación).

---

## 🏛️ Entidades (`docs/wiki/entities/`)

| Entidad | Descripción | Archivo |
| :--- | :--- | :--- |
| **Tarifas Legales y Sectores** | Matriz tarifaria oficial por decreto, recargos legales y prohibición de arbitrariedad | [`tarifas_legales_y_sectores.md`](file:///c:/Workspaces/taxi/docs/wiki/entities/tarifas_legales_y_sectores.md) |
| **Gremios, Organizaciones y Jerarquías** | Organigrama gremial, conductores públicos vs privados y modelos de vinculación de pasajeros | [`gremios_y_organizaciones.md`](file:///c:/Workspaces/taxi/docs/wiki/entities/gremios_y_organizaciones.md) |
| **Perfiles de Usuario (RBAC)** | Administradores, Conductores y Clientes (Pasajeros) | [`perfiles_usuarios.md`](file:///c:/Workspaces/taxi/docs/wiki/entities/perfiles_usuarios.md) |
| **Plataformas y Dispositivos** | Android (Móviles y Tablets) y Desktop (Windows) | [`plataformas_dispositivos.md`](file:///c:/Workspaces/taxi/docs/wiki/entities/plataformas_dispositivos.md) |
| **Servidor de Producción** | Servidor host `fundetaxcol.co` en modo consulta estricta, Caddy, servicios y addons Odoo | [`servidor_produccion.md`](file:///c:/Workspaces/taxi/docs/wiki/entities/servidor_produccion.md) |
| **Backend Firebase** | Arquitectura objetivo de base de datos Firestore, Authentication y Cloud Functions | [`firebase_backend.md`](file:///c:/Workspaces/taxi/docs/wiki/entities/firebase_backend.md) |

---

## 💡 Conceptos (`docs/wiki/concepts/`)

| Concepto | Descripción | Archivo |
| :--- | :--- | :--- |
| **Jerarquía Gremial y Matriz de Visibilidad** | Convivencia de flota pública y privada, convenios corporativos y algoritmos de asignación | [`jerarquia_gremial_y_visibilidad_flota.md`](file:///c:/Workspaces/taxi/docs/wiki/concepts/jerarquia_gremial_y_visibilidad_flota.md) |
| **Propósito Humano y Ecosistema Urbano** | Dignificación del oficio, el taxista como anfitrión urbano y eje vertical | [`proposito_humano_y_ecosistema_urbano.md`](file:///c:/Workspaces/taxi/docs/wiki/concepts/proposito_humano_y_ecosistema_urbano.md) |
| **Monetización y Publicidad** | Estrategia de sostenibilidad: AdMob, convenios locales y reglas de no intrusión | [`modelo_monetizacion_publicidad.md`](file:///c:/Workspaces/taxi/docs/wiki/concepts/modelo_monetizacion_publicidad.md) |
| **Modelo Cebolla de Cobertura** | Estructura concéntrica: Núcleo Garita -> Conductores -> Clientes Finales | [`modelo_cebolla_arquitectura.md`](file:///c:/Workspaces/taxi/docs/wiki/concepts/modelo_cebolla_arquitectura.md) |
| **Arquitectura Taxi** | Enfoque multi-perfil, multi-dispositivo, alta cobertura y desacoplamiento de Odoo 11 | [`arquitectura_taxi.md`](file:///c:/Workspaces/taxi/docs/wiki/concepts/arquitectura_taxi.md) |
| **Transición UX sin Fricción** | Principios ergonómicos para conductores y operadores sin curva de aprendizaje | [`transicion_ux_usuarios.md`](file:///c:/Workspaces/taxi/docs/wiki/concepts/transicion_ux_usuarios.md) |

---

## 📜 Registro de Mutaciones
Consultar el historial cronológico de actualizaciones en [`log.md`](file:///c:/Workspaces/taxi/docs/wiki/log.md).
