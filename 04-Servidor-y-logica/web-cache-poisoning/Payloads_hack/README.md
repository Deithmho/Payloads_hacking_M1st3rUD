# 🗡️ Web cache poisoning: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Marcador en ruta única

**Objetivo:** Probar almacenamiento sin tocar página popular.

```http
GET /prueba-cache-123 HTTP/1.1
Host: {ORIGEN}
X-Forwarded-Host: {CONTROLLED_HOST}
```

**Interpretación:** Solicitar la misma URL sin header desde otra sesión y buscar el marcador.

### 2. Control cachebuster

**Objetivo:** Descartar reflexión normal.

```http
GET /prueba-cache-123?cb=control HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Comparar cabeceras y contenido; no usar payload activo.

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../../README.md)
