# 🗡️ DOM clobbering: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Global inocuo

**Objetivo:** Comprobar si el nodo altera un global en laboratorio.

```html
<a id="configPrueba" href="#marcador">prueba</a>
```

**Interpretación:** En consola, comparar `window.configPrueba` antes/después; buscar código que lo use.

### 2. Nombre de formulario

**Objetivo:** Detectar colisión con método sin enviar datos.

```html
<form id="f"><input name="submit" value="prueba"></form>
```

**Interpretación:** En laboratorio, inspeccionar `typeof f.submit`; no equivale a exploit.

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../../README.md)
