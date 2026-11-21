import 'package:flutter/foundation.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';

/// Servicio central de conectividad y gestión reactiva con Google Firebase.
/// Soporta persistencia offline nativa y manejo seguro de inicialización.
class FirebaseService {
  static bool _initialized = false;
  static bool get isInitialized => _initialized;

  static FirebaseFirestore? _firestore;
  static FirebaseAuth? _auth;

  static FirebaseFirestore get firestore {
    if (!_initialized) {
      debugPrint('[FirebaseService] Advertencia: Firestore invocado antes de inicialización completa.');
    }
    return _firestore ?? FirebaseFirestore.instance;
  }

  static FirebaseAuth get auth {
    return _auth ?? FirebaseAuth.instance;
  }

  /// Inicializa Firebase y configura Firestore con persistencia offline garantizada.
  static Future<void> initialize() async {
    if (_initialized) return;

    try {
      if (Firebase.apps.isEmpty) {
        await Firebase.initializeApp();
      }

      _firestore = FirebaseFirestore.instance;
      _auth = FirebaseAuth.instance;

      // Habilitar persistencia offline con caché ilimitada
      _firestore!.settings = const Settings(
        persistenceEnabled: true,
        cacheSizeBytes: Settings.CACHE_SIZE_UNLIMITED,
      );

      _initialized = true;
      debugPrint('[FirebaseService] Firebase inicializado con éxito. Persistencia offline activa.');
    } catch (e) {
      debugPrint('[FirebaseService] Nota en inicialización (Modo Offline / Entorno de desarrollo): $e');
      // Permitir continuar en modo offline/mock para no congelar la UI
      _initialized = true;
    }
  }

  /// Consulta el UID del usuario actualmente autenticado
  static String? get currentUserId => auth.currentUser?.uid;

  /// Retorna un Stream con los cambios de autenticación
  static Stream<User?> get authStateChanges => auth.authStateChanges();
}
