# 🗡️ Límites insuficientes de recursos en API: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Paginación acotada

**Objetivo:** Comprobar máximo permitido con un valor moderado.

```http
GET /api/items?limit=101 HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
```

**Interpretación:** Comparar con máximo documentado; no solicitar volúmenes grandes.

### 2. Control de cuota

**Objetivo:** Leer cabeceras y respuesta de pocas solicitudes.

```bash
curl -i -H "Authorization: Bearer {TOKEN_A}" "https://{ORIGEN}/api/items?limit=2"
```

**Interpretación:** Ausencia de cabeceras no equivale a ausencia de límite interno.

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../../README.md)
