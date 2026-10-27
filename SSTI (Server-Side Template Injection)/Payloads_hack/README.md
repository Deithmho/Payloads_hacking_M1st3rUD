# 🗡️ Server-Side Template Injection (SSTI): payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 📚 Banco ampliado de payloads

[Abrir el catálogo por técnica y los diccionarios de PayloadsAllTheThings](Catalogo_PATT.md). Los bloques de esta guía explican las pruebas iniciales; el catálogo reúne variantes adicionales por motor, parser y contexto.

> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.

## 💉 Payloads básicos

### Aritmética por familia de plantilla

```text
{{7*7}}
${7*7}
<%= 7*7 %>
#{7*7}
```

**Cuándo usarlo:** Una línea por solicitud; delimitadores corresponden a motores distintos. 49 repetible indica evaluación solo tras descartar transformación/reflejo.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/server-side-template-injection).


### Comparar literal con expresión

```text
prueba-123
{{7*7}}
{{7*"7"}}
```

**Cuándo usarlo:** La tercera línea ayuda a diferenciar semánticas: Jinja2 puede repetir una cadena, Twig suele calcular; confirmar con error o huella del motor.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/server-side-template-injection).


## 🧭 Payloads por contexto

### Jinja2/Twig sin llamadas peligrosas

```text
{{(2+3)*4}}
{{'prueba-' ~ '123'}}
{{7*'7'}}
```

**Cuándo usarlo:** Cada línea es independiente. Ajustar comillas y filtros al motor; la evaluación matemática no demuestra acceso a objetos del servidor.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/server-side-template-injection).


### FreeMarker y ERB

```text
${(2+3)*4}
${"prueba-" + "123"}
<%= (2+3)*4 %>
<%= "prueba-" + "123" %>
```

**Cuándo usarlo:** Dos sintaxis separadas (Java FreeMarker y Ruby ERB), cada línea individual. Aplicar solo donde el motor esté identificado.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/server-side-template-injection).


## 🔥 Payloads avanzados

### Entrada dentro de una expresión existente

```text
}}
}}prueba-123{{
}}<b>prueba-123</b>{{
```

**Cuándo usarlo:** Solo cuando la aplicación inserta la entrada dentro de {{...}}. Son fragmentos para estudiar cierre de contexto, no documentos de plantilla completos.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/server-side-template-injection).


## 🔬 Pruebas guiadas por escenario

### 1. Expresión Jinja2/Twig

**Objetivo:** Primer canary aritmético cuando el dato se renderiza como fuente de plantilla.

```text
{{7*7}}
```

**Interpretación:** 49 en la respuesta cruda sugiere evaluación, pero algunas plantillas cliente comparten sintaxis; comparar renderizado servidor.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/README.md).

### 2. Diferencial Jinja2 frente a Twig

**Objetivo:** La multiplicación por string suele distinguir motores; validar en laboratorio.

```text
{{7*'7'}}
```

**Interpretación:** Jinja2 suele repetir la cadena, Twig la convierte a número. Confirmar versión y un segundo canary.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/README.md).

### 3. FreeMarker

**Objetivo:** Aplicable cuando se sospecha motor Java FreeMarker.

```text
${7*7}
```

**Interpretación:** Una salida 49 debe aparecer antes de ejecutar JavaScript cliente y variar frente a ${7+7}.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/README.md).

### 4. ERB Ruby

**Objetivo:** Aplicable a plantillas ERB renderizadas en backend.

```text
<%= 7*7 %>
```

**Interpretación:** El servidor debe emitir 49; si el texto queda literal, no se confirmó ERB.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/README.md).

### 5. Pug/Jade

**Objetivo:** Aplicable a plantillas Pug que interpolan con #{...}.

```text
#{7*7}
```

**Interpretación:** Confirmar en la respuesta HTTP original y un control literal.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/README.md).

### 6. Thymeleaf inlining

**Objetivo:** Aplicable solo cuando está activa la evaluación en línea del motor Thymeleaf.

```text
[[${7*7}]]
```

**Interpretación:** No confundir con texto que el navegador transforma después; inspeccionar respuesta cruda.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/README.md).

### 7. Error diferenciado sin comandos

**Objetivo:** Solo en un template de laboratorio para observar manejo de errores.

```text
{{(1/0).marca_prueba}}
```

**Interpretación:** Un error específico del motor puede ayudar a identificarlo; un 500 genérico no prueba SSTI.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/README.md).

### 8. Filtro Jinja2 de transformación

**Objetivo:** Diferenciar evaluación de simple aritmética permitida.

```text
{{'prueba-123'|upper}}
```

**Interpretación:** Una salida PRUEBA-123 en respuesta cruda indica interpretación del filtro; comprobar control literal.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/README.md).

### 9. FreeMarker built-in de texto

**Objetivo:** Aplicable solo a sintaxis FreeMarker.

```text
${'prueba-123'?upper_case}
```

**Interpretación:** El resultado en mayúsculas ayuda a identificar motor; un error de parser no confirma explotación.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/README.md).

### 10. Apache Velocity #set

**Objetivo:** Aplicable a Velocity en Java cuando entrada se interpreta como plantilla completa.

```text
#set($marca = 7 * 7)$marca
```

**Interpretación:** 49 en salida cruda indica evaluación de directiva, distinto de interpolación de variable.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/README.md).

### 11. Django Template: widthratio

**Objetivo:** Solo si se renderiza una plantilla Django, no Jinja2; directiva sin acceso a sistema.

```text
{% widthratio 7 7 49 %}
```

**Interpretación:** Una salida 49 en respuesta HTTP cruda demuestra evaluación de la directiva; no implica ejecución Python.

**Fuente técnica:** [docs.djangoproject.com](https://docs.djangoproject.com/en/dev/ref/templates/builtins/#widthratio).

### 12. Mako: método Python sobre literal

**Objetivo:** Confirmar Mako cuando `${}` podría confundirse con FreeMarker.

```text
${'prueba-123'.upper()}
```

**Interpretación:** PRUEBA-123 sugiere semántica Python/Mako; contrastar con una segunda expresión del motor.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/Python.md).

### 13. Smarty: función math

**Objetivo:** Solo en un campo que pasa a una plantilla Smarty completa.

```text
{math equation="7*7"}
```

**Interpretación:** 49 confirma evaluación de una función de Smarty en servidor; una vista previa legítima debe evaluarse según contrato.

**Fuente técnica:** [www.smarty.net](https://www.smarty.net/docs/en/language.function.math.tpl).

### 14. EJS Node: método JavaScript

**Objetivo:** Desambiguar EJS de ERB cuando ambos aceptan etiquetas `<%= ... %>`.

```text
<%= 'prueba-123'.toUpperCase() %>
```

**Interpretación:** PRUEBA-123 en respuesta cruda indica evaluación JS; ERB no tiene ese método.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/JavaScript.md).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
