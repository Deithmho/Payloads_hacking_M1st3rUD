# 🤝 Cómo contribuir

Este repositorio es una guía de trabajo autorizada. Una contribución útil explica una condición técnica verificable, una prueba mínima y sus límites.

## Estructura de cada tema

```text
Nombre de la vulnerabilidad/
├── Descripcion/
│   └── README.md
└── Payloads_hack/
    ├── README.md
    ├── Catalogo_PATT.md
    ├── PATT_*.md
    ├── PATT_LISTA_*.txt
    └── Ampliacion_original.md (cuando corresponda)
```

Mantener **exactamente esas dos subcarpetas**. El índice principal debe enlazar ambas. Para añadir un tema, editar `tools/catalogo.py`, `tools/payloads_*.py` y `tools/bancos_*.py` de su área. Si incorpora documentos de PayloadsAllTheThings, actualizar `tools/patt_mapa.py` y regenerar con `tools/importar_patt.py` usando la revisión fija. Ejecutar `python3 tools/generar_catalogo.py` y luego `python3 tools/validar_catalogo.py`.

## Criterios de aceptación

- Explicar origen de la entrada, sink, límite de confianza, variantes, condiciones de explotación y corrección.
- Indicar qué resultado **sí** confirma el fallo y qué resultado todavía es ambiguo.
- Mantener al menos seis escenarios técnicamente distintos por tema, cada uno con objetivo, ejemplo, interpretación y fuente.
- Añadir al menos cuatro bloques de banco por tema, repartidos entre **básicos**, **por contexto** y **avanzados**; las listas deben contener alternativas reales y advertir sus precondiciones.
- Ofrecer primero pruebas de control y payloads de bajo impacto con marcadores. Señalar las precondiciones de ejemplos avanzados antes de su uso.
- Vincular fuente primaria o investigación técnica. Si se usa un relato secundario, describir su grado de verificación.
- Distinguir severidad demostrada de severidad hipotética y no asignar CVSS numérico sin un caso concreto.
- Mantener español profesional, Markdown legible y bloques de código con lenguaje.

## Datos y pruebas

Usar cuentas y objetos propios. Redactar tokens, cookies, correos e identificadores de terceros. No incorporar volcados ni credenciales. Los anexos de terceros son material de referencia bajo la [licencia MIT de PATT](LICENCIA_PATT.md): no ejecutar automáticamente diccionarios completos, payloads de alteración de estado o pruebas de carga contra sistemas compartidos. La autorización y las reglas del programa determinan qué se puede probar.

---

[← Índice general](README.md)
