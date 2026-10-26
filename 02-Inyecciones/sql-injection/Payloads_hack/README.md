# 🗡️ SQL injection: payloads y técnicas

> **Uso autorizado:** sustituir `{ORIGEN}`, `{TOKEN_A}`, `{ID_PROPIO}` y `{ID_CONTROLADO_B}` por valores del entorno y de cuentas propias. No ejecutar muestras que cambien estado sin permiso específico y plan de reversión.

## 🎯 Preparación

- Capturar primero la solicitud legítima y su respuesta esperada.
- Mantener igual método, sesión, cabeceras y cuerpo salvo el campo bajo prueba.
- Usar un marcador único como `prueba-123` para distinguir reflejos y efectos de caché.

## 🔬 Pruebas por escenario

### 1. Booleano verdadero/falso

**Objetivo:** Comparar dos condiciones sin extraer datos.

```http
GET /api/items?name=prueba%27%20AND%201%3D1--%20 HTTP/1.1
Host: {ORIGEN}

# Control: name=prueba%27%20AND%201%3D2--%20
```

**Interpretación:** Una diferencia repetible sugiere inyección; contrastar con sintaxis y caché.

### 2. Retardo corto en PostgreSQL

**Objetivo:** Medir una condición temporal solo si el programa permite pruebas de tiempo.

```sql
' AND (SELECT 1 FROM pg_sleep(1))=1--
```

**Interpretación:** Repetir con control sin `pg_sleep`; la latencia de red por sí sola no confirma SQLi.

### 3. OAST Oracle

**Objetivo:** Consultar DNS sin incluir datos; requiere privilegio UTL_INADDR y entorno de laboratorio.

```sql
SELECT UTL_INADDR.get_host_address('prueba-123.{CONTROLLED_HOST}') FROM dual;
```

**Interpretación:** La consulta DNS debe correlacionarse; puede fallar por ACL o privilegios, lo que no descarta SQLi.

## ✅ Evidencia mínima

1. Solicitud de control y solicitud modificada, con diferencias visibles.
2. Respuesta o efecto observado en una cuenta/objeto de prueba independiente.
3. Explicación del control que falló y del alcance real comprobado.

---

[📖 Descripción y análisis](../Descripcion/README.md) · [← Índice general](../../../README.md)
