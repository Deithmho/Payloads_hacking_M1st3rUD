# 🗡️ Fijación de sesión: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Comparación de cookies

**Objetivo:** Verificar la rotación sin compartir IDs en el informe.

```http
GET /login HTTP/1.1
Host: {ORIGEN}

# Registrar Set-Cookie anónimo; iniciar sesión y comparar Set-Cookie posterior.
```

**Interpretación:** Los valores deben ser distintos y el anterior no debe acceder a `/api/me`.

### 2. Sesión anterior

**Objetivo:** Reutilizar la cookie anónima tras login propio.

```http
GET /api/me HTTP/1.1
Host: {ORIGEN}
Cookie: session={COOKIE_ANONIMA_ANTERIOR}
```

**Interpretación:** Si obtiene datos privados, confirmar que no es una sesión diferente creada accidentalmente.

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../../README.md)
