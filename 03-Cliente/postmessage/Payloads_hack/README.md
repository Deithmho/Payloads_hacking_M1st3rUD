# 🗡️ Vulnerabilidades de postMessage: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Mensaje de marcador

**Objetivo:** Probar receptor desde origen controlado.

```js
window.opener?.postMessage({type:"probe",value:"prueba-123"}, "https://{ORIGEN}");
```

**Interpretación:** Observar una acción concreta del receptor; no inferir confianza por ausencia de error.

### 2. Receptor instrumentado

**Objetivo:** Inspeccionar mensajes recibidos en ventana propia.

```js
addEventListener("message", e => console.log(e.origin, e.data));
```

**Interpretación:** Usar solo datos de cuenta propia y comprobar si el emisor usa un destino demasiado amplio.

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../../README.md)
