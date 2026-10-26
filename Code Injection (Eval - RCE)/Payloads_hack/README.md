# 🗡️ Code injection / eval: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Aritmética común

**Objetivo:** En un campo de fórmula que pueda llegar a eval; línea base sin efecto.

```text
7*7
```

**Interpretación:** 49 por sí solo puede ser una calculadora legítima: comparar funciones fuera del lenguaje permitido.

**Fuente técnica:** [documentación de la técnica](https://community.owasp.org/attacks/Code_Injection).

### 2. Python eval: tipo y operación

**Objetivo:** Solo cuando la implementación usa evaluación Python; expresión sin llamadas peligrosas.

```python
str(7*7)
```

**Interpretación:** El resultado texto 49 y un error Python en control negativo pueden confirmar evaluación Python.

**Fuente técnica:** [documentación de la técnica](https://community.owasp.org/attacks/Code_Injection).

### 3. Python eval: literal compuesto

**Objetivo:** Comprobar capacidad de construir datos fuera del contrato de una fórmula simple.

```python
{'marca':'prueba-123'}['marca']
```

**Interpretación:** Una salida prueba-123 demuestra acceso al intérprete, pero no privilegios de sistema.

**Fuente técnica:** [documentación de la técnica](https://community.owasp.org/attacks/Code_Injection).

### 4. PHP eval: función inofensiva

**Objetivo:** Solo para un sink PHP que acepta expresiones de PHP.

```php
strtoupper('prueba-123')
```

**Interpretación:** PRUEBA-123 en la respuesta con control literal apoya evaluación de código PHP.

**Fuente técnica:** [documentación de la técnica](https://community.owasp.org/attacks/Code_Injection).

### 5. JavaScript servidor: Math.max

**Objetivo:** Node.js eval o función dinámica en backend; no confundir con código ejecutado en navegador.

```js
Math.max(7, 49)
```

**Interpretación:** Confirmar 49 en respuesta cruda o efecto servidor, no en DevTools del cliente.

**Fuente técnica:** [documentación de la técnica](https://community.owasp.org/attacks/Code_Injection).

### 6. Ruby eval: transformación

**Objetivo:** Solo si el backend interpreta Ruby dinámico.

```ruby
'prueba-123'.upcase
```

**Interpretación:** La transformación debe originarse en servidor y no en una plantilla frontend.

**Fuente técnica:** [documentación de la técnica](https://community.owasp.org/attacks/Code_Injection).

### 7. Ciego Python con pausa corta

**Objetivo:** Laboratorio o ventana autorizada, cuando no se devuelve salida.

```python
__import__('time').sleep(1)
```

**Interpretación:** Comparar tiempos de control; la pausa prueba capacidad de llamada si es repetible, no demuestra acceso a shell.

**Fuente técnica:** [documentación de la técnica](https://community.owasp.org/attacks/Code_Injection).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
