/// Helper utilitario para generación de enlaces y mensajes de seguimiento vía WhatsApp
class WhatsAppTrackingHelper {
  /// Base URL canónica para el tracking web del pasajero
  static const String defaultBaseUrl = 'https://taxi.fundetaxcol.co';

  /// Limpia y formatea un número de celular colombiano al estándar internacional 57XXXXXXXXXX
  static String formatearNumeroColombia(String numero) {
    final limpio = numero.replaceAll(RegExp(r'[^\d]'), '');
    if (limpio.isEmpty) return '';

    if (limpio.startsWith('57') && limpio.length == 12) {
      return limpio;
    }
    if (limpio.length == 10) {
      return '57$limpio';
    }
    return limpio;
  }

  /// Genera la URL pública de tracking web para el viaje
  static String generarUrlWebTracking(String viajeId, {String baseUrl = defaultBaseUrl}) {
    final cleanId = viajeId.trim();
    final cleanBase = baseUrl.endsWith('/') ? baseUrl.substring(0, baseUrl.length - 1) : baseUrl;
    return '$cleanBase/t/$cleanId';
  }

  /// Construye el mensaje formal y enriquecido de WhatsApp para el pasajero que aborda en bahía
  static String construirMensajeDespacho({
    required String bahiaNombre,
    required String placa,
    required String conductor,
    required String destino,
    required double valorTotal,
    required String urlTracking,
  }) {
    final valorFormateado = valorTotal.toStringAsFixed(0).replaceAllMapped(
          RegExp(r'(\d{1,3})(?=(\d{3})+(?!\d))'),
          (Match m) => '${m[1]}.',
        );

    return '''🚕 *¡Tu Taxi Formal en Bahía $bahiaNombre está listo!*

📋 *Datos de Seguridad de tu Servicio:*
• *Vehículo:* $placa
• *Conductor:* $conductor
• *Destino:* $destino
• *Tarifa Oficial Decretada:* \$$valorFormateado COP

🔒 *Monitorea tu viaje y accede a tu ticket digital aquí:*
$urlTracking

_Gracias por viajar seguro con la red de Taxi Formal._''';
  }

  /// Genera el enlace directo para disparar la API de WhatsApp
  static String generarUrlWhatsApp({
    required String telefono,
    required String mensaje,
  }) {
    final telFormateado = formatearNumeroColombia(telefono);
    final mensajeEncoded = Uri.encodeComponent(mensaje);
    return 'https://api.whatsapp.com/send?phone=$telFormateado&text=$mensajeEncoded';
  }
}
