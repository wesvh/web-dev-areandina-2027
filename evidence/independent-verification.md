# Verificación independiente — Entrega 2

Fecha: 25 de octubre de 2026. Candidato de ejecución: `cfe938d25c1809fe4c7e2f85c454d1359f4a2218`.

## Resultado local

**PASS sin bloqueos reproducibles**, limitado a implementación local. Un verificador independiente extrajo el candidato en una carpeta temporal y utilizó un proyecto Docker, puerto y volumen MySQL separados. No modificó el repositorio ni la base de datos principal.

- Arranque desde cero mediante `./start.sh`: aplicación saludable.
- `docker compose exec -T web python manage.py test --noinput`: **23 de 23 pruebas aprobadas** contra MySQL real.
- `python manage.py check`: sin problemas; `makemigrations --check --dry-run`: sin cambios pendientes.
- Registro sin privilegios, contraseñas almacenadas mediante hash, restricciones de administrador y redirecciones seguras: aprobados.
- Registro, inicio y cierre de sesión sin token CSRF: HTTP 403. Cierre de sesión mediante GET: HTTP 405.
- Catálogo público, CSS y CSS de Admin: HTTP 200. Las votaciones en borrador no se exponen por identificador.
- Reinicio después de detener web: conservó registros, edición modificada y hash de contraseña del administrador; el hash no se incluye en esta evidencia.
- Contenedor web sin privilegios de root, DEBUG desactivado, MySQL sin puerto publicado y web restringido a localhost.
- `.env` generado con modo 600, excluido del código versionado y de la imagen; contraseña root de MySQL ausente del entorno web.
- PDF: 11 páginas tamaño Carta, autor y docente correctos, campos pendientes identificados. La inspección visual fue realizada por el autor de la entrega, no por el verificador independiente.

Actualización documental del 26 de octubre: las siete capturas se reemplazaron por vistas reales de escritorio, ventana 1440×900. El PDF mantiene 11 páginas, figuras principalmente completas y un detalle horizontal de cabecera identificado expresamente. La sesión mostrada ahora es `admin_demo`; el formulario administrativo muestra la categoría existente ID 3, no un nuevo guardado. Estas actualizaciones documentales no alteraron código de ejecución ni registros del catálogo y no se presentan como una nueva ejecución de la suite independiente.

El autor repitió `check` en el sistema principal: sin problemas. Comparó sus registros con `evidence/restart.json`: 2 ediciones, 3 categorías, 4 votaciones y 4 opciones; categoría de evidencia ID 3 conservada. El volumen principal no se eliminó. Los contenedores, red y volumen del verificador se eliminaron separadamente.

## Límites y pendientes

- Actualización del 26 de octubre de 2026: el usuario autorizó publicación **pública**, reemplazando su solicitud inicial de privacidad. Código publicado en https://github.com/wesvh/web-dev-areandina-2027, rama `master`, mediante SSH personal `wesvh`. El historial se revisó antes de subirlo: sin coincidencias con secretos locales ni los patrones de credenciales comprobados. Esta revisión no afirma detectar todo secreto posible.
- Falta nombre del programa académico y enlace real del video.
- El repositorio público permite consultar código sin invitación. El acceso y permisos del futuro video siguen pendientes; no se afirma que el docente haya revisado la entrega.
- Entrega individual por solicitud expresa; la rúbrica exige cuatro integrantes y el criterio de equipo vale 5 puntos de 20.
- No se afirma RED/GREEN inicial: el runner Docker no existía cuando se escribió el primer código. Se registran únicamente resultados efectivamente observados.
- RDD está desactivado. La evaluación de riesgo fue alta por autenticación y entorno Docker; la verificación funcional independiente no constituye un recibo nativo de revisión.
- Engram rechazó el proyecto detectado; seguimiento y evidencia se conservan localmente.

Risk: items 2 (authentication and administrator privileges) and 5 (Docker execution, dependencies and automatic initialization).
