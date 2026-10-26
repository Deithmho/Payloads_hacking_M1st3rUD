# 🗡️ Inyección de comandos del sistema: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Separador POSIX ;

**Objetivo:** Valor insertado en línea de shell POSIX, fuera de comillas; emitir marcador sin tocar archivos.

```text
127.0.0.1; printf prueba-123
```

**Interpretación:** Comprobar salida del proceso, no simple eco del parámetro.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Command%20Injection/README.md).

### 2. AND condicional

**Objetivo:** El comando anterior debe terminar con éxito.

```text
127.0.0.1 && printf prueba-123
```

**Interpretación:** La ausencia de marcador puede deberse a fallo del comando inicial; comparar con ;.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Command%20Injection/README.md).

### 3. Sustitución POSIX $()

**Objetivo:** Útil si el dato queda dentro de otra palabra o argumento con expansión de shell.

```text
127.0.0.1$(printf prueba-123)
```

**Interpretación:** Verificar si el marcador modifica salida o argumento; el texto reflejado sin evaluación no basta.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Command%20Injection/README.md).

### 4. Backticks POSIX

**Objetivo:** Variante de sustitución en shells que la admiten.

```text
127.0.0.1`printf prueba-123`
```

**Interpretación:** Comparar con backticks escapados; el proceso de destino debe ejecutar un shell.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Command%20Injection/README.md).

### 5. Salto de línea

**Objetivo:** Cuando se bloquea ; pero el shell interpreta LF; usar un único comando inerte.

```text
127.0.0.1%0Aprintf%20prueba-123
```

**Interpretación:** La aplicación debe decodificar %0A antes de invocar shell; probar también control %250A.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Command%20Injection/README.md).

### 6. Separador Windows cmd.exe

**Objetivo:** Solo si el backend usa cmd.exe; & ejecuta el siguiente comando.

```text
127.0.0.1 & echo prueba-123
```

**Interpretación:** Confirmar con control que el marcador sale del proceso Windows.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Command%20Injection/README.md).

### 7. Ciego por tiempo

**Objetivo:** Solo en laboratorio o ventana pactada; pausa de un segundo.

```text
127.0.0.1; sleep 1
```

**Interpretación:** Comparar medianas con 127.0.0.1 sin pausa; el retardo por red no demuestra ejecución.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Command%20Injection/README.md).

### 8. OAST DNS sin datos

**Objetivo:** Laboratorio o permiso expreso; host controlado y marcador único.

```text
127.0.0.1; nslookup prueba-123.{CONTROLLED_HOST}
```

**Interpretación:** Una consulta DNS correlacionada prueba ejecución de comando o de otra capa; revisar origen y logs.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Command%20Injection/README.md).

### 9. Pipe POSIX

**Objetivo:** Enviar la salida de la orden inicial a printf; requiere shell POSIX.

```text
127.0.0.1 | printf prueba-123
```

**Interpretación:** El marcador debe provenir del proceso servidor y desaparecer con pipe escapado.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Command%20Injection/README.md).

### 10. Separación con IFS

**Objetivo:** Solo para shell compatible cuando el filtro bloquea espacios y ya existe indicio de inyección.

```text
127.0.0.1;printf${IFS}prueba-123
```

**Interpretación:** `${IFS}` debe expandirse en shell; si se refleja literalmente, no hay evaluación.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Command%20Injection/README.md).

### 11. PowerShell en Windows

**Objetivo:** Solo si se sabe que el backend invoca PowerShell y no cmd.exe.

```text
127.0.0.1; Write-Output prueba-123
```

**Interpretación:** El separador ; y Write-Output son de PowerShell; confirmar proceso y salida.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Command%20Injection/README.md).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
