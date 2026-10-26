# 🗡️ Header injection: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. IP declarada

**Objetivo:** Comprobar si se confía en una IP aportada por cliente.

```http
GET /api/me HTTP/1.1
Host: {ORIGEN}
X-Forwarded-For: 127.0.0.1
```

**Interpretación:** Un cambio de respuesta exige confirmar qué capa lo causó; no asumir bypass.

### 2. Cabecera de marcador

**Objetivo:** Trazar propagación sin efectos.

```http
GET /api/me HTTP/1.1
Host: {ORIGEN}
X-Prueba: prueba-123
```

**Interpretación:** Buscar solo el marcador en respuesta o logs autorizados.

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../../README.md)
