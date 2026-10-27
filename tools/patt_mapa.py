"""Correspondencia editorial entre las 61 guías y documentos de PATT.

Cada ruta se conserva con el nombre original para poder comprobar el origen.
Una misma fuente puede servir a varias guías cuando el contexto cambia.
"""

MAPA = {
    # Autenticación y sesión
    'autenticacion-rota': ['Account Takeover/README.md', 'Insecure Randomness/README.md', 'Type Juggling/README.md'],
    'jwt': ['JSON Web Token/README.md'],
    'oauth': ['OAuth Misconfiguration/README.md'],
    'saml': ['SAML Injection/README.md'],
    'fijacion-sesion': ['CRLF Injection/README.md'],
    'reset-password-poisoning': ['Account Takeover/README.md'],
    'mfa-bypass': ['Account Takeover/mfa-bypass.md'],
    'idor': ['Insecure Direct Object References/README.md'],
    'control-acceso': ['Insecure Direct Object References/README.md'],
    'mass-assignment': ['Mass Assignment/README.md', 'External Variable Modification/README.md'],

    # Inyecciones
    'sql-injection': [
        'SQL Injection/README.md', 'SQL Injection/MySQL Injection.md',
        'SQL Injection/PostgreSQL Injection.md', 'SQL Injection/MSSQL Injection.md',
        'SQL Injection/SQLite Injection.md', 'SQL Injection/OracleSQL Injection.md',
        'SQL Injection/DB2 Injection.md', 'SQL Injection/BigQuery Injection.md',
        'SQL Injection/Cassandra Injection.md', 'SQL Injection/SQLmap.md',
    ],
    'nosql-injection': ['NoSQL Injection/README.md'],
    'command-injection': ['Command Injection/README.md'],
    'xxe': ['XXE Injection/README.md'],
    'ssti': [
        'Server Side Template Injection/README.md',
        'Server Side Template Injection/Python.md',
        'Server Side Template Injection/JavaScript.md',
        'Server Side Template Injection/PHP.md',
        'Server Side Template Injection/Java.md',
        'Server Side Template Injection/Ruby.md',
        'Server Side Template Injection/ASP.md',
        'Server Side Template Injection/Elixir.md',
    ],
    'ldap-injection': ['LDAP Injection/README.md'],
    'crlf-injection': ['CRLF Injection/README.md'],
    'header-injection': ['CRLF Injection/README.md'],
    'host-header-injection': ['Account Takeover/README.md', 'Web Cache Deception/README.md'],
    'email-header-injection': ['CRLF Injection/README.md'],
    'xpath-injection': ['XPATH Injection/README.md'],
    'code-injection': [
        'Command Injection/README.md', 'Server Side Include Injection/README.md',
        'XSLT Injection/README.md', 'LaTeX Injection/README.md',
        'CSV Injection/README.md',
    ],

    # Navegador y cliente
    'xss': [
        'XSS Injection/README.md', 'XSS Injection/1 - XSS Filter Bypass.md',
        'XSS Injection/2 - XSS Polyglot.md',
        'XSS Injection/3 - XSS Common WAF Bypass.md',
        'XSS Injection/4 - CSP Bypass.md',
        'XSS Injection/5 - XSS in Angular.md',
        'CSS Injection/README.md', 'XS-Leak/README.md',
    ],
    'csrf': ['Cross-Site Request Forgery/README.md', 'Client Side Path Traversal/README.md'],
    'clickjacking': ['Clickjacking/README.md'],
    'cors': ['CORS Misconfiguration/README.md'],
    'prototype-pollution': ['Prototype Pollution/README.md'],
    'open-redirect': ['Open Redirect/README.md'],
    'websocket-hijacking': ['Web Sockets/README.md'],
    'postmessage': ['XSS Injection/README.md'],
    'dom-clobbering': ['DOM Clobbering/README.md'],

    # Servidor y lógica
    'ssrf': [
        'Server Side Request Forgery/README.md',
        'Server Side Request Forgery/SSRF-Advanced-Exploitation.md',
        'Server Side Request Forgery/SSRF-Cloud-Instances.md',
        'Headless Browser/README.md',
    ],
    'deserializacion': [
        'Insecure Deserialization/README.md', 'Insecure Deserialization/Java.md',
        'Insecure Deserialization/PHP.md', 'Insecure Deserialization/Python.md',
        'Insecure Deserialization/Node.md', 'Insecure Deserialization/DotNET.md',
        'Insecure Deserialization/Ruby.md',
    ],
    'race-condition': ['Race Condition/README.md'],
    'business-logic': ['Business Logic Errors/README.md', 'Type Juggling/README.md'],
    'rate-limit-bypass': ['Brute Force Rate Limit/README.md'],
    'path-traversal-lfi': [
        'Directory Traversal/README.md', 'File Inclusion/README.md',
        'File Inclusion/Wrappers.md', 'File Inclusion/LFI-to-RCE.md',
    ],
    'rfi': ['File Inclusion/README.md', 'File Inclusion/Wrappers.md'],
    'file-upload': ['Upload Insecure Files/README.md', 'Upload Insecure Files/Configuration Apache .htaccess/README.md'],
    'request-smuggling': ['Request Smuggling/README.md'],
    'http-parameter-pollution': ['HTTP Parameter Pollution/README.md'],
    'web-cache-poisoning': ['Web Cache Deception/README.md'],
    'web-cache-deception': ['Web Cache Deception/README.md'],

    # API
    'graphql': ['GraphQL Injection/README.md'],
    'api-key-leakage': ['API Key Leaks/README.md', 'API Key Leaks/IIS-Machine-Keys.md'],
    'bola': ['Insecure Direct Object References/README.md'],
    'bfla': [],  # No hay guía PATT de autorización por función.
    'excessive-data-exposure': ['ORM Leak/README.md', 'Hidden Parameters/README.md'],
    'resource-limits': ['Brute Force Rate Limit/README.md', 'Denial of Service/README.md', 'Regular Expression/README.md'],
    'api-mass-assignment': ['Mass Assignment/README.md', 'External Variable Modification/README.md'],
    'webhook-ssrf': ['Server Side Request Forgery/README.md', 'Server Side Request Forgery/SSRF-Advanced-Exploitation.md'],
    'web-llm-prompt-injection': ['Prompt Injection/README.md'],

    # Infraestructura y misceláneos
    'subdomain-takeover': [],  # PATT no contiene una guía propia sobre takeover.
    'dns-rebinding': ['DNS Rebinding/README.md'],
    'tabnabbing': ['Tabnabbing/README.md'],
    'information-disclosure': [
        'API Key Leaks/README.md', 'Insecure Source Code Management/README.md',
        'Insecure Source Code Management/Git.md',
        'Insecure Source Code Management/Subversion.md',
        'Insecure Source Code Management/Mercurial.md',
        'Insecure Source Code Management/Bazaar.md',
        'Insecure Management Interface/README.md', 'Virtual Hosts/README.md',
    ],
    'security-misconfiguration': ['Reverse Proxy Misconfigurations/README.md', 'Clickjacking/README.md'],
    'cloud-metadata-ssrf': ['Server Side Request Forgery/SSRF-Cloud-Instances.md'],
    'zip-slip': ['Zip Slip/README.md'],
    'cors-credenciales': ['CORS Misconfiguration/README.md'],
    'clickjacking-framing': ['Clickjacking/README.md'],
}
