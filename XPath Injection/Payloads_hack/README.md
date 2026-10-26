# 🗡️ XPath injection: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Comilla simple de diagnóstico

**Objetivo:** El parámetro se inserta en una cadena XPath delimitada por comillas simples.

```text
prueba'
```

**Interpretación:** Un error del parser es pista, no explotación; comparar con cadena válida.

**Fuente técnica:** [documentación de la técnica](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/07-Injection/09-XPath_Injection/).

### 2. Booleano verdadero

**Objetivo:** Consulta de laboratorio similar a //item[name='ENTRADA'].

```text
prueba' or '1'='1
```

**Interpretación:** Debe alterar selección de nodos propios y no solo el código de respuesta.

**Fuente técnica:** [documentación de la técnica](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/07-Injection/09-XPath_Injection/).

### 3. Booleano falso

**Objetivo:** Control de la variante anterior manteniendo forma sintáctica.

```text
prueba' or '1'='2
```

**Interpretación:** Una diferencia estable verdadero/falso apoya control del predicado.

**Fuente técnica:** [documentación de la técnica](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/07-Injection/09-XPath_Injection/).

### 4. starts-with sobre nodo propio

**Objetivo:** Adaptar XPath al esquema XML del laboratorio; no adivinar datos ajenos.

```text
prueba' or starts-with(//item[@id='own']/name,'prueba') or 'a'='b
```

**Interpretación:** El resultado depende del valor en el nodo propio; comprobar condición falsa cambiando prefijo.

**Fuente técnica:** [documentación de la técnica](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/07-Injection/09-XPath_Injection/).

### 5. contains sobre nodo propio

**Objetivo:** Verificar evaluación de función XPath 1.0.

```text
prueba' or contains(//item[@id='own']/name,'ueba') or 'a'='b
```

**Interpretación:** Contrastar con subcadena imposible para descartar reflexión.

**Fuente técnica:** [documentación de la técnica](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/07-Injection/09-XPath_Injection/).

### 6. string-length

**Objetivo:** Probar un dato de longitud conocida del XML de prueba.

```text
prueba' or string-length(//item[@id='own']/name)=10 or 'a'='b
```

**Interpretación:** Sustituir 10 por longitud real y comparar con 11; no extraer datos ajenos.

**Fuente técnica:** [documentación de la técnica](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/07-Injection/09-XPath_Injection/).

### 7. count de nodos propios

**Objetivo:** Medir selección de nodos de prueba mediante XPath.

```text
prueba' or count(//item[@id='own'])=1 or 'a'='b
```

**Interpretación:** Un resultado distinto requiere control count(...)=2 y observación del nodo devuelto.

**Fuente técnica:** [documentación de la técnica](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/07-Injection/09-XPath_Injection/).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
