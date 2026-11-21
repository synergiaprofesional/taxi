#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script: scripts/query_graphify.py
Descripción: Utilidad de consulta forense y análisis de impacto (blast radius)
             sobre los grafos de conocimiento generados por Graphify en Synergia Móvil.
Ubicación obligatoria: scripts/ (Regla Inviolable #1)
"""

import sys
import os
import json
import argparse
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent

GRAPHS = {
    "lib": WORKSPACE_ROOT / "lib" / "graphify-out" / "graph.json",
    "bitacoras": WORKSPACE_ROOT / "Bitacoras" / "graphify-out" / "graph.json",
}

def load_graph(graph_key: str) -> dict:
    path = GRAPHS.get(graph_key)
    if not path or not path.exists():
        print(f"Error: No se encontró el grafo '{graph_key}' en: {path}", file=sys.stderr)
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_stats(g: dict, name: str):
    nodes = g.get("nodes", [])
    edges = g.get("links", g.get("edges", []))
    communities = set(n.get("community") for n in nodes if n.get("community") is not None)
    print(f"\n=======================================================")
    print(f"  ESTADÍSTICAS DEL GRAFO: {name.upper()}")
    print(f"=======================================================")
    print(f" - Total Nodos:        {len(nodes)}")
    print(f" - Total Relaciones:   {len(edges)}")
    print(f" - Comunidades:        {len(communities)}")
    
    # Grados por nodo (God Nodes)
    degrees = {}
    for e in edges:
        s = e.get("source")
        t = e.get("target")
        degrees[s] = degrees.get(s, 0) + 1
        degrees[t] = degrees.get(t, 0) + 1
        
    top_nodes = sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:10]
    print("\n Top 10 Nodos más conectados (God Nodes):")
    for nid, count in top_nodes:
        # buscar label
        label = nid
        for n in nodes:
            if n.get("id") == nid:
                label = n.get("label", nid)
                break
        print(f"   * {label} ({nid}): {count} conexiones")
    print("=======================================================\n")

def find_nodes(g: dict, term: str):
    term = term.lower()
    nodes = g.get("nodes", [])
    matches = [n for n in nodes if term in str(n.get("label", "")).lower() or term in str(n.get("id", "")).lower()]
    print(f"\nBúsqueda de '{term}': {len(matches)} coincidencias encontradas:")
    for n in matches[:25]:
        src = n.get("source_file") or "N/A"
        print(f" - [{n.get('id')}] {n.get('label')} (Tipo: {n.get('file_type', 'N/A')}, Archivo: {src})")
    if len(matches) > 25:
        print(f" ... y {len(matches) - 25} coincidencias más.")

def blast_radius(g: dict, term: str):
    term = term.lower()
    nodes = g.get("nodes", [])
    edges = g.get("links", g.get("edges", []))
    
    matching_ids = {n.get("id"): n.get("label") for n in nodes if term in str(n.get("label", "")).lower() or term in str(n.get("id", "")).lower()}
    if not matching_ids:
        print(f"No se encontró ningún nodo coincidente con: '{term}'")
        return
        
    print(f"\n=======================================================")
    print(f"  ANÁLISIS DE IMPACTO (BLAST RADIUS) PARA: '{term}'")
    print(f"  Nodos identificados: {list(matching_ids.values())}")
    print(f"=======================================================")
    
    inbound = []
    outbound = []
    
    for e in edges:
        s = e.get("source")
        t = e.get("target")
        rel = e.get("relation", "relates_to")
        src_f = e.get("source_file") or "N/A"
        
        if s in matching_ids and t not in matching_ids:
            outbound.append((s, rel, t, src_f))
        elif t in matching_ids and s not in matching_ids:
            inbound.append((s, rel, t, src_f))
            
    print(f"\n1. VECINOS SALIENTES (A qué llama o qué afecta este componente) [{len(outbound)}]:")
    for s, rel, t, src_f in outbound[:20]:
        s_lbl = matching_ids.get(s, s)
        print(f"   --> [{s_lbl}] --({rel})--> [{t}] (en {src_f})")
        
    print(f"\n2. VECINOS ENTRANTES (Quién depende o llama a este componente) [{len(inbound)}]:")
    for s, rel, t, src_f in inbound[:20]:
        t_lbl = matching_ids.get(t, t)
        print(f"   <-- [{s}] --({rel})--> [{t_lbl}] (en {src_f})")
    print("=======================================================\n")

def main():
    parser = argparse.ArgumentParser(description="Herramienta de Consulta y Análisis de Grafos Graphify para Synergia Móvil")
    parser.add_argument("--graph", choices=["lib", "bitacoras"], default="lib", help="Grafo a consultar (default: lib)")
    parser.add_argument("--stats", action="store_true", help="Mostrar estadísticas y God Nodes")
    parser.add_argument("--find", type=str, help="Buscar nodos por nombre o id")
    parser.add_argument("--blast-radius", type=str, help="Calcular impacto de cambios en un componente")
    
    args = parser.parse_args()
    
    if not (args.stats or args.find or args.blast_radius):
        args.stats = True
        
    g = load_graph(args.graph)
    
    if args.stats:
        get_stats(g, args.graph)
    if args.find:
        find_nodes(g, args.find)
    if args.blast_radius:
        blast_radius(g, args.blast_radius)

if __name__ == "__main__":
    main()

