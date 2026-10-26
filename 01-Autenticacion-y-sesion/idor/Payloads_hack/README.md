# 🗡️ IDOR: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Lectura cruzada A→B

**Objetivo:** Validar acceso de A al objeto propio de B.

```http
GET /api/objects/{ID_CONTROLADO_B} HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A}
```

**Interpretación:** Un 200 con datos de B confirma lectura cruzada; un 200 vacío no.

### 2. ID en cuerpo

**Objetivo:** Comprobar una referencia anidada sin modificar datos.

```json
{"objectId":"{ID_CONTROLADO_B}","include":"summary"}
```

**Interpretación:** Verificar que la respuesta no incluya detalles de B bajo la sesión A.

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../../README.md)
