class AppVersion {
  static const String versionName = '3.0.0';
  static const int versionCode = 1;
  static const String environment = 'Producción Taxi - Firebase Cloud';

  /// Retorna formato formal con build, ej: "v3.0.0+1"
  static String get display => 'v$versionName+$versionCode';

  /// Retorna formato corto, ej: "v3.0.0"
  static String get shortDisplay => 'v$versionName';

  /// Texto estampado en el pie de los tiquetes térmicos impresos
  static String get ticketFooter => 'Taxi $display - Sistema Oficial';
}
