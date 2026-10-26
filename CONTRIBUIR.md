# 🤝 Cómo contribuir

Este repositorio es una guía de trabajo autorizada. Una contribución útil explica una condición técnica verificable, una prueba mínima y sus límites.

## Estructura de cada tema

```text
Nombre de la vulnerabilidad/
├── Descripcion/
│   └── README.md
└── Payloads_hack/
    └── README.md
```

Mantener **exactamente esas dos subcarpetas**. El índice principal debe enlazar ambas. Para añadir un tema, editar `tools/catalogo.py`, `tools/payloads_*.py` y `tools/bancos_*.py` de su área; ejecutar `python3 tools/generar_catalogo.py` y luego `python3 tools/validar_catalogo.py`.

## Criterios de aceptación

- Explicar origen de la entrada, sink, límite de confianza, variantes, condiciones de explotación y corrección.
- Indicar qué resultado **sí** confirma el fallo y qué resultado todavía es ambiguo.
- Mantener al menos seis escenarios técnicamente distintos por tema, cada uno con objetivo, ejemplo, interpretación y fuente.
- Añadir al menos cuatro bloques de banco por tema, repartidos entre **básicos**, **por contexto** y **avanzados**; las listas deben contener alternativas reales y advertir sus precondiciones.
- Ofrecer pruebas de control y payloads de bajo impacto con marcadores, no con secretos ni dominios de terceros.
- Vincular fuente primaria o investigación técnica. Si se usa un relato secundario, describir su grado de verificación.
- Distinguir severidad demostrada de severidad hipotética y no asignar CVSS numérico sin un caso concreto.
- Mantener español profesional, Markdown legible y bloques de código con lenguaje.

## Datos y pruebas

Usar cuentas y objetos propios. Redactar tokens, cookies, correos e identificadores de terceros. No incluir volcados, credenciales, payloads destructivos ni pruebas de carga contra sistemas compartidos. La autorización y las reglas del programa determinan qué se puede probar.

---

[← Índice general](README.md)
