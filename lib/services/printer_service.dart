import 'dart:convert';
import 'dart:io';
import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';
import 'package:http/http.dart' as http;
import 'package:http/io_client.dart';
import 'package:intl/intl.dart';
import '../core/config/app_version.dart';
import '../core/utils/local_storage.dart';
import '../models/printer_config_model.dart';
import '../models/ticket_data_model.dart';

class PrinterService {
  PrinterConfigModel config = const PrinterConfigModel();

  // Comandos ESC/POS estándar
  static const int esc = 0x1B;
  static const int gs = 0x1D;

  // Formato de moneda
  final NumberFormat _currencyFormat =
      NumberFormat.currency(locale: 'es_CO', symbol: '\$', decimalDigits: 0);
  final DateFormat _dateFormat = DateFormat('dd/MM/yyyy HH:mm:ss');

  static String _storageKeyForUser(String user) {
    final sanitizedUser = user.trim().toLowerCase();
    return 'user_pref_${sanitizedUser}_printer_config';
  }

  void updateConfig(PrinterConfigModel newConfig, {String? user}) {
    config = newConfig;
    if (user != null && user.trim().isNotEmpty) {
      saveUserConfig(user, newConfig);
    }
  }

  /// Guarda la configuración de impresión de forma persistente para el usuario
  Future<void> saveUserConfig(String user, PrinterConfigModel newConfig) async {
    config = newConfig;
    if (user.trim().isEmpty) return;
    try {
      final key = _storageKeyForUser(user);
      final jsonString = jsonEncode(newConfig.toJson());
      await LocalStorage.setString(key, jsonString);
      debugPrint('[PrinterService] Configuración guardada para "$user" ($key): $jsonString');
    } catch (e) {
      debugPrint('[PrinterService] Error guardando configuración para "$user": $e');
    }
  }

  /// Carga la configuración de impresión persistida para el usuario
  Future<PrinterConfigModel> loadUserConfig(String user) async {
    if (user.trim().isEmpty) return config;
    try {
      final key = _storageKeyForUser(user);
      final raw = LocalStorage.getString(key);
      if (raw != null && raw.isNotEmpty) {
        final decoded = jsonDecode(raw) as Map<String, dynamic>;
        config = PrinterConfigModel.fromJson(decoded);
        debugPrint('[PrinterService] Configuración cargada para "$user": ${config.nombreODireccion} (${config.anchoPapel}mm)');
        return config;
      }
    } catch (e) {
      debugPrint('[PrinterService] Error al cargar configuración para "$user": $e');
    }
    return config;
  }

  String _limpiarTextoAscii(String texto) {
    return texto
        .replaceAll('á', 'a')
        .replaceAll('é', 'e')
        .replaceAll('í', 'i')
        .replaceAll('ó', 'o')
        .replaceAll('ú', 'u')
        .replaceAll('Á', 'A')
        .replaceAll('É', 'E')
        .replaceAll('Í', 'I')
        .replaceAll('Ó', 'O')
        .replaceAll('Ú', 'U')
        .replaceAll('ñ', 'n')
        .replaceAll('Ñ', 'N')
        .replaceAll('¡', '')
        .replaceAll('¿', '');
  }

  String _extraerTurnoEnUnaLinea(String rawTurno) {
    var limpio = rawTurno.trim();
    if (limpio.contains('[')) {
      limpio = limpio.split('[')[0].trim();
    }
    // Remover prefijos repetidos tipo "TURNO", "TURNO:", "TURNO #"
    limpio = limpio.replaceFirst(RegExp(r'^TURNO\s*:?\s*#?\s*', caseSensitive: false), '').trim();
    return limpio.toUpperCase();
  }

  /// Genera la representación en texto formateado para pantalla / emulador
  String generarTextoTiquete(TicketDataModel ticket) {
    final ancho = config.anchoPapel == 80 ? 48 : 32;
    final separador = '=' * ancho;
    final subSeparador = '-' * ancho;

    final buffer = StringBuffer();
    buffer.writeln(_centrar(_limpiarTextoAscii(ticket.empresaNombre), ancho));
    buffer.writeln(_centrar(_limpiarTextoAscii(ticket.nit), ancho));
    buffer.writeln(_centrar('BAHIA: ${_limpiarTextoAscii(ticket.bahiaNombre.toUpperCase())}', ancho));
    buffer.writeln(subSeparador);
    
    // Descripción y turno en una sola línea
    final turnoLinea = _extraerTurnoEnUnaLinea(ticket.turnoNumero);
    buffer.writeln(_centrar('TURNO: $turnoLinea', ancho));
    // Siguiente línea: Nombre del conductor
    buffer.writeln(_centrar(_limpiarTextoAscii(ticket.conductor.trim().toUpperCase()), ancho));
    buffer.writeln(separador);

    buffer.writeln(_formatearLinea('PLACA:', _limpiarTextoAscii(ticket.placa), ancho));
    buffer.writeln(_formatearLinea('MOVIL / INTERNO:', _limpiarTextoAscii(ticket.movilNumero), ancho));
    buffer.writeln(_formatearLinea('CONDUCTOR:', _limpiarTextoAscii(ticket.conductor), ancho));
    if (ticket.destino.isNotEmpty) {
      buffer.writeln(_formatearLinea('DESTINO:', _limpiarTextoAscii(ticket.destino), ancho));
    }
    if (ticket.direccion.isNotEmpty) {
      buffer.writeln(_formatearLinea('DIRECCION:', _limpiarTextoAscii(ticket.direccion), ancho));
    }
    buffer.writeln(_formatearLinea('FECHA/HORA (COT):', _dateFormat.format(ticket.fechaHora), ancho));
    buffer.writeln(_formatearLinea('CAJERO:', _limpiarTextoAscii(ticket.cajero), ancho));
    buffer.writeln(subSeparador);
    buffer.writeln(_formatearLinea('TOTAL RECAUDADO:', _currencyFormat.format(ticket.valorTotal), ancho));
    buffer.writeln(subSeparador);
    buffer.writeln(_centrar(_limpiarTextoAscii(ticket.pieMensaje), ancho));
    buffer.writeln(_centrar('Verificacion: [SYNERGIA-OK]', ancho));
    buffer.writeln(_centrar(AppVersion.ticketFooter, ancho));
    buffer.writeln('\n\n'); // Avance final
    return buffer.toString();
  }

  /// Genera los bytes binarios ESC/POS para impresoras térmicas reales
  Uint8List generarBytesEscPos(TicketDataModel ticket) {
    final List<int> bytes = [];

    // Inicializar impresora (ESC @)
    bytes.addAll([esc, 0x40]);

    // Centrar encabezado (ESC a 1)
    bytes.addAll([esc, 0x61, 0x01]);
    bytes.addAll([esc, 0x45, 0x01]); // Negrita activada
    bytes.addAll(latin1.encode('${_limpiarTextoAscii(ticket.empresaNombre)}\n'));
    bytes.addAll([esc, 0x45, 0x00]); // Negrita desactivada
    bytes.addAll(latin1.encode('${_limpiarTextoAscii(ticket.nit)}\n'));
    bytes.addAll(latin1.encode('BAHIA: ${_limpiarTextoAscii(ticket.bahiaNombre)}\n'));
    bytes.addAll(latin1.encode('--------------------------------\n'));

    // 1. DESCRIPCIÓN Y NÚMERO DE TURNO EN UNA LÍNEA (Doble alto para destacar sin partirse en el ancho)
    final turnoLinea = _extraerTurnoEnUnaLinea(ticket.turnoNumero);
    bytes.addAll([gs, 0x21, 0x01]); // Doble alto (0x01), ancho normal
    bytes.addAll([esc, 0x45, 0x01]); // Negrita
    bytes.addAll(latin1.encode('TURNO: $turnoLinea\n'));

    // 2. SIGUIENTE LÍNEA: NOMBRE DEL CONDUCTOR EN FUENTE B (REDUCIDA)
    bytes.addAll([gs, 0x21, 0x00]); // Tamaño estándar
    bytes.addAll([esc, 0x4D, 0x01]); // Fuente B (reducida/condensada 9x17)
    bytes.addAll([esc, 0x45, 0x01]); // Negrita para visibilidad
    bytes.addAll(latin1.encode('${_limpiarTextoAscii(ticket.conductor.trim().toUpperCase())}\n'));
    bytes.addAll([esc, 0x45, 0x00]); // Desactivar negrita
    bytes.addAll([esc, 0x4D, 0x00]); // Restablecer a Fuente A estándar

    bytes.addAll(latin1.encode('================================\n'));

    // Alinear izquierda (ESC a 0)
    bytes.addAll([esc, 0x61, 0x00]);
    bytes.addAll(latin1.encode('PLACA:     ${_limpiarTextoAscii(ticket.placa)}\n'));
    bytes.addAll(latin1.encode('MOVIL:     ${_limpiarTextoAscii(ticket.movilNumero)}\n'));
    bytes.addAll(latin1.encode('CONDUCTOR: ${_limpiarTextoAscii(ticket.conductor)}\n'));
    if (ticket.destino.isNotEmpty) {
      bytes.addAll(latin1.encode('DESTINO:   ${_limpiarTextoAscii(ticket.destino)}\n'));
    }
    if (ticket.direccion.isNotEmpty) {
      bytes.addAll(latin1.encode('DIRECCION: ${_limpiarTextoAscii(ticket.direccion)}\n'));
    }
    bytes.addAll(latin1.encode('FECHA:     ${_dateFormat.format(ticket.fechaHora)}\n'));
    bytes.addAll(latin1.encode('OPERADOR:  ${_limpiarTextoAscii(ticket.cajero)}\n'));
    bytes.addAll(latin1.encode('--------------------------------\n'));

    // Valor Total con formato limpio $ XX.XXX
    bytes.addAll([esc, 0x45, 0x01]);
    final valorFormateado = NumberFormat('#,###', 'es_CO').format(ticket.valorTotal);
    bytes.addAll(latin1.encode('TOTAL PAGADO: \$ $valorFormateado\n'));
    bytes.addAll([esc, 0x45, 0x00]);
    bytes.addAll(latin1.encode('--------------------------------\n'));

    // Centrar pie
    bytes.addAll([esc, 0x61, 0x01]);
    bytes.addAll(latin1.encode('${_limpiarTextoAscii(ticket.pieMensaje)}\n'));
    bytes.addAll(latin1.encode('[SYNERGIA MOVIL MULTIPLATAFORMA]\n'));
    bytes.addAll(latin1.encode('${AppVersion.ticketFooter}\n'));

    // Avance de papel de 3 líneas (ESC d 3)
    bytes.addAll([esc, 0x64, 0x03]);

    // Corte de papel automático (GS V 66 0)
    if (config.autoCorte) {
      bytes.addAll([gs, 0x56, 0x42, 0x00]);
    }

    return Uint8List.fromList(bytes);
  }

  /// Envía la impresión según el tipo configurado
  static const MethodChannel _bluetoothChannel =
      MethodChannel('com.synergia.synergia_movil/bluetooth_printer');

  Future<bool> _imprimirBluetoothAndroid(Uint8List bytes, String macAddress) async {
    if (!kIsWeb && Platform.isAndroid) {
      try {
        final res = await _bluetoothChannel.invokeMethod<bool>('printBytes', {
          'address': macAddress,
          'bytes': bytes,
        }).timeout(const Duration(seconds: 5));
        return res ?? false;
      } on PlatformException catch (pe) {
        debugPrint('[PrinterService] Error en canal nativo Bluetooth: ${pe.message}');
        return false;
      } on MissingPluginException {
        debugPrint('[PrinterService] Canal nativo Bluetooth no disponible');
        return false;
      } catch (e) {
        debugPrint('[PrinterService] Excepción al imprimir vía Bluetooth: $e');
        return false;
      }
    }
    debugPrint('[PrinterService] Impresión Bluetooth solo soportada en Android.');
    return false;
  }

  Future<bool> imprimirTicket(TicketDataModel ticket) async {
    try {
      final bytes = generarBytesEscPos(ticket);
      debugPrint('[PrinterService] Generados ${bytes.length} bytes ESC/POS para turno ${ticket.turnoNumero}');

      switch (config.tipo) {
        case TipoImpresora.emulador:
          debugPrint('[PrinterService] Impresión en Emulador completada con éxito.');
          return true;
        case TipoImpresora.bluetooth:
          debugPrint('[PrinterService] [Android] Enviando a Bluetooth MAC: ${config.nombreODireccion}');
          final ok = await _imprimirBluetoothAndroid(bytes, config.nombreODireccion);
          if (!ok) {
            debugPrint('[PrinterService] Falló impresión física Bluetooth o dispositivo no alcanzable.');
          }
          return ok;
        case TipoImpresora.spoolerWindows:
          debugPrint('[PrinterService] [Windows] Enviando bytes reales a Spooler: ${config.nombreODireccion}');
          return await _imprimirSpoolerWindows(bytes, config.nombreODireccion);
        case TipoImpresora.tcp:
          debugPrint('[PrinterService] Enviando a Impresora Wi-Fi/TCP ${config.nombreODireccion}:${config.puerto}');
          return await _imprimirTcpSocket(bytes, config.nombreODireccion, config.puerto);
        case TipoImpresora.url:
          debugPrint('[PrinterService] Enviando a Servicio URL: ${config.nombreODireccion}');
          return await _imprimirPorUrl(ticket, config.nombreODireccion);
      }
    } catch (e) {
      debugPrint('[PrinterService] Error al imprimir: $e');
      return false;
    }
  }

  /// Conexión e inyección directa de bytes ESC/POS vía socket TCP (para impresoras Wi-Fi / LAN port 9100)
  Future<bool> _imprimirTcpSocket(Uint8List bytes, String host, int port) async {
    final cleanHost = host.trim();
    if (cleanHost.isEmpty) {
      debugPrint('[PrinterService] Host/IP de impresora Wi-Fi vacío');
      return false;
    }
    try {
      final socket = await Socket.connect(cleanHost, port, timeout: const Duration(seconds: 4));
      socket.add(bytes);
      await socket.flush();
      await socket.close();
      debugPrint('[PrinterService] Impresión Wi-Fi completada en $cleanHost:$port');
      return true;
    } catch (e) {
      debugPrint('[PrinterService] Error conectando a impresora Wi-Fi ($cleanHost:$port): $e');
      return false;
    }
  }

  String _generarHtmlTiquete(TicketDataModel ticket) {
    final turnoLinea = _extraerTurnoEnUnaLinea(ticket.turnoNumero);
    final valorFormateado = NumberFormat('#,###', 'es_CO').format(ticket.valorTotal);
    return '''
<html>
<body style="font-family: monospace; font-size: 11px; margin: 0; padding: 2px;">
  <div style="text-align: center;">
    <b>${_limpiarTextoAscii(ticket.empresaNombre)}</b><br>
    ${_limpiarTextoAscii(ticket.nit)}<br>
    BAHIA: ${_limpiarTextoAscii(ticket.bahiaNombre.toUpperCase())}<br>
    <hr style="border: none; border-top: 1px dashed #000; margin: 4px 0;">
    <span style="font-size: 14px; font-weight: 900;">TURNO: $turnoLinea</span><br>
    <span style="font-size: 9px; font-weight: bold;">${_limpiarTextoAscii(ticket.conductor.trim().toUpperCase())}</span>
    <hr style="border: none; border-top: 1px solid #000; margin: 4px 0;">
  </div>
  <table style="width: 100%; font-size: 10px; border-collapse: collapse;">
    <tr><td><b>PLACA:</b></td><td>${_limpiarTextoAscii(ticket.placa)}</td></tr>
    <tr><td><b>MOVIL:</b></td><td>${_limpiarTextoAscii(ticket.movilNumero)}</td></tr>
    <tr><td><b>CONDUCTOR:</b></td><td>${_limpiarTextoAscii(ticket.conductor)}</td></tr>
    ${ticket.destino.isNotEmpty ? '<tr><td><b>DESTINO:</b></td><td>${_limpiarTextoAscii(ticket.destino)}</td></tr>' : ''}
    ${ticket.direccion.isNotEmpty ? '<tr><td><b>DIRECCION:</b></td><td>${_limpiarTextoAscii(ticket.direccion)}</td></tr>' : ''}
    <tr><td><b>FECHA:</b></td><td>${_dateFormat.format(ticket.fechaHora)}</td></tr>
    <tr><td><b>OPERADOR:</b></td><td>${_limpiarTextoAscii(ticket.cajero)}</td></tr>
  </table>
  <hr style="border: none; border-top: 1px dashed #000; margin: 4px 0;">
  <div style="text-align: left; font-weight: bold; font-size: 12px;">
    TOTAL: \$ $valorFormateado
  </div>
  <hr style="border: none; border-top: 1px dashed #000; margin: 4px 0;">
  <div style="text-align: center; font-size: 9px;">
    ${_limpiarTextoAscii(ticket.pieMensaje)}<br>
    [SYNERGIA MOVIL MULTIPLATAFORMA]
  </div>
</body>
</html>
''';
  }

  bool _esDireccionLocal(String host) {
    final h = host.toLowerCase().trim();
    return h == 'localhost' ||
        h == '127.0.0.1' ||
        h.startsWith('192.168.') ||
        h.startsWith('10.') ||
        h.startsWith('172.16.') ||
        h.startsWith('172.17.') ||
        h.startsWith('172.18.') ||
        h.startsWith('172.19.') ||
        h.startsWith('172.20.') ||
        h.startsWith('172.21.') ||
        h.startsWith('172.22.') ||
        h.startsWith('172.23.') ||
        h.startsWith('172.24.') ||
        h.startsWith('172.25.') ||
        h.startsWith('172.26.') ||
        h.startsWith('172.27.') ||
        h.startsWith('172.28.') ||
        h.startsWith('172.29.') ||
        h.startsWith('172.30.') ||
        h.startsWith('172.31.');
  }

  http.Client _createHttpClient() {
    if (kIsWeb) return http.Client();
    final ioClient = HttpClient();
    ioClient.badCertificateCallback = (X509Certificate cert, String host, int port) => true;
    ioClient.connectionTimeout = const Duration(seconds: 5);
    return IOClient(ioClient);
  }

  /// Envía el tiquete a un servicio HTTP/HTTPS público o local (PC con impresora térmica)
  Future<bool> _imprimirPorUrl(TicketDataModel ticket, String urlBase) async {
    final cleanUrl = urlBase.trim();
    if (cleanUrl.isEmpty) {
      debugPrint('[PrinterService] URL de impresión vacía');
      return false;
    }

    final client = _createHttpClient();
    try {
      final parsed = Uri.parse(cleanUrl.startsWith('http') ? cleanUrl : 'http://$cleanUrl');

      // 1. Soporte directo para C:\proxyServer (puerto 4000, 443, 80 o IPs locales de red)
      final esProxyServer = parsed.port == 4000 ||
          parsed.path.contains('hw_proxy') ||
          _esDireccionLocal(parsed.host);

      if (esProxyServer) {
        // A) Intentar primero endpoint RAW directo (calidad nativa, tamaño real 80mm sin PDF)
        try {
          final endpointRaw = parsed.path.contains('print_raw')
              ? parsed
              : parsed.replace(path: '/hw_proxy/print_raw');
          final rawBytes = generarBytesEscPos(ticket);
          debugPrint('[PrinterService] Detectado proxy local/Caddy: enviando RAW (${rawBytes.length} bytes) a $endpointRaw');
          final rawPayload = {
            'params': {
              'bytes_base64': base64Encode(rawBytes),
              'printer': 'TIQUETES',
            },
          };
          final rawResp = await client.post(
            endpointRaw,
            headers: {'Content-Type': 'application/json'},
            body: jsonEncode(rawPayload),
          ).timeout(const Duration(seconds: 5));
          debugPrint('[PrinterService] Respuesta proxy RAW: código ${rawResp.statusCode}');
          if (rawResp.statusCode >= 200 && rawResp.statusCode < 300) {
            return true;
          }
        } catch (e) {
          debugPrint('[PrinterService] Fallback a print_xml_receipt: $e');
        }

        // B) Fallback a print_xml_receipt (si print_raw no responde o proxy antiguo)
        try {
          final endpointProxy = parsed.path.contains('print_xml_receipt')
              ? parsed
              : parsed.replace(path: '/hw_proxy/print_xml_receipt');
          debugPrint('[PrinterService] Enviando HTML fallback a $endpointProxy');
          final proxyPayload = {
            'params': {
              'receipt': {
                'html': _generarHtmlTiquete(ticket),
                'impresora': {
                  'zoom': 1.35,
                  'page_width': 80,
                  'mt': 0,
                  'mb': 0,
                  'mr': 0,
                  'ml': 0,
                },
              },
            },
          };
          final proxyResp = await client.post(
            endpointProxy,
            headers: {'Content-Type': 'application/json'},
            body: jsonEncode(proxyPayload),
          ).timeout(const Duration(seconds: 6));
          debugPrint('[PrinterService] Respuesta proxy HTML: código ${proxyResp.statusCode}');
          if (proxyResp.statusCode >= 200 && proxyResp.statusCode < 300) {
            return true;
          }
        } catch (e) {
          debugPrint('[PrinterService] Error en print_xml_receipt fallback: $e');
        }
      }

      final payload = {
        'id': ticket.turnoId,
        'turno': ticket.turnoNumero,
        'consecutivo': ticket.turnoNumero,
        'placa': ticket.placa,
        'conductor': ticket.conductor,
        'bahia': ticket.bahiaNombre,
        'destino': ticket.destino,
        'tarifa': ticket.destino,
        'direccion': ticket.direccion,
        'nota': ticket.direccion,
        'valor': ticket.valorTotal,
        'total': ticket.valorTotal,
        'cajero': ticket.cajero,
        'usuario': ticket.cajero,
        'fecha': _dateFormat.format(ticket.fechaHora),
        'fecha_iso': ticket.fechaHora.toIso8601String(),
        'ancho_papel': config.anchoPapel,
        'auto_corte': config.autoCorte,
        'texto_tiquete': generarTextoTiquete(ticket),
        'bytes_base64': base64Encode(generarBytesEscPos(ticket)),
      };

      final Map<String, String> qParams = Map.from(parsed.queryParameters);
      qParams['turno'] = ticket.turnoNumero;
      qParams['placa'] = ticket.placa;
      qParams['conductor'] = ticket.conductor;
      if (ticket.destino.isNotEmpty) qParams['destino'] = ticket.destino;
      if (ticket.direccion.isNotEmpty) qParams['direccion'] = ticket.direccion;
      qParams['total'] = ticket.valorTotal.toString();
      qParams['qcontext'] = jsonEncode(payload);

      final uriConQuery = parsed.replace(queryParameters: qParams);
      debugPrint('[PrinterService] Petición GET al servicio URL: $uriConQuery');

      final resp = await client.get(uriConQuery).timeout(const Duration(seconds: 6));
      debugPrint('[PrinterService] Respuesta del servicio URL: código ${resp.statusCode}');

      if (resp.statusCode >= 200 && resp.statusCode < 300) {
        return true;
      }

      // Fallback POST
      if (resp.statusCode == 405 || resp.statusCode == 404) {
        final postResp = await client.post(
          parsed,
          headers: {'Content-Type': 'application/json'},
          body: jsonEncode(payload),
        ).timeout(const Duration(seconds: 6));
        return postResp.statusCode >= 200 && postResp.statusCode < 300;
      }

      return false;
    } catch (e) {
      debugPrint('[PrinterService] Excepción al llamar al servicio URL de impresión: $e');
      return false;
    } finally {
      client.close();
    }
  }

  String _centrar(String texto, int ancho) {
    if (texto.length >= ancho) return texto.substring(0, ancho);
    final margen = (ancho - texto.length) ~/ 2;
    return ' ' * margen + texto;
  }

  String _formatearLinea(String etiqueta, String valor, int ancho) {
    final espacioDisponible = ancho - etiqueta.length - 1;
    if (espacioDisponible <= 0) return '$etiqueta $valor';
    final valorAjustado = valor.length > espacioDisponible
        ? valor.substring(0, espacioDisponible)
        : valor;
    final padding = ancho - etiqueta.length - valorAjustado.length;
    return etiqueta + (' ' * (padding > 0 ? padding : 1)) + valorAjustado;
  }

  /// Inyección directa de bytes ESC/POS al spooler Win32 de Windows
  Future<bool> _imprimirSpoolerWindows(Uint8List bytes, String printerName) async {
    if (kIsWeb || !Platform.isWindows) {
      debugPrint('[PrinterService] Impresión Spooler solo disponible en Windows Desktop.');
      return false;
    }
    try {
      final pName = printerName.trim().isEmpty ? 'TIQUETES' : printerName.trim();
      final tempDir = Directory.systemTemp.path;
      final tempBin = File('$tempDir\\ticket_${DateTime.now().millisecondsSinceEpoch}.bin');
      await tempBin.writeAsBytes(bytes);

      // Ubicación canónica en scripts/ o en temp
      final workspaceScript = File('scripts/raw_print_windows.ps1');
      String scriptPath;
      if (workspaceScript.existsSync()) {
        scriptPath = workspaceScript.path;
      } else {
        scriptPath = '$tempDir\\raw_print_windows.ps1';
        if (!File(scriptPath).existsSync()) {
          await File(scriptPath).writeAsString(_rawPrinterPs1Content);
        }
      }

      final result = await Process.run(
        'powershell',
        [
          '-NoProfile',
          '-ExecutionPolicy',
          'Bypass',
          '-File',
          scriptPath,
          '-PrinterName',
          pName,
          '-FilePath',
          tempBin.path,
        ],
      );

      // Eliminar binario temporal
      try {
        if (tempBin.existsSync()) await tempBin.delete();
      } catch (_) {}

      if (result.exitCode == 0) {
        debugPrint('[PrinterService] [Windows] Impresión física exitosa en $pName');
        return true;
      } else {
        debugPrint('[PrinterService] [Windows] Error spooler: ${result.stderr}');
        return false;
      }
    } catch (e) {
      debugPrint('[PrinterService] [Windows] Excepción al enviar al spooler: $e');
      return false;
    }
  }

  static const String _rawPrinterPs1Content = r'''
param (
    [Parameter(Mandatory=$true)]
    [string]$PrinterName,

    [Parameter(Mandatory=$true)]
    [string]$FilePath
)

$code = @"
using System;
using System.IO;
using System.Runtime.InteropServices;

public class RawPrinterHelper
{
    [StructLayout(LayoutKind.Sequential, CharSet=CharSet.Ansi)]
    public class DOCINFOA
    {
        [MarshalAs(UnmanagedType.LPStr)] public string pDocName;
        [MarshalAs(UnmanagedType.LPStr)] public string pOutputFile;
        [MarshalAs(UnmanagedType.LPStr)] public string pDataType;
    }

    [DllImport("winspool.Drv", EntryPoint="OpenPrinterA", SetLastError=true, CharSet=CharSet.Ansi, ExactSpelling=true, CallingConvention=CallingConvention.StdCall)]
    public static extern bool OpenPrinter([MarshalAs(UnmanagedType.LPStr)] string szPrinter, out IntPtr hPrinter, IntPtr pd);

    [DllImport("winspool.Drv", EntryPoint="ClosePrinter", SetLastError=true, ExactSpelling=true, CallingConvention=CallingConvention.StdCall)]
    public static extern bool ClosePrinter(IntPtr hPrinter);

    [DllImport("winspool.Drv", EntryPoint="StartDocPrinterA", SetLastError=true, CharSet=CharSet.Ansi, ExactSpelling=true, CallingConvention=CallingConvention.StdCall)]
    public static extern bool StartDocPrinter(IntPtr hPrinter, int level, [In, MarshalAs(UnmanagedType.LPStruct)] DOCINFOA di);

    [DllImport("winspool.Drv", EntryPoint="EndDocPrinter", SetLastError=true, ExactSpelling=true, CallingConvention=CallingConvention.StdCall)]
    public static extern bool EndDocPrinter(IntPtr hPrinter);

    [DllImport("winspool.Drv", EntryPoint="StartPagePrinter", SetLastError=true, ExactSpelling=true, CallingConvention=CallingConvention.StdCall)]
    public static extern bool StartPagePrinter(IntPtr hPrinter);

    [DllImport("winspool.Drv", EntryPoint="EndPagePrinter", SetLastError=true, ExactSpelling=true, CallingConvention=CallingConvention.StdCall)]
    public static extern bool EndPagePrinter(IntPtr hPrinter);

    [DllImport("winspool.Drv", EntryPoint="WritePrinter", SetLastError=true, ExactSpelling=true, CallingConvention=CallingConvention.StdCall)]
    public static extern bool WritePrinter(IntPtr hPrinter, IntPtr pBytes, int dwCount, out int dwWritten);

    public static bool SendBytesToPrinter(string szPrinterName, byte[] pBytes)
    {
        IntPtr hPrinter = new IntPtr(0);
        DOCINFOA di = new DOCINFOA();
        bool bSuccess = false;

        di.pDocName = "Synergia Movil Ticket";
        di.pDataType = "RAW";

        if (OpenPrinter(szPrinterName.Normalize(), out hPrinter, IntPtr.Zero))
        {
            if (StartDocPrinter(hPrinter, 1, di))
            {
                if (StartPagePrinter(hPrinter))
                {
                    IntPtr pUnmanagedBytes = Marshal.AllocCoTaskMem(pBytes.Length);
                    Marshal.Copy(pBytes, 0, pUnmanagedBytes, pBytes.Length);
                    int dwWritten = 0;
                    bSuccess = WritePrinter(hPrinter, pUnmanagedBytes, pBytes.Length, out dwWritten);
                    Marshal.FreeCoTaskMem(pUnmanagedBytes);
                    EndPagePrinter(hPrinter);
                }
                EndDocPrinter(hPrinter);
            }
            ClosePrinter(hPrinter);
        }
        return bSuccess;
    }

    public static bool SendFileToPrinter(string szPrinterName, string szFileName)
    {
        byte[] bytes = File.ReadAllBytes(szFileName);
        return SendBytesToPrinter(szPrinterName, bytes);
    }
}
"@

Add-Type -TypeDefinition $code -Language CSharp

if (Test-Path $FilePath) {
    $result = [RawPrinterHelper]::SendFileToPrinter($PrinterName, $FilePath)
    if ($result) {
        Write-Output "SUCCESS: Sent $FilePath to $PrinterName"
        exit 0
    } else {
        Write-Error "ERROR: Failed to send raw data to $PrinterName"
        exit 1
    }
} else {
    Write-Error "File not found: $FilePath"
    exit 2
}
''';
}
