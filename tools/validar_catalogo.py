#!/usr/bin/env python3
"""Verifica la estructura y enlaces locales del catálogo generado."""

import re
from pathlib import Path
from catalogo import CATEGORIAS, TEMAS

raiz = Path(__file__).resolve().parents[1]
errores = []
slugs = set()

for tema in TEMAS:
    key = (tema['categoria'], tema['slug'])
    if key in slugs:
        errores.append(f'Slug duplicado: {key}')
    slugs.add(key)
    carpeta = raiz / tema['categoria'] / tema['slug']
    subcarpetas = sorted(p.name for p in carpeta.iterdir() if p.is_dir())
    if subcarpetas != ['Descripcion', 'Payloads_hack']:
        errores.append(f'Subcarpetas inesperadas: {carpeta}')
    for sub in ('Descripcion', 'Payloads_hack'):
        doc = carpeta / sub / 'README.md'
        if not doc.is_file():
            errores.append(f'Falta {doc}')
            continue
        texto = doc.read_text(encoding='utf-8')
        if not texto.startswith('# ') or texto.count('```') % 2:
            errores.append(f'Markdown incompleto: {doc}')
        if sub == 'Descripcion':
            for encabezado in ('## 🧩', '## ⚙️', '## 🧭', '## 🔗', '## ⚠️', '## 🔍', '## 🛡️', '## 📚'):
                if encabezado not in texto:
                    errores.append(f'Falta {encabezado} en {doc}')
        else:
            if len(re.findall(r'^### \d+\.', texto, re.M)) < 2:
                errores.append(f'Faltan escenarios: {doc}')

for doc in raiz.rglob('*.md'):
    for destino in re.findall(r'\[[^]]+\]\(([^)]+)\)', doc.read_text(encoding='utf-8')):
        if not destino.startswith(('https://', 'http://', '#')):
            path = (doc.parent / destino.split('#', 1)[0]).resolve()
            if not path.exists():
                errores.append(f'Enlace roto: {doc} -> {destino}')

for categoria, _ in CATEGORIAS:
    publicados = {p.name for p in (raiz / categoria).iterdir() if p.is_dir()}
    esperados = {t['slug'] for t in TEMAS if t['categoria'] == categoria}
    if publicados != esperados:
        errores.append(f'Índice de carpetas no coincide: {categoria}')

if errores:
    raise SystemExit('\n'.join(errores))
print(f'OK: {len(TEMAS)} temas, {len(CATEGORIAS)} categorías, dos guías por tema y enlaces locales válidos')
