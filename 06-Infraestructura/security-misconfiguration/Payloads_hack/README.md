# 🗡️ Configuración de seguridad incorrecta: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Cabeceras por ruta

**Objetivo:** Comparar recurso público y privado.

```bash
curl -I "https://{ORIGEN}/api/me"
```

**Interpretación:** Verificar `Cache-Control`, CSP y framing en el recurso pertinente.

### 2. Métodos declarados

**Objetivo:** Inventariar sin alterar estado.

```http
OPTIONS /api/test-owned HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** `Allow` es pista; comprobar autorización efectiva en un objeto propio.

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../../README.md)
