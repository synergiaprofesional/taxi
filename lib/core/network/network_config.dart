/// Gestor centralizado y robusto de URLs para Synergia Móvil.
/// Resuelve de forma definitiva los vicios de concatenación ('http://https://...')
/// y provee URLs válidas para APIs REST, JSON-RPC y WebSockets.
class NetworkConfig {
  String _host;
  bool _useHttps;
  int _port;

  NetworkConfig({
    String host = 'fundetaxcol.co',
    bool useHttps = false,
    int? port,
  })  : _host = sanitizeHost(host),
        _useHttps = useHttps,
        _port = port ?? (useHttps ? 443 : 80);

  String get rawHost => _host;
  bool get useHttps => _useHttps;
  int get port => _port;

  void updateHost(String newHost) {
    _host = sanitizeHost(newHost);
  }

  void setUseHttps(bool value) {
    _useHttps = value;
    if (_port == 80 && value) {
      _port = 443;
    } else if (_port == 443 && !value) {
      _port = 80;
    }
  }

  void setPort(int newPort) {
    _port = newPort;
  }

  /// Construye una URL completa a partir de un endpoint relativo.
  String buildUrl(String endpoint) {
    final base = buildBaseUrl(host: _host, port: _port, isSecure: _useHttps);
    final cleanEndpoint = endpoint.startsWith('/') ? endpoint : '/$endpoint';
    return '$base$cleanEndpoint';
  }

  /// Limpia y normaliza el nombre de host o IP.
  /// Remueve cualquier protocolo previo ('http://', 'https://') y barras finales.
  static String sanitizeHost(String rawHost) {
    String clean = rawHost.trim();
    clean = clean.replaceFirst(RegExp(r'^https?:\/\/', caseSensitive: false), '');
    clean = clean.replaceAll(RegExp(r'\/.*$'), ''); // Remueve rutas accidentales
    return clean.isEmpty ? 'fundetaxcol.co' : clean;
  }

  /// Construye la URL Base para HTTP o HTTPS.
  /// Omite el puerto si es el estándar (80 para http, 443 para https).
  static String buildBaseUrl({
    required String host,
    required int port,
    bool isSecure = false,
  }) {
    final cleanHost = sanitizeHost(host);
    final scheme = isSecure ? 'https' : 'http';

    // Si es puerto estándar según el esquema, omitir el sufijo de puerto
    if ((isSecure && port == 443) || (!isSecure && port == 80)) {
      return '$scheme://$cleanHost';
    }

    return '$scheme://$cleanHost:$port';
  }

  /// Construye la URL para conexión a WebSockets (Socket.IO).
  /// Si isSecure es true, utiliza 'wss://' o 'https://' a través del proxy inverso.
  static String buildSocketUrl({
    required String host,
    required int portSocket,
    bool isSecure = true,
  }) {
    final cleanHost = sanitizeHost(host);

    if (isSecure) {
      // Con Caddy reverse proxy, el socket viaja sobre HTTPS/WSS estándar
      return 'https://$cleanHost';
    } else {
      // Conexión legacy directa por puerto no cifrado
      return 'http://$cleanHost:$portSocket';
    }
  }
}
