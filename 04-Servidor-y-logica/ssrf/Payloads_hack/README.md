# 🗡️ Server-Side Request Forgery (SSRF): payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Canary de salida

**Objetivo:** Demostrar request desde backend sin tocar terceros.

```json
{"url":"https://{CONTROLLED_HOST}/ssrf-prueba-123"}
```

**Interpretación:** Correlacionar hora, ruta y cabeceras del callback; distinguir navegador de backend.

### 2. Redirección controlada

**Objetivo:** Comprobar si el cliente sigue redirecciones hacia otro host propio.

```text
https://{CONTROLLED_HOST}/redirigir-a-segundo-host-propio
```

**Interpretación:** Ambos hosts deben ser propios; registrar cada salto.

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../../README.md)
