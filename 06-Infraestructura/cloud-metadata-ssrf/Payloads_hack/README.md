# 🗡️ SSRF hacia metadatos cloud: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Verificación de egress propia

**Objetivo:** Establecer primero que existe SSRF sin tocar metadata.

```json
{"url":"https://{CONTROLLED_HOST}/metadata-precheck"}
```

**Interpretación:** Callback externa es solo precondición; no implica alcance cloud.

### 2. Laboratorio de metadata simulada

**Objetivo:** Probar controles HTTP sin credenciales reales.

```http
GET /latest/meta-data/instance-id HTTP/1.1
Host: {SERVIDOR_METADATA_SIMULADO}
```

**Interpretación:** Usar simulador o entorno propio; no recolectar roles ni tokens de producción.

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../../README.md)
