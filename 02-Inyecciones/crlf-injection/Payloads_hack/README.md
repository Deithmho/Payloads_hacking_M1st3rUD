# 🗡️ CRLF injection: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Nueva cabecera

**Objetivo:** Comprobar separación real.

```http
GET /redirect?next=%2Fok%0d%0aX-Prueba:%20prueba-123 HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Inspeccionar encabezados crudos, no solo vista renderizada.

### 2. Control codificado

**Objetivo:** Descartar reflejo literal.

```http
GET /redirect?next=%2Fok%250d%250aX-Prueba HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Si aparece texto codificado pero no cabecera nueva, no hay CRLF confirmado.

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../../README.md)
