# 🗡️ Email header injection: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Cc a cuenta propia

**Objetivo:** Probar sin destinatarios ajenos.

```text
Prueba%0d%0aCc:%20{EMAIL_PROPIO_2}
```

**Interpretación:** Confirmar en cabeceras crudas de un mensaje de prueba.

### 2. Control literal

**Objetivo:** Descartar simple reflejo en plantilla.

```text
Prueba-Cc-{EMAIL_PROPIO_2}
```

**Interpretación:** No debe crearse una cabecera nueva.

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../../README.md)
