# 🗡️ Tabnabbing y engaño de pestañas: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Enlace target blank

**Objetivo:** Localizar enlaces externos que abren otra pestaña.

```html
<a href="https://{DESTINO_PROPIO}/canary" target="_blank">Abrir prueba</a>
```

**Interpretación:** Los navegadores modernos suelen aplicar noopener implícito; comprobar opener en el navegador real.

**Fuente técnica:** [documentación de la técnica](https://community.owasp.org/attacks/Reverse_Tabnabbing).

### 2. Rel explícito

**Objetivo:** Comparar comportamiento con la protección declarada.

```html
<a href="https://{DESTINO_PROPIO}/canary" target="_blank" rel="noopener noreferrer">Abrir prueba</a>
```

**Interpretación:** Este es control negativo: la nueva pestaña no debería tener acceso a window.opener.

**Fuente técnica:** [documentación de la técnica](https://community.owasp.org/attacks/Reverse_Tabnabbing).

### 3. Comprobación de opener

**Objetivo:** Medir si la pestaña nueva conserva la referencia.

```javascript
console.log(window.opener === null ? "sin-opener" : "con-opener");
```

**Interpretación:** Una referencia existente requiere además navegación posible y un flujo de usuario relevante.

**Fuente técnica:** [documentación de la técnica](https://community.owasp.org/attacks/Reverse_Tabnabbing).

### 4. Apertura con window.open

**Objetivo:** Comparar código de apertura programática con enlace HTML.

```javascript
const tab = window.open("https://{DESTINO_PROPIO}/canary", "_blank");
```

**Interpretación:** La política de opener puede diferir entre API y enlace. Usar destino propio.

**Fuente técnica:** [documentación de la técnica](https://community.owasp.org/attacks/Reverse_Tabnabbing).

### 5. Navegación inocua de origen

**Objetivo:** Demostrar capacidad de cambiar la pestaña original sin phishing.

```javascript
if (window.opener) window.opener.location = "https://{DESTINO_PROPIO}/proof/{NONCE}";
```

**Interpretación:** Solo sobre ventana propia de laboratorio. No imitar página de login ni recolectar credenciales.

**Fuente técnica:** [documentación de la técnica](https://community.owasp.org/attacks/Reverse_Tabnabbing).

### 6. Destino redirigido

**Objetivo:** Comprobar si un enlace inicialmente confiable acaba en página controlada.

```text
href=https://{DOMINIO_EN_ALCANCE}/redirect?to=https://{DESTINO_PROPIO}/canary
target=_blank
```

**Interpretación:** Verificar el destino final y opener en el navegador; la redirección por sí sola no prueba tabnabbing.

**Fuente técnica:** [documentación de la técnica](https://community.owasp.org/attacks/Reverse_Tabnabbing).

### 7. Atributo opener explícito

**Objetivo:** Confirmar el efecto de rel=opener en un laboratorio.

```html
<a href="https://{DESTINO_PROPIO}/canary" target="_blank" rel="opener">Prueba local</a>
```

**Interpretación:** Solo útil si la aplicación coloca rel=opener; no extrapolar a enlaces target blank sin ese atributo.

**Fuente técnica:** [documentación de la técnica](https://community.owasp.org/attacks/Reverse_Tabnabbing).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
