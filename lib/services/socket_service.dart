import 'package:flutter/foundation.dart';
import 'package:get/get.dart';
import 'package:socket_io_client/socket_io_client.dart' as io;

class SocketService extends GetxService {
  io.Socket? _socket;
  var isConnected = false.obs;
  var eventSequence = 0.obs;
  var lastEventName = ''.obs;
  var lastEventData = <String, dynamic>{}.obs;
  String serverUrl = 'http://fundetaxcol.co:3000';

  void conectar({String host = 'http://fundetaxcol.co:3000'}) {
    serverUrl = host;
    try {
      _socket?.dispose();

      _socket = io.io(
        host,
        io.OptionBuilder()
            .setTransports(['websocket', 'polling'])
            .enableAutoConnect()
            .enableReconnection()
            .setReconnectionAttempts(10)
            .setReconnectionDelay(3000)
            .build(),
      );

      _socket?.onConnect((_) {
        isConnected.value = true;
        debugPrint('[SocketService] Conectado a server_rt_odoo en $host');
      });

      _socket?.onReconnect((_) {
        isConnected.value = true;
        debugPrint('[SocketService] Reconectado a server_rt_odoo en $host');
      });

      _socket?.onReconnectAttempt((attempt) {
        debugPrint('[SocketService] Reintento de conexión ($attempt) a server_rt_odoo...');
      });

      _socket?.onDisconnect((_) {
        isConnected.value = false;
        debugPrint('[SocketService] Desconectado de server_rt_odoo');
      });

      _socket?.onConnectError((err) {
        isConnected.value = false;
        debugPrint('[SocketService] Error de conexión socket: $err');
      });

      _socket?.connect();

      void handleEvent(String name, dynamic data) {
        lastEventName.value = name;
        eventSequence.value++;
        if (data is Map) {
          lastEventData.value = Map<String, dynamic>.from(data);
        }
        debugPrint('[SocketService] Evento recibido (#${eventSequence.value}): $name');
      }

      _socket?.on('turn', (data) => handleEvent('turn', data));
      _socket?.on('dispatch', (data) => handleEvent('dispatch', data));
      _socket?.on('session', (data) => handleEvent('session', data));
      _socket?.on('payment', (data) => handleEvent('payment', data));
      _socket?.on('turnId', (data) => handleEvent('turnId', data));
      _socket?.on('dispatchId', (data) => handleEvent('dispatchId', data));
      _socket?.on('paymentId', (data) => handleEvent('paymentId', data));
      _socket?.on('sessionId', (data) => handleEvent('sessionId', data));
      _socket?.on('new_turno', (data) => handleEvent('new_turno', data));
      _socket?.on('update_turno', (data) => handleEvent('update_turno', data));
      _socket?.on('dispatch_turno', (data) => handleEvent('dispatch_turno', data));
    } catch (e) {
      isConnected.value = false;
      debugPrint('[SocketService] Excepción al inicializar socket: $e');
    }
  }

  void emitirEvento(String evento, Map<String, dynamic> datos) {
    if (isConnected.value && _socket != null) {
      _socket?.emit(evento, datos);
    } else {
      debugPrint('[SocketService] Socket desconectado. Evento $evento encolado localmente.');
    }
  }

  void reconnect({String? host}) {
    debugPrint('[SocketService] Forzando reconexión manual a server_rt_odoo...');
    desconectar();
    conectar(host: host ?? serverUrl);
  }

  void desconectar() {
    _socket?.disconnect();
    _socket?.dispose();
    _socket = null;
    isConnected.value = false;
  }
}
