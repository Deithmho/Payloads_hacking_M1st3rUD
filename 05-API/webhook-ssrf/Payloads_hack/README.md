# 🗡️ SSRF mediante webhooks: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Callback propio

**Objetivo:** Establecer línea base de entrega.

```json
{"url":"https://{CONTROLLED_HOST}/webhook-prueba-123","events":["test"]}
```

**Interpretación:** Registrar origen, método y tipo de dato; no conservar secretos.

### 2. Redirección propia

**Objetivo:** Verificar política del cliente HTTP.

```text
https://{CONTROLLED_HOST}/redirigir-a-otro-host-propio
```

**Interpretación:** No redirigir a IPs internas o metadata fuera de laboratorio.

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../../README.md)
