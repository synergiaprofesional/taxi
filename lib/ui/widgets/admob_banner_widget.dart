import 'package:flutter/material.dart';
import 'package:google_mobile_ads/google_mobile_ads.dart';
import '../../core/theme/app_colors.dart';

/// Widget de Banner AdMob con Enclavamiento de Seguridad Vial
/// Regla Inviolable: Si el móvil está en carrera activa o en movimiento, el banner se inhibe.
class AdmobBannerWidget extends StatefulWidget {
  final bool isInActiveRide;
  final String adUnitId;

  const AdmobBannerWidget({
    super.key,
    this.isInActiveRide = false,
    // ID de prueba oficial de Google AdMob para banner Android
    this.adUnitId = 'ca-app-pub-3940256099942544/6300978111',
  });

  @override
  State<AdmobBannerWidget> createState() => _AdmobBannerWidgetState();
}

class _AdmobBannerWidgetState extends State<AdmobBannerWidget> {
  BannerAd? _bannerAd;
  bool _isLoaded = false;

  @override
  void initState() {
    super.initState();
    if (!widget.isInActiveRide) {
      _loadBanner();
    }
  }

  @override
  void didUpdateWidget(covariant AdmobBannerWidget oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (widget.isInActiveRide && _bannerAd != null) {
      // Enclavamiento de seguridad vial: destruir anuncio si entra en carrera
      _bannerAd?.dispose();
      _bannerAd = null;
      setState(() => _isLoaded = false);
    } else if (!widget.isInActiveRide && _bannerAd == null) {
      _loadBanner();
    }
  }

  void _loadBanner() {
    try {
      _bannerAd = BannerAd(
        adUnitId: widget.adUnitId,
        size: AdSize.banner,
        request: const AdRequest(),
        listener: BannerAdListener(
          onAdLoaded: (ad) {
            if (mounted) setState(() => _isLoaded = true);
          },
          onAdFailedToLoad: (ad, error) {
            debugPrint('[AdMob] Error al cargar banner: $error');
            ad.dispose();
          },
        ),
      )..load();
    } catch (e) {
      debugPrint('[AdMob] Error inicializando banner: $e');
    }
  }

  @override
  void dispose() {
    _bannerAd?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (widget.isInActiveRide || !_isLoaded || _bannerAd == null) {
      return const SizedBox.shrink();
    }

    return Container(
      width: _bannerAd!.size.width.toDouble(),
      height: _bannerAd!.size.height.toDouble(),
      margin: const EdgeInsets.symmetric(vertical: 8),
      decoration: BoxDecoration(
        color: AppColors.surface,
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: Colors.grey.withOpacity(0.2)),
      ),
      alignment: Alignment.center,
      child: AdWidget(ad: _bannerAd!),
    );
  }
}
