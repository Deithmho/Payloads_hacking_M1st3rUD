# 🗡️ Server-Side Template Injection (SSTI): payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Expresión Jinja2/Twig

**Objetivo:** Primer canary aritmético cuando el dato se renderiza como fuente de plantilla.

```text
{{7*7}}
```

**Interpretación:** 49 en la respuesta cruda sugiere evaluación, pero algunas plantillas cliente comparten sintaxis; comparar renderizado servidor.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/README.md).

### 2. Diferencial Jinja2 frente a Twig

**Objetivo:** La multiplicación por string suele distinguir motores; validar en laboratorio.

```text
{{7*'7'}}
```

**Interpretación:** Jinja2 suele repetir la cadena, Twig la convierte a número. Confirmar versión y un segundo canary.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/README.md).

### 3. FreeMarker

**Objetivo:** Aplicable cuando se sospecha motor Java FreeMarker.

```text
${7*7}
```

**Interpretación:** Una salida 49 debe aparecer antes de ejecutar JavaScript cliente y variar frente a ${7+7}.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/README.md).

### 4. ERB Ruby

**Objetivo:** Aplicable a plantillas ERB renderizadas en backend.

```text
<%= 7*7 %>
```

**Interpretación:** El servidor debe emitir 49; si el texto queda literal, no se confirmó ERB.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/README.md).

### 5. Pug/Jade

**Objetivo:** Aplicable a plantillas Pug que interpolan con #{...}.

```text
#{7*7}
```

**Interpretación:** Confirmar en la respuesta HTTP original y un control literal.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/README.md).

### 6. Thymeleaf inlining

**Objetivo:** Aplicable solo cuando está activa la evaluación en línea del motor Thymeleaf.

```text
[[${7*7}]]
```

**Interpretación:** No confundir con texto que el navegador transforma después; inspeccionar respuesta cruda.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/README.md).

### 7. Error diferenciado sin comandos

**Objetivo:** Solo en un template de laboratorio para observar manejo de errores.

```text
{{(1/0).marca_prueba}}
```

**Interpretación:** Un error específico del motor puede ayudar a identificarlo; un 500 genérico no prueba SSTI.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/README.md).

### 8. Filtro Jinja2 de transformación

**Objetivo:** Diferenciar evaluación de simple aritmética permitida.

```text
{{'prueba-123'|upper}}
```

**Interpretación:** Una salida PRUEBA-123 en respuesta cruda indica interpretación del filtro; comprobar control literal.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/README.md).

### 9. FreeMarker built-in de texto

**Objetivo:** Aplicable solo a sintaxis FreeMarker.

```text
${'prueba-123'?upper_case}
```

**Interpretación:** El resultado en mayúsculas ayuda a identificar motor; un error de parser no confirma explotación.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/README.md).

### 10. Apache Velocity #set

**Objetivo:** Aplicable a Velocity en Java cuando entrada se interpreta como plantilla completa.

```text
#set($marca = 7 * 7)$marca
```

**Interpretación:** 49 en salida cruda indica evaluación de directiva, distinto de interpolación de variable.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/README.md).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
