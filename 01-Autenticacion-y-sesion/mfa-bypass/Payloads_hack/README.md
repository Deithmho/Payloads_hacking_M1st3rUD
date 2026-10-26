# 🗡️ Bypass de MFA: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Ruta final con MFA pendiente

**Objetivo:** Comprobar enforcement servidor.

```http
GET /api/me HTTP/1.1
Host: {ORIGEN}
Cookie: session={SESION_MFA_PENDIENTE}
```

**Interpretación:** Una respuesta con datos privados indica que la ruta no exige el segundo factor.

### 2. Acción sensible

**Objetivo:** Verificar un flujo propio antes de MFA.

```http
GET /api/security/settings HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_MFA_PENDIENTE}
```

**Interpretación:** Debe rechazarse o limitarse a configurar/completar MFA.

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../../README.md)
