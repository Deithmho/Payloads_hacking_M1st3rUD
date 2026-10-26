# 🗡️ XPath injection: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Condición verdadera

**Objetivo:** Comparar búsqueda de prueba.

```text
prueba' or '1'='1
```

**Interpretación:** Debe contrastarse con búsqueda legítima y observar nodos propios.

### 2. Condición falsa

**Objetivo:** Control negativo de la misma forma.

```text
prueba' or '1'='2
```

**Interpretación:** La diferencia repetible apoya la hipótesis; un error solo no basta.

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../../README.md)
