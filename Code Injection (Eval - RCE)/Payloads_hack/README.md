# 🗡️ Code injection / eval: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

> **Lectura del banco:** cuando un bloque enumera varias URL, rutas, cabeceras o cuerpos, cada línea suele ser una alternativa. Elegir la variante que corresponde al motor, parser y flujo real.

## 💉 Payloads básicos

### Aritmética sin efectos

```text
7*7
(2+3)*4
7+7
prueba-123
```

**Cuándo usarlo:** Una línea por solicitud a campo de expresión. Contrastar evaluación con reflejo y cálculo funcional previsto; 49 por sí solo no implica RCE.

**Fuente:** [OWASP WSTG](https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/07-Input_Validation_Testing/11-Testing_for_Code_Injection/).


### Controles por tipo de entrada

```jsonl
{"formula":"7*7"}
{"formula":"(2+3)*4"}
{"formula":"prueba-123"}
```

**Cuándo usarlo:** Una línea JSON por request. Aplicar solo si la API anuncia fórmulas o reglas; un parser matemático restringido puede evaluar sin code injection.

**Fuente:** [OWASP WSTG](https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/07-Input_Validation_Testing/11-Testing_for_Code_Injection/).


## 🧭 Payloads por contexto

### JavaScript/Node.js: capacidad de expresión

```javascript
Math.max(2,3)
"prueba-" + "123"
typeof process
```

**Cuándo usarlo:** Cada línea se evalúa por separado en laboratorio. typeof process distingue entorno Node, pero su presencia no demuestra acceso a archivos o ejecución de comandos.

**Fuente:** [OWASP WSTG](https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/07-Input_Validation_Testing/11-Testing_for_Code_Injection/).


### Python: expresión frente a sentencia

```python
sum([2,3])
"prueba-" + "123"
1 if True else 0
```

**Cuándo usarlo:** Para eval de Python; exec acepta también sentencias. Funciones pueden estar restringidas y una fórmula legítima no es vulnerabilidad por sí sola.

**Fuente:** [OWASP WSTG](https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/07-Input_Validation_Testing/11-Testing_for_Code_Injection/).


## 🔥 Payloads avanzados

### PHP eval con salida inocua

```php
echo 7*7;
print('prueba-123');
```

**Cuándo usarlo:** Una sentencia por prueba en un laboratorio PHP donde la entrada llegue a eval. Confirmar que la salida proviene del servidor, no del navegador.

**Fuente:** [OWASP WSTG](https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/07-Input_Validation_Testing/11-Testing_for_Code_Injection/).


### Disponibilidad de funciones sin invocarlas

```text
typeof require
typeof process
callable(__import__)
'eval' in globals()
```

**Cuándo usarlo:** Las dos primeras son JavaScript/Node; las dos últimas Python. Solo sondas de capacidad en entorno aislado: no importan módulos ni leen datos.

**Fuente:** [OWASP WSTG](https://wstg.owasp.org/stable/4-Web_Application_Security_Testing/07-Input_Validation_Testing/11-Testing_for_Code_Injection/).


## 🔬 Pruebas guiadas por escenario

### 1. Aritmética común

**Objetivo:** En un campo de fórmula que pueda llegar a eval; línea base sin efecto.

```text
7*7
```

**Interpretación:** 49 por sí solo puede ser una calculadora legítima: comparar funciones fuera del lenguaje permitido.

**Fuente técnica:** [OWASP](https://community.owasp.org/attacks/Code_Injection).

### 2. Python eval: tipo y operación

**Objetivo:** Solo cuando la implementación usa evaluación Python; expresión sin llamadas peligrosas.

```python
str(7*7)
```

**Interpretación:** El resultado texto 49 y un error Python en control negativo pueden confirmar evaluación Python.

**Fuente técnica:** [OWASP](https://community.owasp.org/attacks/Code_Injection).

### 3. Python eval: literal compuesto

**Objetivo:** Comprobar capacidad de construir datos fuera del contrato de una fórmula simple.

```python
{'marca':'prueba-123'}['marca']
```

**Interpretación:** Una salida prueba-123 demuestra acceso al intérprete, pero no privilegios de sistema.

**Fuente técnica:** [OWASP](https://community.owasp.org/attacks/Code_Injection).

### 4. PHP eval: función inofensiva

**Objetivo:** Solo para un sink PHP que acepta expresiones de PHP.

```php
strtoupper('prueba-123')
```

**Interpretación:** PRUEBA-123 en la respuesta con control literal apoya evaluación de código PHP.

**Fuente técnica:** [OWASP](https://community.owasp.org/attacks/Code_Injection).

### 5. JavaScript servidor: Math.max

**Objetivo:** Node.js eval o función dinámica en backend; no confundir con código ejecutado en navegador.

```js
Math.max(7, 49)
```

**Interpretación:** Confirmar 49 en respuesta cruda o efecto servidor, no en DevTools del cliente.

**Fuente técnica:** [OWASP](https://community.owasp.org/attacks/Code_Injection).

### 6. Ruby eval: transformación

**Objetivo:** Solo si el backend interpreta Ruby dinámico.

```ruby
'prueba-123'.upcase
```

**Interpretación:** La transformación debe originarse en servidor y no en una plantilla frontend.

**Fuente técnica:** [OWASP](https://community.owasp.org/attacks/Code_Injection).

### 7. Ciego Python con pausa corta

**Objetivo:** Laboratorio o ventana autorizada, cuando no se devuelve salida.

```python
__import__('time').sleep(1)
```

**Interpretación:** Comparar tiempos de control; la pausa prueba capacidad de llamada si es repetible, no demuestra acceso a shell.

**Fuente técnica:** [OWASP](https://community.owasp.org/attacks/Code_Injection).

### 8. PHP eval en contexto de sentencia

**Objetivo:** Solo si el valor se concatena en `eval("$x = ENTRADA;")`; canary sin funciones de sistema.

```php
1; echo 'prueba-123';
```

**Interpretación:** La salida del marcador muestra que se añadieron sentencias, no solo que se evaluó una fórmula.

**Fuente técnica:** [OWASP](https://community.owasp.org/attacks/Code_Injection).

### 9. Python exec frente a eval

**Objetivo:** Laboratorio donde el servidor ejecuta un bloque de sentencias y captura stdout.

```python
marca = "prueba-123"
print(marca)
```

**Interpretación:** La asignación no es expresión válida para eval(); verla ejecutada distingue un sink exec o equivalente.

**Fuente técnica:** [docs.python.org](https://docs.python.org/3/library/functions.html#exec).

### 10. Node.js Function constructor

**Objetivo:** Solo si un servicio Node crea una función desde el cuerpo suministrado por el usuario.

```js
return Math.max(7,49);
```

**Interpretación:** `return` a nivel superior es válido en el cuerpo de Function y no en un script eval; observar 49 en respuesta servidor.

**Fuente técnica:** [developer.mozilla.org](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function/Function).

### 11. Spring Expression Language

**Objetivo:** Se conoce un sink `parseExpression` de SpEL que acepta una expresión completa.

```spel
T(java.lang.Math).max(7,49)
```

**Interpretación:** 49 prueba invocación estática inocua en SpEL; un simple cálculo esperado por contrato no implica vulnerabilidad.

**Fuente técnica:** [docs.spring.io](https://docs.spring.io/spring-framework/reference/core/expressions/language-ref/types.html).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
