# 🗡️ DNS rebinding: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Laboratorio DNS

**Objetivo:** Registrar resoluciones alternas propias.

```text
A {DOMINIO_CONTROLADO}: 198.51.100.10 -> 198.51.100.11 (ambas IPs de laboratorio)
```

**Interpretación:** Documentar IP de conexión final; no usar 127.0.0.1 ni metadata en producción.

### 2. Canary de URL

**Objetivo:** Comprobar si fetch usa nombre controlado.

```json
{"url":"https://{CONTROLLED_HOST}/dns-prueba-123"}
```

**Interpretación:** Una callback normal solo demuestra fetch, no rebinding.

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../../README.md)
