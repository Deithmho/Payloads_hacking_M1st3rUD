# 🤝 Cómo contribuir

Este repositorio es una guía de trabajo autorizada. Una contribución útil explica una condición técnica verificable, una prueba mínima y sus límites.

## Estructura de cada tema

```text
Categoria/Tema/
├── Descripcion/
│   └── README.md
└── Payloads_hack/
    └── README.md
```

Mantener **exactamente esas dos subcarpetas**. El índice principal debe enlazar ambas. Para añadir un tema, editar `tools/catalogo.py`, ejecutar `python3 tools/generar_catalogo.py` y luego `python3 tools/validar_catalogo.py`.

## Criterios de aceptación

- Explicar origen de la entrada, sink, límite de confianza, variantes, condiciones de explotación y corrección.
- Indicar qué resultado **sí** confirma el fallo y qué resultado todavía es ambiguo.
- Ofrecer una prueba de control y un payload de bajo impacto con marcadores, no con secretos ni dominios de terceros.
- Vincular fuente primaria o investigación técnica. Si se usa un relato secundario, describir su grado de verificación.
- Distinguir severidad demostrada de severidad hipotética y no asignar CVSS numérico sin un caso concreto.
- Mantener español profesional, Markdown legible y bloques de código con lenguaje.

## Datos y pruebas

Usar cuentas y objetos propios. Redactar tokens, cookies, correos e identificadores de terceros. No incluir volcados, credenciales, payloads destructivos ni pruebas de carga contra sistemas compartidos. La autorización y las reglas del programa determinan qué se puede probar.

---

[← Índice general](README.md)
