# 🗡️ LDAP injection: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Comodín literal

**Objetivo:** Verificar si el filtro interpreta `*`.

```http
GET /api/directory?name=prueba%2A HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Comparar con la búsqueda literal de un registro propio; resultados amplios no prueban login.

### 2. Paréntesis de control

**Objetivo:** Detectar parser de filtro sin atacar cuentas.

```text
prueba)(uid=prueba-123
```

**Interpretación:** Errores LDAP o diferencias necesitan un control válido y no implican acceso.

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../../README.md)
