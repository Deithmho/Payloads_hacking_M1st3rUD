# 🗡️ Cross-Site Scripting (XSS): payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Contexto HTML

**Objetivo:** Comprobar ejecución inocua en entorno de prueba.

```html
<img src=x onerror="document.body.dataset.prueba='123'">
```

**Interpretación:** Verificar el atributo en DOM; no enviar datos a otro origen.

### 2. Contexto atributo

**Objetivo:** Probar salida de un atributo entre comillas.

```html
"><svg onload="document.body.dataset.prueba='123'"></svg>
```

**Interpretación:** Solo tiene sentido si la entrada cae en un atributo HTML; inspeccionar fuente y DOM.

### 3. DOM-based

**Objetivo:** Probar una fuente de fragmento solo cuando un script la inserta en HTML.

```text
#<img src=x onerror="document.body.dataset.prueba=123">
```

**Interpretación:** Requiere que el JavaScript copie `location.hash` a `innerHTML` u otro sink; observar DOM y ejecución.

### 4. Persistencia

**Objetivo:** Usar un campo propio que se renderice después.

```json
{"comment":"<img src=x onerror=\"document.body.dataset.prueba=123\">"}
```

**Interpretación:** Verificar guardado y renderizado en una segunda sesión de prueba; no involucrar usuarios reales.

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../../README.md)
