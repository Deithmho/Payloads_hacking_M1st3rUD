# 🗡️ HTTP Request Smuggling: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Control de laboratorio

**Objetivo:** Documentar una request ambigua solo para un lab aislado.

```http
POST / HTTP/1.1
Host: {LAB_AISLADO}
Content-Length: 6
Transfer-Encoding: chunked

0

X
```

**Interpretación:** No usar contra producción: el impacto puede recaer en la siguiente request de otra persona.

### 2. Control normal

**Objetivo:** Comparar parsing sin ambigüedad.

```http
POST / HTTP/1.1
Host: {LAB_AISLADO}
Content-Length: 0
```

**Interpretación:** Una diferencia no basta; seguir metodología de investigación y descartar pipelining.

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../../README.md)
