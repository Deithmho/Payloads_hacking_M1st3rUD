# 🗡️ Tabnabbing y engaño de pestañas: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Inspección de enlace

**Objetivo:** Comprobar atributos y comportamiento.

```html
<a href="https://{CONTROLLED_HOST}/prueba" target="_blank" rel="noopener noreferrer">Prueba</a>
```

**Interpretación:** Este ejemplo es la forma segura; comparar con el enlace real.

### 2. Control de opener

**Objetivo:** Medir en el navegador usado por el programa.

```js
console.log(window.opener === null ? "aislado" : "opener disponible");
```

**Interpretación:** La referencia disponible es condición, no explotación de phishing.

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../../README.md)
