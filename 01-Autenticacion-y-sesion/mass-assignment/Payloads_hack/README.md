# 🗡️ Mass assignment: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Campo no editable

**Objetivo:** Verificar rechazo de propiedad de rol en cuenta propia.

```http
PATCH /api/me HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
Content-Type: application/json

{"displayName":"prueba-123","role":"admin"}
```

**Interpretación:** Confirmar persistencia y privilegios; un eco en JSON no basta.

### 2. Propietario en objeto propio

**Objetivo:** Comprobar que el owner no sea editable.

```json
{"name":"prueba-123","ownerId":"{ID_CONTROLADO_B}"}
```

**Interpretación:** Debe rechazarse o ignorarse `ownerId`; usar únicamente objetos de A y B.

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../../README.md)
