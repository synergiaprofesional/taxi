import 'package:flutter/material.dart';

/// Paleta de colores institucional para Synergia Móvil
/// Diseñada con estética ejecutiva de movilidad:
/// - Modo Oscuro: Fondos Slate profundos para turno nocturno y oficina.
/// - Modo Claro: Fondos Slate claros con alto contraste para exteriores con sol.
class AppColors {
  // Paleta Oscura (Dark Mode)
  static const Color darkBackground = Color(0xFF0F172A);      // Slate 900
  static const Color darkSurface = Color(0xFF1E293B);         // Slate 800
  static const Color darkSurfaceElevated = Color(0xFF334155); // Slate 700
  static const Color darkCardBorder = Color(0xFF475569);      // Slate 600
  static const Color darkTextPrimary = Color(0xFFF8FAFC);
  static const Color darkTextSecondary = Color(0xFF94A3B8);
  static const Color darkTextMuted = Color(0xFF64748B);

  // Paleta Clara (Light Mode)
  static const Color lightBackground = Color(0xFFF1F5F9);     // Slate 100
  static const Color lightSurface = Color(0xFFFFFFFF);        // Blanco puro
  static const Color lightSurfaceElevated = Color(0xFFE2E8F0); // Slate 200
  static const Color lightCardBorder = Color(0xFFCBD5E1);     // Slate 300
  static const Color lightTextPrimary = Color(0xFF0F172A);    // Slate 900
  static const Color lightTextSecondary = Color(0xFF475569);  // Slate 600
  static const Color lightTextMuted = Color(0xFF64748B);

  // Identidad Cromática Oficial del Gremio de Taxistas (Amarillo y Negro)
  static const Color taxiYellow = Color(0xFFF59E0B);         // Amarillo Taxi Oficial / Ámbar 500
  static const Color taxiYellowLight = Color(0xFFFBBF24);    // Amarillo Taxi Brillante / Ámbar 400
  static const Color taxiYellowDark = Color(0xFFD97706);     // Amarillo Taxi Dorado / Ámbar 600
  static const Color taxiBlack = Color(0xFF0F172A);          // Negro Carbón Asfalto / Slate 900
  static const Color taxiBlackPure = Color(0xFF000000);      // Negro Puro (Para tipografía sobre Amarillo)
  static const Color taxiBlackSoft = Color(0xFF1E293B);      // Negro Grafito / Slate 800

  // Primarios y Acentos Institucionales
  static const Color primary = taxiYellow;                   // Amarillo Taxi Institucional
  static const Color primaryHover = taxiYellowDark;          // Ámbar 600
  static const Color primaryDark = Color(0xFFB45309);        // Ámbar 700
  static const Color secondary = Color(0xFF0EA5E9);          // Sky 500 (Operaciones / Despacho)
  static const Color accent = taxiYellowLight;

  // Estados de Turno
  static const Color turnEspera = Color(0xFF64748B);         // Gris / Espera
  static const Color turnActual = taxiYellow;                // Amarillo Taxi / Turno Actual en Bahía
  static const Color turnSiguiente = Color(0xFF3B82F6);      // Azul / Siguiente en fila
  static const Color turnDespachado = Color(0xFF10B981);     // Verde Esmeralda / Despachado
  static const Color turnCancelado = Color(0xFFEF4444);      // Rojo / Cancelado

  // Compatibilidad hacia atrás (por defecto oscuro)
  static const Color background = darkBackground;
  static const Color surface = darkSurface;
  static const Color surfaceElevated = darkSurfaceElevated;
  static const Color cardBorder = darkCardBorder;
  static const Color textPrimary = darkTextPrimary;
  static const Color textSecondary = darkTextSecondary;
  static const Color textMuted = darkTextMuted;

  // Estados del Sistema
  static const Color success = Color(0xFF10B981);
  static const Color warning = Color(0xFFF59E0B);
  static const Color error = Color(0xFFEF4444);
  static const Color info = Color(0xFF0EA5E9);

  // Paleta WhatsApp Fiel — Modo Oscuro
  static const Color waDarkBackground = Color(0xFF0B141A);
  static const Color waDarkSurface = Color(0xFF111B21);
  static const Color waDarkSearchField = Color(0xFF20272B);
  static const Color waDarkTextPrimary = Color(0xFFE9EDEF);
  static const Color waDarkTextSecondary = Color(0xFF8696A0);
  static const Color waDarkDivider = Color(0xFF222D34);
  static const Color waDarkActiveGreen = Color(0xFF00A884);
  static const Color waDarkBadgeGreen = Color(0xFF25D366);

  // Paleta WhatsApp Fiel — Modo Claro
  static const Color waLightBackground = Color(0xFFFFFFFF);
  static const Color waLightSurface = Color(0xFFFFFFFF);
  static const Color waLightSearchField = Color(0xFFF0F2F5);
  static const Color waLightTextPrimary = Color(0xFF111B21);
  static const Color waLightTextSecondary = Color(0xFF667781);
  static const Color waLightDivider = Color(0xFFE9EDEF);
  static const Color waLightActiveGreen = Color(0xFF008069);
  static const Color waLightBadgeGreen = Color(0xFF25D366);
  static const Color waCheckBlue = Color(0xFF53BDEB);
}
