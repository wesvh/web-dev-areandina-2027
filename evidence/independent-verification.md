# Verificación independiente — Entrega 2

Fecha: 25 de octubre de 2026. Candidato de ejecución: `cfe938d25c1809fe4c7e2f85c454d1359f4a2218`.

## Resultado local

**PASS sin bloqueos reproducibles**, limitado a implementación local. Un verificador independiente extrajo el candidato en una carpeta temporal y utilizó un proyecto Docker, puerto y volumen MySQL separados. No modificó el repositorio ni la base de datos principal.

- Arranque desde cero mediante `./start.sh`: aplicación saludable.
- `docker compose exec -T web python manage.py test --noinput`: **23 de 23 pruebas aprobadas** contra MySQL real.
- `python manage.py check`: sin problemas; `makemigrations --check --dry-run`: sin cambios pendientes.
- Registro sin privilegios, contraseñas cifradas mediante hash, restricciones de administrador y redirecciones seguras: aprobados.
- Registro, inicio y cierre de sesión sin token CSRF: HTTP 403. Cierre de sesión mediante GET: HTTP 405.
- Catálogo público, CSS y CSS de Admin: HTTP 200. Las votaciones en borrador no se exponen por identificador.
- Reinicio después de detener web: conservó registros, edición modificada y hash de contraseña del administrador; el hash no se incluye en esta evidencia.
- Contenedor web sin privilegios de root, DEBUG desactivado, MySQL sin puerto publicado y web restringido a localhost.
- `.env` generado con modo 600, excluido del código versionado y de la imagen; contraseña root de MySQL ausente del entorno web.
- PDF: 11 páginas tamaño Carta, autor y docente correctos, campos pendientes identificados. La inspección visual fue realizada por el autor de la entrega, no por el verificador independiente.

El autor repitió `check` en el sistema principal: sin problemas. Comparó sus registros con `evidence/restart.json`: 2 ediciones, 3 categorías, 4 votaciones y 4 opciones; categoría de evidencia ID 3 conservada. El volumen principal no se eliminó. Los contenedores, red y volumen del verificador se eliminaron separadamente.

## Límites y pendientes

- GitHub privado en `wesvh/festival-vallenato-2027`: destino autorizado, **todavía no publicado**. Falta autenticar la cuenta personal; no se utilizó la cuenta corporativa disponible.
- Falta nombre del programa académico y enlace real del video.
- Permisos del docente y apertura del repositorio desde otra sesión: pendientes después de publicar.
- Entrega individual por solicitud expresa; la rúbrica exige cuatro integrantes y el criterio de equipo vale 5 puntos de 20.
- No se afirma RED/GREEN inicial: el runner Docker no existía cuando se escribió el primer código. Se registran únicamente resultados efectivamente observados.
- RDD está desactivado. La evaluación de riesgo fue alta por autenticación y entorno Docker; la verificación funcional independiente no constituye un recibo nativo de revisión.
- Engram rechazó el proyecto detectado; seguimiento y evidencia se conservan localmente.

Risk: items 2 (authentication and administrator privileges) and 5 (Docker execution, dependencies and automatic initialization).
