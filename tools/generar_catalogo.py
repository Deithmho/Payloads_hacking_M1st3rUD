#!/usr/bin/env python3
"""Genera las guías a partir de datos editoriales revisables."""

from pathlib import Path
from urllib.parse import quote, urlsplit
from importlib import import_module
from importlib.util import find_spec
import json
from catalogo import CATEGORIAS, TEMAS, FUENTES

RAIZ = Path(__file__).resolve().parents[1]


def integrar_payloads():
    modulos = (
        'payloads_auth', 'payloads_injections', 'payloads_client',
        'payloads_server', 'payloads_api', 'payloads_infra',
    )
    ampliaciones = {}
    for nombre in modulos:
        if find_spec(nombre) is None:
            continue
        datos = import_module(nombre).AMPLIACIONES
        repetidos = set(ampliaciones) & set(datos)
        if repetidos:
            raise SystemExit(f'Payloads repetidos en {nombre}: {repetidos}')
        ampliaciones.update(datos)
    for tema in TEMAS:
        if tema['slug'] in ampliaciones:
            pruebas = ampliaciones[tema['slug']]
            if len(pruebas) < 6 or any(len(p) != 6 or not p[5].startswith('https://') for p in pruebas):
                raise SystemExit(f'Pruebas insuficientes o sin fuente: {tema["slug"]}')
            if len({p[0] for p in pruebas}) != len(pruebas) or len({p[3] for p in pruebas}) != len(pruebas):
                raise SystemExit(f'Pruebas duplicadas: {tema["slug"]}')
            for prueba in pruebas:
                if prueba[2] == 'json':
                    try:
                        json.loads(prueba[3])
                    except json.JSONDecodeError as error:
                        raise SystemExit(f'JSON inválido en {tema["slug"]}: {prueba[0]} ({error})')
            tema['pruebas'] = [dict(zip(
                ('nombre', 'objetivo', 'lenguaje', 'codigo', 'interpretacion', 'fuente_url'), p
            )) for p in pruebas]
    return set(ampliaciones)


def integrar_bancos():
    modulos = (
        'bancos_auth', 'bancos_injections', 'bancos_client',
        'bancos_server', 'bancos_api', 'bancos_infra',
    )
    bancos = {}
    for nombre in modulos:
        if find_spec(nombre) is None:
            continue
        datos = import_module(nombre).BANCOS
        repetidos = set(bancos) & set(datos)
        if repetidos:
            raise SystemExit(f'Bancos repetidos en {nombre}: {repetidos}')
        bancos.update(datos)
    for tema in TEMAS:
        if tema['slug'] not in bancos:
            continue
        grupos = bancos[tema['slug']]
        if len(grupos) < 4 or {g[0] for g in grupos} != {'basicos', 'contextos', 'avanzados'}:
            raise SystemExit(f'Banco insuficiente: {tema["slug"]}')
        if any(len(g) != 6 or not g[5].startswith('https://') or not g[3].strip() for g in grupos):
            raise SystemExit(f'Banco mal formado: {tema["slug"]}')
        if len({g[1] for g in grupos}) != len(grupos) or len({g[3] for g in grupos}) != len(grupos):
            raise SystemExit(f'Grupos repetidos en banco: {tema["slug"]}')
        tema['bancos'] = [dict(zip(
            ('nivel', 'titulo', 'lenguaje', 'codigo', 'nota', 'fuente_url'), g
        )) for g in grupos]
    return set(bancos)


def enlace(tema):
    return tema['carpeta']


def enlace_md(tema):
    return quote(enlace(tema), safe='')


def lista(items):
    return "\n".join(f"- {item}" for item in items)


def etiqueta_fuente(url):
    host = urlsplit(url).hostname or ''
    if 'swisskyrepo/PayloadsAllTheThings' in url:
        return 'PayloadsAllTheThings'
    for dominio, etiqueta in (
        ('portswigger.net', 'PortSwigger'),
        ('wstg.owasp.org', 'OWASP WSTG'),
        ('api-security.owasp.org', 'OWASP API Security'),
        ('cheatsheetseries.owasp.org', 'OWASP Cheat Sheet'),
        ('genai.owasp.org', 'OWASP GenAI'),
        ('docs.aws.amazon.com', 'AWS'),
        ('docs.cloud.google.com', 'Google Cloud'),
        ('learn.microsoft.com', 'Microsoft Learn'),
        ('datatracker.ietf.org', 'RFC'),
        ('community.owasp.org', 'OWASP'),
        ('developer.android.com', 'Android Developers'),
    ):
        if host == dominio:
            return etiqueta
    return host


def escribir_descripcion(tema):
    titulo = tema['titulo']
    variantes = "\n".join(f"| **{nombre}** | {detalle} |" for nombre, detalle in tema['variantes'])
    refs = [FUENTES[x] for x in tema['fuentes']]
    ref_md = "\n".join(f"- [{nombre}]({url}) — {motivo}." for nombre, url, motivo in refs)
    caso = tema.get('caso') or "No se atribuye un incidente concreto sin una divulgación pública verificable. Las fuentes enlazadas documentan el mecanismo; un laboratorio, cuando lo hay, no prueba impacto en un sistema real."
    return f"""# 📖 {titulo}: descripción general

> **Alcance:** pruebas con autorización, cuentas y objetos propios. Los ejemplos de `Payloads_hack/` usan marcadores y buscan una señal mínima, sin extracción masiva ni cambios irreversibles.

## 🧩 Qué es y por qué ocurre

{tema['mecanismo']}

El límite de confianza relevante es **{tema['limite']}**. La aplicación recibe **{tema['entrada']}** y debería **{tema['control']}**. La vulnerabilidad aparece cuando **{tema['fallo']}**. Una respuesta inesperada aislada no basta: hay que demostrar que el dato controlado cambia una decisión o un efecto protegido.

## ⚙️ Flujo técnico

1. **Punto de entrada:** {tema['paso1']}
2. **Procesamiento:** {tema['paso2']}
3. **Ruptura del control:** {tema['paso3']}
4. **Observación:** {tema['paso4']}

## 🧭 Contextos y variantes

**Dónde buscar:** {tema['contextos']}.

| Variante | Diferencia técnica |
| --- | --- |
{variantes}

## 🔗 Cadenas y dependencias

{tema['cadena']}

> **Condición:** una cadena solo es válida si cada eslabón se reproduce con la misma identidad, origen, caché y configuración relevantes. No se infiere explotación por la mera presencia de un encabezado, parámetro o versión.

## ⚠️ Impacto y severidad

{tema['impacto']} La severidad depende del activo alcanzado, privilegios necesarios, interacción, amplitud y consecuencias demostradas. **No se asigna un CVSS numérico sin un escenario reproducido**; para un informe, calcular CVSS v4.0 con esos datos y añadir el contexto de negocio.

## 🔍 Checklist de detección

{lista(tema['checklist'])}
- Registrar request y response mínimos, identidad usada, resultado esperado y observado.
- Repetir con un control negativo y confirmar que el comportamiento no es una respuesta genérica del proxy, WAF o caché.
- Detenerse en la primera prueba suficiente; redactar secretos y datos ajenos.

## 🛡️ Corrección y verificación

{tema['correccion']} La prueba de regresión debe comprobar tanto el caso permitido como el caso denegado en el componente que toma la decisión.

## 🧪 Caso o evidencia pública

{caso}

## 📚 Fuentes

{ref_md}

---

[← Índice general](../../README.md) · [🗡️ Payloads y técnicas](../Payloads_hack/README.md)
"""


def escribir_payloads(tema):
    fence = chr(96) * 3
    bancos = [
        '> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.'
    ]
    for nivel, encabezado in (
        ('basicos', '## 💉 Payloads básicos'),
        ('contextos', '## 🧭 Payloads por contexto'),
        ('avanzados', '## 🔥 Payloads avanzados'),
    ):
        bancos.append(encabezado)
        for grupo in tema['bancos']:
            if grupo['nivel'] != nivel:
                continue
            bancos.append(f"""### {grupo['titulo']}

{fence}{grupo['lenguaje']}
{grupo['codigo']}
{fence}

**Cuándo usarlo:** {grupo['nota']}

**Fuente:** [{etiqueta_fuente(grupo['fuente_url'])}]({grupo['fuente_url']}).
""")
    bancos_md = "\n\n".join(bancos)
    bloques = []
    for numero, p in enumerate(tema['pruebas'], 1):
        bloques.append(f"""### {numero}. {p['nombre']}

**Objetivo:** {p['objetivo']}

```{p['lenguaje']}
{p['codigo'].strip()}
```

**Interpretación:** {p['interpretacion']}

**Fuente técnica:** [{etiqueta_fuente(p['fuente_url'])}]({p['fuente_url']}).
""")
    return f"""# 🗡️ {tema['titulo']}: payloads y técnicas

> **Uso autorizado:** sustituir `{{ORIGEN}}`, `{{TOKEN_A}}`, `{{ID_PROPIO}}` y `{{ID_CONTROLADO_B}}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 📚 Banco ampliado de payloads

[Abrir el catálogo por técnica y los diccionarios de PayloadsAllTheThings](Catalogo_PATT.md). Los bloques de esta guía explican las pruebas iniciales; el catálogo reúne variantes adicionales por motor, parser y contexto.

{bancos_md}

## 🔬 Pruebas guiadas por escenario

{chr(10).join(bloques)}
## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
"""


def main():
    cubiertos = integrar_payloads()
    bancos_cubiertos = integrar_bancos()
    esperados = {t['slug'] for t in TEMAS}
    if cubiertos != esperados:
        raise SystemExit(f'Faltan ampliaciones: {sorted(esperados - cubiertos)}; extra: {sorted(cubiertos - esperados)}')
    if bancos_cubiertos != esperados:
        raise SystemExit(f'Faltan bancos: {sorted(esperados - bancos_cubiertos)}; extra: {sorted(bancos_cubiertos - esperados)}')
    if len({(t['categoria'], t['slug']) for t in TEMAS}) != len(TEMAS):
        raise SystemExit('Slug duplicado')
    for tema in TEMAS:
        if len(tema['pruebas']) < 2:
            raise SystemExit(f"Faltan técnicas: {tema['slug']}")
        carpeta = RAIZ / enlace(tema)
        for subcarpeta, contenido in [
            ('Descripcion', escribir_descripcion(tema)),
            ('Payloads_hack', escribir_payloads(tema)),
        ]:
            destino = carpeta / subcarpeta / 'README.md'
            destino.parent.mkdir(parents=True, exist_ok=True)
            destino.write_text(contenido, encoding='utf-8')
    secciones = []
    for categoria, rotulo in CATEGORIAS:
        filas = [t for t in TEMAS if t['categoria'] == categoria]
        indice = "\n".join(f"{i}. [{t['carpeta']}]({enlace_md(t)}/Descripcion/README.md) · [payloads]({enlace_md(t)}/Payloads_hack/README.md)" for i, t in enumerate(filas, 1))
        secciones.append(f"## {rotulo}\n\n{indice}")
    secciones_md = "\n\n".join(secciones)
    escenarios = sum(len(t['pruebas']) for t in TEMAS)
    bloques_banco = sum(len(t['bancos']) for t in TEMAS)
    estadisticas_patt = json.loads((RAIZ / 'tools/patt_stats.json').read_text(encoding='utf-8'))
    cobertura_filas = []
    for categoria, rotulo in CATEGORIAS:
        filas = [t for t in TEMAS if t['categoria'] == categoria]
        cobertura_filas.append(
            f"| {rotulo} | {len(filas)} | {sum(len(t['bancos']) for t in filas)} | {sum(len(t['pruebas']) for t in filas)} |"
        )
    cobertura = "\n".join(cobertura_filas)
    principal = f"""# 🛡️ Payloads Hacking M1st3rUD

**Manual de campo en español para pentesting web, APIs y bug bounty autorizado.** Cada tema separa el mecanismo, contexto, variantes, evidencia y corrección de los ejemplos técnicos listos para adaptar. El catálogo contiene **{len(TEMAS)} temas, {bloques_banco} bloques de payloads y {escenarios} escenarios de prueba**, incluyendo las categorías solapadas solicitadas: una misma raíz técnica puede tener guías de aplicación distintas.

El banco ampliado incorpora **{estadisticas_patt['documentos']} anexos técnicos, {estadisticas_patt['bloques']} bloques de código, {estadisticas_patt['inline']} variantes en línea y {estadisticas_patt['listas']} diccionarios con {estadisticas_patt['lineas_listas']} líneas** de una revisión fija de PayloadsAllTheThings. Estas cifras cuentan apariciones por tema; algunas fuentes se reutilizan donde sirven a más de una vulnerabilidad.

> **Uso ético:** emplear solo en laboratorios, activos propios o programas con autorización y alcance vigentes. Respetar límites de frecuencia, datos, concurrencia y divulgación. Los ejemplos son pruebas mínimas; un resultado llamativo no equivale a una vulnerabilidad validada.

## 📊 Cobertura

| Área | Temas | Bancos | Escenarios |
| --- | ---: | ---: | ---: |
{cobertura}

## 🧭 Cómo usar este repositorio

1. Abrir `Descripcion/README.md` para entender el límite de confianza y la señal de confirmación.
2. En `Payloads_hack/README.md`, empezar por **Payloads básicos**, elegir una variante por contexto y consultar las pruebas guiadas para interpretar el resultado.
3. Abrir `Payloads_hack/Catalogo_PATT.md` para las variantes por motor, codificación y tecnología, y para descargar los diccionarios cuando existan.
4. Comparar con un control negativo y registrar la evidencia mínima; detenerse antes de afectar datos ajenos.
5. Calcular severidad a partir del impacto comprobado, no del nombre de la técnica.

Cada vulnerabilidad tiene su carpeta en la raíz, con el nombre de la lista solicitada y **exactamente dos subcarpetas**: `Descripcion/` y `Payloads_hack/`. En nombres que contenían `/`, se usa ` - ` porque la barra separa directorios en Git.

{secciones_md}

## 📚 Referencias y criterio editorial

- [OWASP WSTG](https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/), [OWASP Top 10:2025](https://top10.owasp.org/2025/0x00_2025-Introduction/) y [OWASP API Security Top 10:2023](https://api-security.owasp.org/editions/2023/en/0x11-t10/) aportan taxonomía y metodología.
- [PortSwigger Web Security Academy](https://portswigger.net/web-security/all-topics) aporta mecanismos y laboratorios reproducibles.
- [HackTricks](https://book.hacktricks.wiki/) aporta referencias técnicas. Los anexos identificados como PATT reproducen o adaptan código y listas de [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings) bajo su [licencia MIT](LICENCIA_PATT.md), con enlace a cada documento de origen.
- [YesWeHack, análisis de confusión sintáctica](https://www.yeswehack.com/learn-bug-bounty/syntax-confusion-ambiguous-parsing-exploits) y [PortSwigger Research](https://portswigger.net/research/) se usan como ejemplos de investigación pública. [Fuentes y criterios](FUENTES.md) explica la diferencia entre una investigación pública, un laboratorio y un relato secundario.

## 🔄 Origen y reproducción del banco ampliado

Los anexos proceden de la revisión `3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a` de PayloadsAllTheThings. La [correspondencia de temas](tools/patt_mapa.py) y el [importador](tools/importar_patt.py) permiten regenerarlos desde una copia local de esa revisión con `python3 tools/importar_patt.py --upstream /ruta/a/PayloadsAllTheThings`. Después, ejecutar `python3 tools/generar_catalogo.py` y `python3 tools/validar_catalogo.py`. El banco reúne documentos y listas de texto pertinentes al pentesting web/API; no es una réplica de imágenes, binarios ni archivos de claves del proyecto original.

## 🧾 Contribuciones y calidad

Las mejoras deben mantener la estructura, explicar precondiciones, incluir una prueba de control, enlazar fuentes y evitar datos de terceros. [Guía de contribución](CONTRIBUIR.md).

---

**Créditos:** OWASP, PortSwigger, HackTricks, PayloadsAllTheThings y autores de investigaciones públicas citadas. Los anexos PATT contienen material de terceros identificado y licenciado; las guías explicativas y la organización en español son aportaciones de este repositorio.
"""
    (RAIZ / 'README.md').write_text(principal, encoding='utf-8')
    print(f"Generadas {len(TEMAS)} guías en {len(CATEGORIAS)} categorías")


if __name__ == '__main__':
    main()
