# 🗡️ Exposición excesiva de datos en API: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Respuesta completa

**Objetivo:** Inspeccionar JSON de objeto propio.

```bash
curl -s -H "Authorization: Bearer {TOKEN_A}" "https://{ORIGEN}/api/me" | jq "keys"
```

**Interpretación:** Usar valores propios y redactar cualquier campo sensible en evidencia.

### 2. Comparación de roles

**Objetivo:** Detectar campos extra en rol bajo.

```text
Comparar claves JSON de {TOKEN_ROL_BAJO} y {TOKEN_ROL_ALTO} para el mismo objeto propio.
```

**Interpretación:** Demostrar por qué el campo extra es sensible para el rol bajo.

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../../README.md)
