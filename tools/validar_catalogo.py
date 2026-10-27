#!/usr/bin/env python3
"""Verifica la estructura y enlaces locales del catálogo generado."""

import json
import re
from pathlib import Path
from urllib.parse import unquote
from catalogo import CATEGORIAS, TEMAS

raiz = Path(__file__).resolve().parents[1]
errores = []
slugs = set()


def fuera_de_codigo(texto):
    """Devuelve Markdown visible para no confundir payloads con enlaces."""
    salida = []
    delimitador = None
    marca = chr(96)
    for linea in texto.splitlines():
        cerca = re.match(r'^\s{0,4}(' + re.escape(marca) + r'{3,}|~{3,})(.*)$', linea)
        if delimitador is not None:
            if cerca and cerca.group(1)[0] == delimitador[0] and len(cerca.group(1)) >= len(delimitador):
                delimitador = None
            continue
        if cerca:
            delimitador = cerca.group(1)
            continue
        salida.append(re.sub(re.escape(marca) + r'[^' + re.escape(marca) + r']*' +
                             re.escape(marca), '', linea))
    return '\n'.join(salida), delimitador is None

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
        if not texto.startswith('# ') or not fuera_de_codigo(texto)[1]:
            errores.append(f'Markdown incompleto: {doc}')
        if sub == 'Descripcion':
            for encabezado in ('## 🧩', '## ⚙️', '## 🧭', '## 🔗', '## ⚠️', '## 🔍', '## 🛡️', '## 📚'):
                if encabezado not in texto:
                    errores.append(f'Falta {encabezado} en {doc}')
        else:
            for encabezado in ('## 💉 Payloads básicos', '## 🧭 Payloads por contexto', '## 🔥 Payloads avanzados'):
                if encabezado not in texto:
                    errores.append(f'Falta {encabezado} en {doc}')
            if '[Abrir el catálogo por técnica' not in texto:
                errores.append(f'Falta navegación al banco ampliado: {doc}')
            if not (carpeta / sub / 'Catalogo_PATT.md').is_file():
                errores.append(f'Falta catálogo ampliado: {carpeta}')
            if texto.count('**Fuente:**') < 4:
                errores.append(f'Faltan bloques de banco: {doc}')
            escenarios = len(re.findall(r'^### \d+\.', texto, re.M))
            if escenarios < 6:
                errores.append(f'Faltan escenarios: {doc}')
            if texto.count('**Fuente técnica:**') != escenarios:
                errores.append(f'Faltan fuentes por técnica: {doc}')

for doc in raiz.rglob('*.md'):
    visible, cerrado = fuera_de_codigo(doc.read_text(encoding='utf-8'))
    if not cerrado:
        errores.append(f'Cerca Markdown sin cerrar: {doc}')
    for destino in re.findall(r'\[[^]]+\]\(([^)]+)\)', visible):
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

estadisticas = json.loads((raiz / 'tools/patt_stats.json').read_text(encoding='utf-8'))
anexos = list(raiz.glob('*/Payloads_hack/PATT_*.md'))
listas_patt = list(raiz.glob('*/Payloads_hack/PATT_LISTA_*'))
if len(anexos) != estadisticas['documentos']:
    errores.append(f'Número de anexos PATT distinto: {len(anexos)}')
if len(listas_patt) != estadisticas['listas']:
    errores.append(f'Número de diccionarios PATT distinto: {len(listas_patt)}')
if not (raiz / 'LICENCIA_PATT.md').is_file():
    errores.append('Falta licencia MIT de PATT')
for anexo in anexos:
    contenido = anexo.read_text(encoding='utf-8')
    if 'LICENCIA_PATT.md' not in contenido or 'github.com/swisskyrepo/PayloadsAllTheThings/blob/' not in contenido:
        errores.append(f'Anexo sin atribución: {anexo}')

if errores:
    raise SystemExit('\n'.join(errores))
print(f'OK: {len(TEMAS)} temas, {len(CATEGORIAS)} categorías, dos guías por tema y enlaces locales válidos')
