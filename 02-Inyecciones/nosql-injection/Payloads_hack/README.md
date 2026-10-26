# 🗡️ NoSQL injection: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Operador inesperado

**Objetivo:** Verificar que una cadena no acepte un objeto operador.

```json
{"username":{"$ne":"prueba-inexistente"},"password":"valor-control"}
```

**Interpretación:** El servidor debe rechazar el tipo u operar de forma segura; no inferir bypass por un error.

### 2. Filtro regex en objeto propio

**Objetivo:** Comprobar interpretación de operador.

```json
{"name":{"$regex":"^prueba-123$"}}
```

**Interpretación:** Comparar con búsqueda literal y confirmar solo sobre registros de prueba.

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../../README.md)
