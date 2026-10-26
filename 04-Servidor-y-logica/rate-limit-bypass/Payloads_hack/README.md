# 🗡️ Bypass de rate limit: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Contador de prueba

**Objetivo:** Comparar unas pocas solicitudes con la misma cuenta.

```bash
for n in 1 2 3; do curl -s -o /dev/null -w "%{http_code}\n" "https://{ORIGEN}/api/test-owned"; done
```

**Interpretación:** Respetar programa; registrar efecto real y no declarar bypass solo por 200.

### 2. IP aportada

**Objetivo:** Verificar si cambia la clave del contador.

```http
GET /api/test-owned HTTP/1.1
Host: {ORIGEN}
X-Forwarded-For: 192.0.2.123
```

**Interpretación:** Comparar únicamente bajo límite pequeño pactado y con control sin cabecera.

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../../README.md)
