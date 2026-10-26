#!/usr/bin/env python3
"""Verifica la estructura y enlaces locales del catálogo generado."""

import re
from pathlib import Path
from urllib.parse import unquote
from catalogo import CATEGORIAS, TEMAS

raiz = Path(__file__).resolve().parents[1]
errores = []
slugs = set()

for tema in TEMAS:
    key = (tema['categoria'], tema['slug'])
    if key in slugs:
        errores.append(f'Slug duplicado: {key}')
    slugs.add(key)
    carpeta = raiz / tema['carpeta']
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
            for encabezado in ('## 💉 Payloads básicos', '## 🧭 Payloads por contexto', '## 🔥 Payloads avanzados'):
                if encabezado not in texto:
                    errores.append(f'Falta {encabezado} en {doc}')
            if texto.count('**Fuente:**') < 4:
                errores.append(f'Faltan bloques de banco: {doc}')
            escenarios = len(re.findall(r'^### \d+\.', texto, re.M))
            if escenarios < 6:
                errores.append(f'Faltan escenarios: {doc}')
            if texto.count('**Fuente técnica:**') != escenarios:
                errores.append(f'Faltan fuentes por técnica: {doc}')

for doc in raiz.rglob('*.md'):
    for destino in re.findall(r'\[[^]]+\]\(([^)]+)\)', doc.read_text(encoding='utf-8')):
        if not destino.startswith(('https://', 'http://', '#')):
            path = (doc.parent / unquote(destino.split('#', 1)[0])).resolve()
            if not path.exists():
                errores.append(f'Enlace roto: {doc} -> {destino}')

if len({t['carpeta'] for t in TEMAS}) != len(TEMAS):
    errores.append('Nombres de carpetas duplicados')
publicados = {p.name for p in raiz.iterdir() if p.is_dir() and p.name not in {'.git', 'tools'}}
esperados = {t['carpeta'] for t in TEMAS}
if publicados != esperados:
    errores.append(f'Carpetas publicadas no coinciden: faltan={esperados-publicados}, sobran={publicados-esperados}')

if errores:
    raise SystemExit('\n'.join(errores))
print(f'OK: {len(TEMAS)} temas, {len(CATEGORIAS)} categorías, dos guías por tema y enlaces locales válidos')
