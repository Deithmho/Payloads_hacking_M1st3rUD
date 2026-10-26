# 🗡️ Clickjacking y framing: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Página sensible en iframe

**Objetivo:** Verificar framing desde origen de prueba.

```html
<iframe src="https://{ORIGEN}/account/settings" width="900" height="600"></iframe>
```

**Interpretación:** Comprobar carga y control accionable bajo cuenta propia.

### 2. Respuesta de la ruta

**Objetivo:** Revisar cabeceras de esa página concreta.

```bash
curl -I "https://{ORIGEN}/account/settings"
```

**Interpretación:** El header debe estar en la respuesta embebida, no solo en la página principal.

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../../README.md)
