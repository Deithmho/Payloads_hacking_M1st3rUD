# 🗡️ LDAP injection: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Comodín frente a asterisco escapado

**Objetivo:** En una búsqueda de una entrada propia, comparar wildcard y literal según RFC 4515.

```text
prueba*
prueba\2a
```

**Interpretación:** El primero puede ser búsqueda legítima. Es inyección si el contrato exigía una cadena literal y el filtro cambia.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/LDAP%20Injection/README.md).

### 2. Cierre de filtro y OR

**Objetivo:** Solo en un login LDAP de laboratorio que interpola uid antes de userPassword; usar identidades de prueba.

```text
*)(uid=*))(|(uid=*
```

**Interpretación:** El payload depende de paréntesis de la consulta original; comprobar filtro final antes de reportar bypass.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/LDAP%20Injection/README.md).

### 3. Condición falsa de control

**Objetivo:** Par de comparación para una condición sobre atributo de prueba.

```text
*)(mail=prueba-123@example.test
*)(mail=ausente-123@example.test
```

**Interpretación:** Una diferencia estable apoya que el filtro incorporó la condición; evita enumerar atributos ajenos.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/LDAP%20Injection/README.md).

### 4. Filtro por objectClass

**Objetivo:** Probar si un cierre permite insertar otro atributo conocido.

```text
*)(objectClass=person
```

**Interpretación:** Comparar con atributo improbable; puede fallar por sintaxis o por esquema, no necesariamente por sanitización.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/LDAP%20Injection/README.md).

### 5. Operador NOT de filtro LDAP

**Objetivo:** Solo si el campo permite un filtro completo o el cierre queda balanceado.

```text
(!(uid=prueba-ausente))
```

**Interpretación:** Una inversión de resultados en datos propios muestra interpretación de sintaxis; validar contexto exacto.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/LDAP%20Injection/README.md).

### 6. Atributo mail con wildcard

**Objetivo:** En un buscador de directorio propio, probar expansión controlada.

```text
prueba*)(mail=*@example.test
```

**Interpretación:** El efecto depende de la plantilla LDAP original y de si el servidor permite el atributo.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/LDAP%20Injection/README.md).

### 7. NUL codificado

**Objetivo:** Solo laboratorio legacy donde se sospeche truncamiento entre componentes.

```text
prueba%00resto
```

**Interpretación:** Modernas bibliotecas suelen rechazar NUL; un error no es vulnerabilidad y no debe asumirse bypass.

**Fuente técnica:** [documentación de la técnica](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/LDAP%20Injection/README.md).

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../README.md)
