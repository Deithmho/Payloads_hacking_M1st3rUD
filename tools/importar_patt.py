#!/usr/bin/env python3
"""Extrae ejemplos técnicos de PATT y los ordena bajo títulos en español.

Uso: python3 tools/importar_patt.py --upstream /ruta/PayloadsAllTheThings
Los archivos generados se versionan; el lector no necesita descargar PATT.
"""

from __future__ import annotations

import argparse
from collections import OrderedDict
import json
from pathlib import Path
import re
import shutil
import subprocess
import unicodedata
from urllib.parse import quote

from catalogo import TEMAS
from patt_mapa import MAPA

RAIZ = Path(__file__).resolve().parents[1]
REVISION = "3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a"
MARCA = chr(96)
FENCE = MARCA * 3
ENCABEZADO = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
CERCA = re.compile(r"^\s{0,4}(" + re.escape(MARCA) + r"{3,}|~{3,})(.*)$")
EN_LINEA = re.compile(re.escape(MARCA) + r"([^" + re.escape(MARCA) + r"\n]+)" + re.escape(MARCA))
OMITIR = {"summary", "references", "table of contents", "disclaimer"}

# Traducciones editoriales para que cada bloque señale el contexto de uso.
# Los nombres de motores, funciones, productos y sintaxis se conservan.
FRASES = [
    ("Password Reset Feature", "Flujo de recuperación de contraseña"),
    ("Account Takeover Through Password Reset Poisoning",
     "Toma de cuenta por envenenamiento del enlace de recuperación"),
    ("Password Reset via Email Parameter", "Recuperación mediante parámetro de correo"),
    ("IDOR on API Parameters", "IDOR en parámetros de API"),
    ("Leaking Password Reset Token", "Filtración del token de recuperación"),
    ("Account Takeover Due To Unicode Normalization Issue",
     "Toma de cuenta por normalización Unicode incorrecta"),
    ("Account Takeover via Web Vulnerabilities",
     "Toma de cuenta mediante vulnerabilidades web"),
    ("Account Takeover via HTTP Request Smuggling",
     "Toma de cuenta mediante desincronización HTTP"),
    ("Session Fixation", "Fijación de sesión"),
    ("Numeric Value Parameter", "Parámetro numérico"),
    ("Common Identifiers Parameter", "Identificadores comunes en parámetros"),
    ("Weak Pseudo Random Number Generator", "Generador seudoaleatorio débil"),
    ("Hashed Parameter", "Parámetro con hash"),
    ("Wildcard Parameter", "Comodines en parámetros"),
    ("IDOR Tips", "Consejos para IDOR"),
    ("Insecure Direct Object References", "Referencias directas inseguras a objetos"),
    ("Web Cache Deception", "Engaño de caché web"),
    ("Caching Sensitive Data", "Caché de datos sensibles"),
    ("Caching Custom JavaScript", "Caché de JavaScript personalizado"),
    ("Detecting Web Cache Deception", "Detección de engaño de caché web"),
    ("CloudFlare Caching", "Caché de Cloudflare"),
    ("UI Redressing", "Manipulación de interfaz"),
    ("Invisible Frames", "Marcos invisibles"),
    ("Button/Form Hijacking", "Secuestro de botones y formularios"),
    ("Execution Methods", "Métodos de ejecución"),
    ("Preventive Measures", "Medidas preventivas"),
    ("Implement X-Frame-Options Header", "Configurar cabecera X-Frame-Options"),
    ("Content Security Policy", "Política de seguridad de contenido"),
    ("Disabling JavaScript", "Desactivar JavaScript"),
    ("OnBeforeUnload Event", "Evento onbeforeunload"),
    ("Origin Reflection", "Reflexión del origen"),
    ("Vulnerable Implementation", "Implementación vulnerable"),
    ("Null Origin", "Origen null"),
    ("XSS on Trusted Origin", "XSS en origen confiable"),
    ("Wildcard Origin Without Credentials", "Origen comodín sin credenciales"),
    ("Expanding the Origin", "Ampliación del origen"),
    ("Inclusion Using Wrappers", "Inclusión mediante wrappers"),
    ("PHAR archive structure", "Estructura de archivo PHAR"),
    ("PHAR deserialization", "Deserialización PHAR"),
    ("Leak File content from error-based oracle",
     "Filtración de archivos mediante oráculo de errores"),
    ("Leak File content inside a Custom format output",
     "Filtración de archivos en salida de formato personalizado"),
    ("Leak File content Using Blind File read primitive",
     "Filtración de archivos mediante lectura ciega"),
    ("Null Byte", "Byte nulo"),
    ("Path Truncation", "Truncamiento de ruta"),
    ("Bypass allow_url_include", "Evasión de allow_url_include"),
    ("Command Injection", "Inyección de comandos"),
    ("Basic Commands", "Comandos básicos"),
    ("Chaining Commands", "Encadenamiento de comandos"),
    ("Argument Injection", "Inyección de argumentos"),
    ("Inside A Command", "Dentro de un comando"),
    ("Filter Bypasses", "Evasiones de filtros"),
    ("Without Space", "Sin espacios"),
    ("With A Line Return", "Con salto de línea"),
    ("With Backslash Newline", "Con barra inversa y salto de línea"),
    ("With Tilde Expansion", "Con expansión de virgulilla"),
    ("With Brace Expansion", "Con expansión de llaves"),
    ("Characters Filter Via Hex Encoding", "Filtro de caracteres mediante hex"),
    ("Characters Filter", "Filtro de caracteres"),
    ("With Single Quote", "Con comilla simple"),
    ("With Double Quote", "Con comilla doble"),
    ("Cross Site Scripting", "XSS"),
    ("Server Side Request Forgery", "SSRF"),
    ("Insecure Deserialization", "Deserialización insegura"),
    ("Cross-Site Request Forgery", "CSRF"),
    ("Mass Assignment", "Asignación masiva"),
    ("Open Redirect", "Redirección abierta"),
    ("Prototype Pollution", "Contaminación de prototipos"),
    ("DNS Rebinding", "Revinculación DNS"),
    ("Requirements", "Requisitos"),
    ("Challenge", "Ejercicio"),
    ("Tricks", "Trucos"),
]
GLOSARIO = [
    ("MySQL Injection", "Inyección MySQL"),
    ("PostgreSQL Injection", "Inyección PostgreSQL"),
    ("MSSQL Injection", "Inyección MSSQL"),
    ("SQL Injection", "Inyección SQL"),
    ("Iterative NULL Method", "Método iterativo con NULL"),
    ("ORDER BY Method", "Método ORDER BY"),
    ("LIMIT INTO Method", "Método LIMIT INTO"),
    ("URL Encoding", "Codificación URL"),
    ("Double URL Encoding", "Doble codificación URL"),
    ("Unicode Encoding", "Codificación Unicode"),
    ("Overlong UTF-8 Unicode Encoding", "Codificación UTF-8 sobrelarga"),
    ("Mangled Path", "Rutas alteradas"),
    ("Reverse Proxy URL Implementation", "Diferencias de URL en proxy inverso"),
    ("UNC Share", "Recurso compartido UNC"),
    ("ASP NET Cookieless", "ASP.NET sin cookies"),
    ("IIS Short Name", "Nombres cortos de IIS"),
    ("Java URL Protocol", "Protocolo URL de Java"),
    ("Extract Columns Name", "Extraer nombres de columnas"),
    ("Extract Data", "Extraer datos"),
    ("Extract Database", "Extraer base de datos"),
    ("Detect Columns Number", "Detección del número de columnas"),
    ("Remote File Inclusion", "Inclusión remota de archivos"),
    ("Local File Inclusion", "Inclusión local de archivos"),
    ("Blind XSS", "XSS ciego"),
    ("DOM Based XSS", "XSS basado en DOM"),
    ("Server Side Template Injection", "Inyección en plantillas del servidor"),
    ("Cross Site Scripting", "Secuencias de comandos entre sitios"),
    ("Cross Site Request Forgery", "Falsificación de solicitudes entre sitios"),
    ("Proof of Concept", "Prueba de concepto"),
    ("Default Databases", "Bases de datos predeterminadas"),
    ("Testing Injection", "Pruebas iniciales de inyección"),
    ("Union Based", "Basada en UNION"),
    ("Error Based", "Basada en errores"),
    ("Time Based", "Basada en tiempo"),
    ("Out of Band", "Fuera de banda"),
    ("WAF Bypass", "Evasión de WAF"),
    ("Filter Bypass", "Evasión de filtros"),
    ("CSP Bypass", "Evasión de CSP"),
    ("Detect Columns Number", "Detección del número de columnas"),
    ("Read Content of a File", "Lectura de un archivo"),
    ("Command Execution", "Ejecución de comandos"),
    ("Code Execution", "Ejecución de código"),
    ("Remote Code Execution", "Ejecución remota de código"),
    ("File Upload", "Subida de archivos"),
    ("File Inclusion", "Inclusión de archivos"),
    ("Directory Traversal", "Recorrido de directorios"),
    ("Path Traversal", "Recorrido de rutas"),
    ("Server Side", "Lado servidor"),
    ("Client Side", "Lado cliente"),
    ("Cross Site", "Entre sitios"),
    ("Account Takeover", "Toma de cuenta"),
    ("Password Reset", "Restablecimiento de contraseña"),
    ("Rate Limit", "Límite de solicitudes"),
    ("Open Redirect", "Redirección abierta"),
    ("Blind", "Ciega"),
    ("Payloads", "Payloads"),
    ("Common", "Comunes"),
    ("Basic", "Básicos"),
    ("Advanced", "Avanzados"),
    ("Methodology", "Metodología"),
    ("Examples", "Ejemplos"),
    ("Example", "Ejemplo"),
    ("Exploit", "Explotación"),
    ("Testing", "Pruebas"),
    ("Tools", "Herramientas"),
    ("Bypass", "Evasión"),
    ("Encoding", "Codificación"),
    ("Decoding", "Decodificación"),
    ("Unicode", "Unicode"),
    ("Comments", "Comentarios"),
    ("Queries", "Consultas"),
    ("Query", "Consulta"),
    ("Tables", "Tablas"),
    ("Table", "Tabla"),
    ("Columns", "Columnas"),
    ("Column", "Columna"),
    ("Database", "Base de datos"),
    ("Extract", "Extraer"),
    ("Using", "Usando"),
    ("Without", "Sin"),
    ("With", "Con"),
    ("Null Bytes", "Bytes nulos"),
    ("Linux Files", "Archivos Linux"),
    ("Windows Files", "Archivos Windows"),
    ("Current", "Actual"),
    ("Custom", "Personalizado"),
    ("Header", "Cabecera"),
    ("Headers", "Cabeceras"),
    ("Cookies", "Cookies"),
    ("Cookie", "Cookie"),
    ("Tokens", "Tokens"),
    ("Token", "Token"),
    ("Session", "Sesión"),
    ("Authentication", "Autenticación"),
    ("Authorization", "Autorización"),
    ("Injection", "Inyección"),
    ("Poisoning", "Envenenamiento"),
    ("Exfiltration", "Extracción de datos"),
    ("Information", "Información"),
    ("Disclosure", "Exposición"),
    ("Response", "Respuesta"),
    ("Request", "Solicitud"),
    ("Method", "Método"),
    ("Files", "Archivos"),
    ("File", "Archivo"),
    ("Data", "Datos"),
    ("Parameter", "Parámetro"),
    ("Parameters", "Parámetros"),
    ("Nested", "Anidado"),
    ("Double", "Doble"),
    ("Single", "Simple"),
    ("Different", "Diferentes"),
    ("Alternative", "Alternativa"),
    ("Other", "Otros"),
]

LISTAS = {
    "sql-injection": ["SQL Injection/Intruder"],
    "nosql-injection": ["NoSQL Injection/Intruder"],
    "command-injection": ["Command Injection/Intruder"],
    "xxe": ["XXE Injection/Intruders"],
    "ldap-injection": ["LDAP Injection/Intruder"],
    "crlf-injection": ["CRLF Injection/Files"],
    "code-injection": ["Server Side Include Injection/Files"],
    "xss": ["XSS Injection/Intruders"],
    "open-redirect": ["Open Redirect/Intruder"],
    "path-traversal-lfi": ["Directory Traversal/Intruder", "File Inclusion/Intruders"],
    "rfi": ["File Inclusion/Intruders"],
    "file-upload": ["Upload Insecure Files/Extension PHP", "Upload Insecure Files/Extension ASP"],
    "web-cache-deception": ["Web Cache Deception/Intruders"],
    "information-disclosure": [
        "Insecure Source Code Management/Files",
        "Insecure Management Interface/Intruder",
    ],
    "security-misconfiguration": ["Insecure Management Interface/Intruder"],
}

# Algunas guías comparten fuente, pero solo incorporan la sección aplicable.
FILTROS = {
    "fijacion-sesion": {
        "CRLF Injection/README.md": ("Session Fixation",),
    },
    "reset-password-poisoning": {
        "Account Takeover/README.md": ("Password Reset Feature",),
    },
    "host-header-injection": {
        "Account Takeover/README.md": ("Account Takeover Through Password Reset Poisoning",),
        "Web Cache Deception/README.md": ("Caching Custom JavaScript",),
    },
    "postmessage": {
        "XSS Injection/README.md": ("XSS in PostMessage",),
    },
    "rfi": {
        "File Inclusion/README.md": ("Remote File Inclusion",),
    },
    "web-cache-poisoning": {
        "Web Cache Deception/README.md": ("Caching Custom JavaScript",),
    },
}


def traducir(titulo: str) -> str:
    titulo = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", titulo)
    titulo = titulo.replace(MARCA, "").replace("**", "").strip()
    for original, espanol in sorted(FRASES, key=lambda par: len(par[0]), reverse=True):
        titulo = re.sub(r"\b" + re.escape(original) + r"\b", espanol, titulo, flags=re.I)
    for original, espanol in GLOSARIO:
        titulo = re.sub(r"\b" + re.escape(original) + r"\b", espanol, titulo, flags=re.I)
    return titulo[:1].upper() + titulo[1:]


def nombre_archivo(ruta: str, numero: int) -> str:
    nombre = Path(ruta).with_suffix("").as_posix().replace("/", "_")
    nombre = unicodedata.normalize("NFKD", nombre).encode("ascii", "ignore").decode()
    nombre = re.sub(r"[^A-Za-z0-9]+", "_", nombre).strip("_")
    return f"PATT_{numero:02d}_{nombre[:75]}.md"


def nombre_visible_documento(ruta: str) -> str:
    archivo = Path(ruta)
    nombre = archivo.parent.name if archivo.stem == "README" else archivo.stem
    return traducir(nombre)


def parece_payload(valor: str) -> bool:
    if any(c in valor for c in r"/\%<>'\x22=;{}[]():?&@#$*._+-"):
        return True
    if valor.isdigit() or valor.casefold() in {"true", "false", "null", "undefined", "nan"}:
        return True
    return bool(re.search(r"\b(SELECT|UNION|ORDER|GROUP|AND|OR|SLEEP|WAITFOR|EXEC|CAST|CONCAT|DOCTYPE)\b", valor, re.I))


def seccion_visible(ancestros: list[tuple[int, str]]) -> bool:
    return not any(t.lower() in OMITIR for _, t in ancestros)


def leer_ejemplos(ruta: Path):
    """Captura fences, código con sangría y variantes de tablas/listas en línea."""
    texto = ruta.read_text(encoding="utf-8", errors="replace")
    if ruta.name == "IIS-Machine-Keys.md":
        # Mantener la sintaxis de ViewState sin republicar claves concretas.
        texto = re.sub(r"\b[A-F0-9]{40,}\b", "{CLAVE_REDACTADA}", texto)
    texto = texto.replace("cweiske@php.net", "usuario@example.test")
    texto = texto.replace("schotte@mayflower.de", "usuario@example.test")
    secciones: OrderedDict[tuple[str, ...], dict] = OrderedDict()
    ancestros: list[tuple[int, str]] = []
    en_cerca = False
    marca_cerca = ""
    idioma = ""
    buffer: list[str] = []
    codigo_sangria: list[str] = []

    def actual():
        titulo = tuple(t for _, t in ancestros if t.lower() not in OMITIR)
        if not titulo:
            titulo = ("Ejemplos generales",)
        return secciones.setdefault(titulo, {"bloques": [], "inline": [], "inline_vistos": set()})

    def vaciar_sangria():
        nonlocal codigo_sangria
        if codigo_sangria and seccion_visible(ancestros):
            contenido = "\n".join(codigo_sangria).strip("\n")
            if contenido.strip():
                actual()["bloques"].append(("text", contenido))
        codigo_sangria = []

    for linea in texto.split("\n"):
        if en_cerca:
            cierre = CERCA.match(linea)
            if cierre and cierre.group(1)[0] == marca_cerca[0] and len(cierre.group(1)) >= len(marca_cerca):
                if seccion_visible(ancestros):
                    contenido = "\n".join(buffer).strip("\n")
                    if contenido.strip():
                        actual()["bloques"].append((idioma, contenido))
                buffer = []
                en_cerca = False
                continue
            buffer.append(linea)
            continue

        apertura = CERCA.match(linea)
        if apertura:
            vaciar_sangria()
            en_cerca = True
            marca_cerca = apertura.group(1)
            idioma = apertura.group(2).strip().split(" ", 1)[0] or "text"
            buffer = []
            continue

        encabezado = ENCABEZADO.match(linea)
        if encabezado:
            vaciar_sangria()
            nivel, titulo = len(encabezado.group(1)), encabezado.group(2).strip()
            while ancestros and ancestros[-1][0] >= nivel:
                ancestros.pop()
            ancestros.append((nivel, titulo))
            continue

        if linea.startswith("    ") and linea.strip() and not linea.lstrip().startswith(("* ", "- ")):
            codigo_sangria.append(linea[4:])
            continue
        vaciar_sangria()
        if not seccion_visible(ancestros):
            continue
        for valor in EN_LINEA.findall(linea):
            valor = valor.strip()
            if not valor or len(valor) > 700 or not parece_payload(valor):
                continue
            grupo = actual()
            if valor not in grupo["inline_vistos"]:
                grupo["inline"].append(valor)
                grupo["inline_vistos"].add(valor)
    vaciar_sangria()
    if en_cerca:
        raise ValueError(f"Cerca Markdown sin cerrar: {ruta}")
    return [(ruta_titulos, grupo) for ruta_titulos, grupo in secciones.items()
            if grupo["bloques"] or grupo["inline"]]


def enlace_fuente(ruta: str) -> str:
    return "https://github.com/swisskyrepo/PayloadsAllTheThings/blob/" + REVISION + "/" + quote(ruta, safe="/")


def renderizar_fuente(tema: dict, ruta: str, sec) -> tuple[str, int, int]:
    partes = [
        f"# {tema['titulo']}: anexo de ejemplos de PayloadsAllTheThings",
        "",
        "> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. "
        "Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, "
        "identificadores y dominios por los del laboratorio o alcance autorizado. "
        "Los ejemplos originales son referencias de sintaxis, no pruebas verificadas "
        "contra el objetivo.",
        "",
        f"**Documento de origen:** [{ruta}]({enlace_fuente(ruta)}), revisión fija "
        f"{REVISION[:12]}. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).",
        "",
        "[← Índice de anexos](Catalogo_PATT.md) · "
        "[← Guía principal](README.md)",
        "",
    ]
    cuenta_bloques = 0
    cuenta_inline = 0
    for numero, (ruta_titulos, grupo) in enumerate(sec, 1):
        # Mantener los dos últimos niveles permite entender el contexto sin títulos enormes.
        contexto = " / ".join(traducir(t) for t in ruta_titulos[-2:])
        partes.extend([f"## {numero}. {contexto}", ""])
        for idioma, codigo in grupo["bloques"]:
            # Evita que el contenido de upstream cierre accidentalmente la cerca.
            largo = max(3, max((len(m.group(0)) for m in re.finditer(re.escape(MARCA) + r"{3,}", codigo)), default=0) + 1)
            cerca = MARCA * largo
            partes.extend([f"{cerca}{idioma}", codigo, cerca, ""])
            cuenta_bloques += 1
        if grupo["inline"]:
            partes.extend(["### Variantes presentes en tablas o texto del apartado", "",
                           f"{FENCE}text", "\n".join(grupo["inline"]), FENCE, ""])
            cuenta_inline += len(grupo["inline"])
    partes.extend([
        "---", "",
        "[← Índice de anexos](Catalogo_PATT.md) · "
        "[← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)",
        "",
    ])
    return "\n".join(partes), cuenta_bloques, cuenta_inline


def generar(upstream: Path) -> dict:
    head = subprocess.check_output(["git", "-C", str(upstream), "rev-parse", "HEAD"], text=True).strip()
    if head != REVISION:
        raise SystemExit(f"Revisión PATT distinta: {head}; se requiere {REVISION}")
    esperados = {t["slug"] for t in TEMAS}
    if set(MAPA) != esperados:
        raise SystemExit(f"Mapa incompleto: faltan {esperados - set(MAPA)}, sobran {set(MAPA) - esperados}")
    licencia = (upstream / "LICENSE").read_text(encoding="utf-8")
    (RAIZ / "LICENCIA_PATT.md").write_text(
        "# Licencia del material de PayloadsAllTheThings\n\n"
        "Los anexos técnicos indicados como PATT incorporan ejemplos de "
        "[PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings) "
        f"de la revisión {REVISION}. Se conserva el aviso legal original completo:\n\n"
        + licencia + "\n", encoding="utf-8")

    stats = {"temas": 0, "documentos": 0, "bloques": 0, "inline": 0,
             "listas": 0, "lineas_listas": 0}
    for tema in TEMAS:
        destino = RAIZ / tema["carpeta"] / "Payloads_hack"
        for previo in destino.glob("PATT_*.md"):
            previo.unlink()
        for previo in destino.glob("PATT_LISTA_*"):
            previo.unlink()
        entradas = []
        for numero, ruta in enumerate(MAPA[tema["slug"]], 1):
            origen = upstream / ruta
            if not origen.is_file():
                raise SystemExit(f"Fuente PATT ausente: {ruta}")
            sec = leer_ejemplos(origen)
            incluidos = FILTROS.get(tema["slug"], {}).get(ruta)
            if incluidos:
                sec = [
                    (titulos, grupo) for titulos, grupo in sec
                    if any(termino.casefold() in titulo.casefold()
                           for termino in incluidos for titulo in titulos)
                ]
            if not sec:
                continue
            nombre = nombre_archivo(ruta, numero)
            contenido, bloques, inline = renderizar_fuente(tema, ruta, sec)
            (destino / nombre).write_text(contenido, encoding="utf-8")
            entradas.append((nombre, ruta, len(sec), bloques, inline))
            stats["documentos"] += 1
            stats["bloques"] += bloques
            stats["inline"] += inline
        stats["temas"] += 1
        listas = []
        for carpeta_rel in LISTAS.get(tema["slug"], []):
            carpeta = upstream / carpeta_rel
            if not carpeta.is_dir():
                raise SystemExit(f"Carpeta de listas PATT ausente: {carpeta_rel}")
            archivos = sorted(x for x in carpeta.iterdir() if x.is_file() and x.suffix in {".txt", ".lst"})
            for archivo in archivos:
                ruta_rel = archivo.relative_to(upstream).as_posix()
                nombre = "PATT_LISTA_" + re.sub(
                    r"[^A-Za-z0-9_.-]+", "_",
                    carpeta.parent.name + "_" + carpeta.name + "_" + archivo.name)
                shutil.copyfile(archivo, destino / nombre)
                lineas = len(archivo.read_bytes().splitlines())
                listas.append((nombre, ruta_rel, lineas))
                stats["listas"] += 1
                stats["lineas_listas"] += lineas
        indice = [
            f"# Banco ampliado: {tema['titulo']}", "",
            ("Este índice ordena los ejemplos técnicos reproducidos o adaptados de "
             "PayloadsAllTheThings por documento y situación. Los títulos explican "
             "el contexto en español y conservan los nombres técnicos de motores "
             "y funciones; el código mantiene la sintaxis de origen. "
             "Consulta primero [los payloads básicos y las pruebas guiadas](README.md)."
             if entradas else
             "Esta vulnerabilidad no tiene un capítulo técnico equivalente en la "
             "revisión consultada de PayloadsAllTheThings. Consulta "
             "[los payloads básicos y las pruebas guiadas](README.md) y la "
             "ampliación original de esta carpeta."),
            "",
            f"**Versión de origen:** [{REVISION[:12]}]"
            f"(https://github.com/swisskyrepo/PayloadsAllTheThings/tree/{REVISION}) · "
            "[Licencia MIT y atribución](../../LICENCIA_PATT.md).", "",
        ]
        if entradas:
            indice.extend([
                "| Documento técnico | Apartados | Bloques de código | Variantes en línea |",
                "| --- | ---: | ---: | ---: |",
            ])
            for nombre, ruta, apartados, bloques, inline in entradas:
                indice.append(
                    f"| [{nombre_visible_documento(ruta)}]({quote(nombre)}) | "
                    f"{apartados} | {bloques} | {inline} |")
        else:
            indice.extend([
                "La ampliación se organiza por situaciones propias de esta vulnerabilidad:",
            ])
            if (destino / "Ampliacion_original.md").is_file():
                indice.extend([
                    "",
                    "[Abrir la ampliación original por situaciones]"
                    "(Ampliacion_original.md).",
                ])
        if listas:
            indice.extend([
                "", "## Diccionarios de payloads para Intruder y fuzzing", "",
                "Cada archivo conserva sus líneas de origen y se debe usar con "
                "el punto de entrada y la profundidad adecuados. No ejecutar "
                "los diccionarios completos contra un programa sin comprobar "
                "sus límites de frecuencia y volumen.", "",
                "| Lista | Líneas | Fuente |", "| --- | ---: | --- |",
            ])
            for nombre, ruta_rel, lineas in listas:
                indice.append(
                    f"| [{nombre.removeprefix('PATT_LISTA_')}]({quote(nombre)}) | "
                    f"{lineas} | [Origen]({enlace_fuente(ruta_rel)}) |")
        indice.extend(["", "---", "",
                       "[← Guía principal](README.md) · "
                       "[← Índice general](../../README.md)", ""])
        (destino / "Catalogo_PATT.md").write_text("\n".join(indice), encoding="utf-8")
    (RAIZ / "tools" / "patt_stats.json").write_text(
        json.dumps(stats, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    return stats


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--upstream", type=Path, required=True)
    args = parser.parse_args()
    print(generar(args.upstream.resolve()))
