import 'package:flutter/material.dart';
import '../../core/theme/app_colors.dart';

class SearchGenericWidget<T> extends StatelessWidget {
  final String label;
  final String hintText;
  final String? valueText;
  final IconData prefixIcon;
  final Future<List<T>> Function(String query) onSearch;
  final String Function(T item) titleBuilder;
  final String Function(T item)? subtitleBuilder;
  final List<T>? primaryItems;
  final String primarySectionTitle;
  final String secondarySectionTitle;
  final Function(T selectedItem)? onSelected;

  const SearchGenericWidget({
    super.key,
    required this.label,
    required this.hintText,
    this.valueText,
    this.prefixIcon = Icons.search,
    required this.onSearch,
    required this.titleBuilder,
    this.subtitleBuilder,
    this.primaryItems,
    this.primarySectionTitle = 'Conductores principales',
    this.secondarySectionTitle = 'Otros conductores',
    this.onSelected,
  });

  void _abrirBuscador(BuildContext context) async {
    final T? selected = await Navigator.push<T>(
      context,
      MaterialPageRoute(
        builder: (ctx) => SearchPageWidget<T>(
          title: label,
          hintText: hintText,
          onSearch: onSearch,
          titleBuilder: titleBuilder,
          subtitleBuilder: subtitleBuilder,
          primaryItems: primaryItems,
          primarySectionTitle: primarySectionTitle,
          secondarySectionTitle: secondarySectionTitle,
        ),
      ),
    );

    if (selected != null && onSelected != null) {
      onSelected!(selected);
    }
  }

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: () => _abrirBuscador(context),
      borderRadius: BorderRadius.circular(10),
      child: InputDecorator(
        decoration: InputDecoration(
          labelText: label,
          hintText: hintText,
          prefixIcon: Icon(prefixIcon, color: AppColors.primary),
          suffixIcon: const Icon(Icons.arrow_drop_down, color: Colors.grey),
          filled: true,
          fillColor: AppColors.surface,
          border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
        ),
        child: Text(
          valueText?.isNotEmpty == true ? valueText! : hintText,
          style: TextStyle(
            color: valueText?.isNotEmpty == true ? Colors.white : Colors.grey.shade500,
            fontSize: 15,
          ),
        ),
      ),
    );
  }
}

class SearchPageWidget<T> extends StatefulWidget {
  final String title;
  final String hintText;
  final Future<List<T>> Function(String query) onSearch;
  final String Function(T item) titleBuilder;
  final String Function(T item)? subtitleBuilder;
  final List<T>? primaryItems;
  final String primarySectionTitle;
  final String secondarySectionTitle;

  const SearchPageWidget({
    super.key,
    required this.title,
    required this.hintText,
    required this.onSearch,
    required this.titleBuilder,
    this.subtitleBuilder,
    this.primaryItems,
    required this.primarySectionTitle,
    required this.secondarySectionTitle,
  });

  @override
  State<SearchPageWidget<T>> createState() => _SearchPageWidgetState<T>();
}

class _SearchPageWidgetState<T> extends State<SearchPageWidget<T>> {
  final TextEditingController _queryCtrl = TextEditingController();
  List<T> _results = [];
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    _ejecutarBusqueda('');
  }

  @override
  void dispose() {
    _queryCtrl.dispose();
    super.dispose();
  }

  Future<void> _ejecutarBusqueda(String q) async {
    setState(() => _isLoading = true);
    try {
      final items = await widget.onSearch(q);
      if (mounted) {
        setState(() {
          _results = items;
          _isLoading = false;
        });
      }
    } catch (e) {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final hasPrimary = widget.primaryItems != null && widget.primaryItems!.isNotEmpty;

    return Scaffold(
      appBar: AppBar(
        title: TextField(
          controller: _queryCtrl,
          autofocus: true,
          style: const TextStyle(color: Colors.white, fontSize: 16),
          decoration: InputDecoration(
            hintText: widget.hintText,
            hintStyle: const TextStyle(color: Colors.white54),
            border: InputBorder.none,
            suffixIcon: _queryCtrl.text.isNotEmpty
                ? IconButton(
                    icon: const Icon(Icons.clear, color: Colors.white70),
                    onPressed: () {
                      _queryCtrl.clear();
                      _ejecutarBusqueda('');
                    },
                  )
                : null,
          ),
          onChanged: _ejecutarBusqueda,
        ),
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator(color: AppColors.primary))
          : ListView(
              padding: const EdgeInsets.symmetric(vertical: 8),
              children: [
                if (hasPrimary && _queryCtrl.text.isEmpty) ...[
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                    child: Text(
                      widget.primarySectionTitle.toUpperCase(),
                      style: const TextStyle(
                        fontSize: 12,
                        fontWeight: FontWeight.bold,
                        letterSpacing: 0.8,
                        color: AppColors.primary,
                      ),
                    ),
                  ),
                  ...widget.primaryItems!.map((item) => _buildItemTile(item, isPrimary: true)),
                  const Divider(height: 24),
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                    child: Text(
                      widget.secondarySectionTitle.toUpperCase(),
                      style: const TextStyle(
                        fontSize: 12,
                        fontWeight: FontWeight.bold,
                        letterSpacing: 0.8,
                        color: Colors.grey,
                      ),
                    ),
                  ),
                ],
                ..._results.map((item) => _buildItemTile(item)),
                if (_results.isEmpty && (!hasPrimary || _queryCtrl.text.isNotEmpty))
                  const Padding(
                    padding: EdgeInsets.all(32),
                    child: Center(
                      child: Text('No se encontraron resultados', style: TextStyle(color: Colors.grey)),
                    ),
                  ),
              ],
            ),
    );
  }

  Widget _buildItemTile(T item, {bool isPrimary = false}) {
    final title = widget.titleBuilder(item);
    final subtitle = widget.subtitleBuilder != null ? widget.subtitleBuilder!(item) : null;

    return ListTile(
      leading: CircleAvatar(
        radius: 18,
        backgroundColor: isPrimary ? AppColors.primary.withValues(alpha: 0.2) : Colors.white10,
        child: Icon(
          isPrimary ? Icons.star : Icons.chevron_right,
          color: isPrimary ? AppColors.primary : Colors.grey,
          size: 18,
        ),
      ),
      title: Text(title, style: TextStyle(fontWeight: isPrimary ? FontWeight.bold : FontWeight.normal)),
      subtitle: subtitle != null ? Text(subtitle, style: const TextStyle(fontSize: 12, color: Colors.grey)) : null,
      onTap: () => Navigator.pop(context, item),
    );
  }
}
