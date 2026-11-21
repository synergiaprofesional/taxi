# Propuesta: Sprint A — Categorías Rápidas, Oferta con Ancla Legal y Selección de Conductor

## 1. Justificación y Contexto
Inspirados en las mejores virtudes de Uber (simplicidad de categorías en 1 toque) e inDrive (control del pasajero para publicar oferta y elegir conductor de una lista transparente), adaptamos este modelo a la ventaja estructural del taxi formal colombiano. A diferencia de las apps transnacionales con algoritmos opacos de tarifa dinámica o subastas sin piso, Taxi implementa:
1. **Selector de Categorías en 1 Toque:** Taxi Estándar, Bahía Prioritaria, Ejecutivo VIP y Envíos Express.
2. **Ancla Legal Oficial:** La tarifa base siempre se calcula a partir del decreto distrital vigente por sectores y recargos oficiales.
3. **Control y Negociación:** El pasajero propone su precio (ajustando la tarifa legal hacia arriba o abajo en tramos de $1.000 o $2.000 COP) y los conductores cercanos o en bahía pueden aceptar o contraofertar.
4. **Marketplace Transparente "Elige tu Conductor":** El pasajero ve en tiempo real las fichas de los conductores que aceptaron (foto, nombre, placa, modelo, calificación, distancia en metros y tiempo de llegada) y él mismo decide a quién subir a su viaje.

## 2. Alcance Técnico
- **Modelo de Datos:** Incorporación de `CategoriaViaje` y `ConductorOfertaModel` en `lib/models/viaje_model.dart`.
- **Servicios:** Métodos en `FirestoreRepository` para publicar ofertas de conductores (`proponerOfertaConductor`), escuchar en tiempo real (`streamOfertasViaje`) y seleccionar la oferta ganadora (`seleccionarConductorViaje`).
- **Interfaz de Usuario:** Rediseño de `PassengerHomeView` con carrusel de categorías y selector de oferta con incrementos; creación de `DriverOffersSheet` para la selección del conductor.
- **TDD:** Suite unitaria `test/models/categoria_oferta_test.dart` y actualización de `COMPENDIO_TESTS.md`.
