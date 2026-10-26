# 🗡️ Autenticación rota: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Acceso sin sesión

**Objetivo:** Comprobar cierre de una ruta privada.

```http
GET /api/me HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Un 200 con datos privados sin sesión es indicio; un 200 genérico no lo es.

### 2. Sesión revocada

**Objetivo:** Verificar invalidez tras logout con token propio.

```http
GET /api/me HTTP/1.1
Host: {ORIGEN}
Authorization: Bearer {TOKEN_A_REVOCADO}
```

**Interpretación:** La respuesta debe negar acceso o exigir una nueva autenticación.

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../../README.md)
