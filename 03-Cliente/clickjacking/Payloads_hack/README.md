# 🗡️ Clickjacking: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Comprobar framing

**Objetivo:** Cargar una página propia en un iframe de origen controlado.

```html
<iframe src="https://{ORIGEN}/settings" width="900" height="600"></iframe>
```

**Interpretación:** Comprobar renderizado y una acción de prueba reversible; no basta ausencia de cabeceras.

### 2. Cabeceras

**Objetivo:** Inspeccionar políticas efectivas.

```bash
curl -I "https://{ORIGEN}/settings"
```

**Interpretación:** Revisar CSP `frame-ancestors` y `X-Frame-Options` junto con comportamiento real.

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../../README.md)
