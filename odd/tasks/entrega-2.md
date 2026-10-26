# Entrega 2 - Festival Vallenato 2027
Outcome: runnable Django/MySQL application, one-command Docker startup, real screenshot evidence and concise APA report. Branch: `codex/entrega-2`. Delivery: local repository and private `wesvh/festival-vallenato-2027`; no PR requested. Runner: Django tests against MySQL in Docker.
Forecast: about 1,500 authored lines across backend, templates, startup and verification. Engram mirror: pending; provider rejects the detected `universidad` project. Existing Entrega 1 artifacts remain unchanged.

## Specs
### S1 - Execution and private repository
User: "Considera pantallazos del documento, considera tambien ejecutable, github, docker para ejecuciuion, migraciones automaticas, para dejar el sistema a punto con 1 solo comando".
User: "Si, pero el repo privsdo y mi cuenta personal es wesvh".
Acceptance: `./start.sh` initializes ignored local secrets, builds and starts MySQL and Django, applies committed migrations and seeds fictional sample data without manual configuration. Docker with Compose and internet for first image download are prerequisites. Restarts preserve existing records. README explains URLs, credentials location, tests and stopping without deleting volumes. Only the explicitly authorized personal account may publish the private repository.

### S2 - Django and MySQL
Assignment: "Proyecto Django: crear el proyecto, organizar aplicaciones, configurar rutas, vistas y plantillas."
Assignment: "MySQL: configurar la conexión, definir modelos relacionados y ejecutar migraciones."
Assignment: "EDICIÓN   →   CATEGORÍA   →   VOTACIÓN   →   OPCIÓN".
Acceptance: Django MVT, `accounts` and `catalog` apps; real MySQL only, committed migrations, foreign keys, database uniqueness constraints and admin CRUD. Edition(year, name), Category(edition, name, description), Poll(category, title, description, status), Option(poll, name, description). Status values draft/open/closed. No vote records in this phase.

### S3 - Authentication and administration
Assignment: "Autenticación: implementar registro, inicio de sesión y cierre de sesión."
Assignment: "Se permite utilizar Django Admin para administrar ediciones, categorías, votaciones y opciones."
Acceptance: built-in Django User, password validators and hashing; CSRF-protected registration/login and POST logout; safe next redirects. Public registration never grants staff privileges. Admin requires staff permission. Local demo administrator has a generated password absent from repository and report.

### S4 - Public dynamic catalog
Assignment: "Ediciones: registrar y consultar diferentes ediciones anuales del Festival."
Assignment: "Categorías: crear y consultar categorías vinculadas a una edición."
Assignment: "Votaciones y opciones: registrar votaciones asociadas a categorías y administrar opciones participantes."
Assignment: "Interfaz pública: consultar y mostrar datos reales de MySQL mediante vistas y plantillas Django."
Acceptance: responsive Spanish public pages from database queries, edition/category/poll drill-down, option lists, empty and 404 states; no fake live voting. All displayed sample categories/options are explicitly fictional. Changes made in Admin appear in public views.

### S5 - Report and evidence
Assignment: "Capturas de pantalla comentadas: imágenes legibles de Django Admin, datos registrados, interfaces públicas y operaciones; explicar qué demuestra cada captura."
Assignment: "Código relevante: fragmentos necesarios para explicar modelos, vistas, rutas o autenticación; no copiar todo el proyecto."
Assignment: "Pruebas y resultados: funcionalidades probadas, procedimiento y resultados."
Assignment: "Repositorio: enlace directo a GitHub u otra plataforma con código y README de instalación y ejecución."
Assignment: "Video: enlace directo a demostración de la aplicación y participación de los cuatro integrantes."
User correction retained: "Retira los demas integrantes, dejame solo a mi" and professor "DEIVYS MORALES URIBE".
Acceptance: concise Spanish APA PDF with Esteban Villada Henao as sole author, supplied professor, institution, course and date; introduction, architecture/model/migrations/authentication, real annotated screenshots, selected code, observed test results, repository status, conclusions and individual responsibilities. Program name and video URL are not supplied: mark pending, do not fabricate. Explain that the assignment requires four people and individual delivery loses the 5-point teamwork criterion. No submission or invented participation.

### S6 - Safety and bounds
Assignment: "No incluir contraseñas, tokens, claves privadas ni credenciales de MySQL. Utilizar datos de prueba."
Assignment: "PARA ENTREGAS POSTERIORES Registro definitivo de votos, control avanzado de duplicados, reglas completas de elegibilidad, publicación final de resultados, auditoría avanzada, pruebas de carga y despliegue productivo."
Acceptance: secrets ignored by Git and Docker context, database not published to host, application bound to localhost, non-root application user, debug disabled by default, static files served locally. No production deployment or invented verification of inaccessible private links. Video and external-session access checks remain explicitly pending until supplied.

## Tasks
- T1 | S2-S4,S6 | delegated backend unit, parallel with T2; Python project/apps/migrations/tests only | complete: 23 MySQL tests pass | d7cd887
- T2 | S4,S5 | delegated presentation unit, parallel with T1; templates/static only, shared contract below | complete: HTTP and real browser flows pass | afdfc3a
- T3 | S1,S2,S6 | inline Docker, startup, docs and integration | complete: clean startup and stopped-web restart pass without data loss | 1f338f7, caf82e7
- T4 | S1-S6 | inline functional proof, then independent verification for Risk items 2 (authentication) and 5 (container execution); capture evidence and APA report | complete locally: 23/23 tests in both stacks, independent PASS, 11-page PDF visually checked; external report fields remain pending | 0d4f877, cfe938d; final verification record in closing documentation commit
- T5 | S1,S5 | inline private GitHub publication only through wesvh, access readback and delivery package | blocked: personal GitHub session unavailable | commit pending

## Shared implementation contract
- Repository root: `festival-vallenato-2027/`. Config package `config`; apps `accounts`, `catalog`.
- Namespaced routes: `catalog:home` `/`; `catalog:edition` `/editions/<int:pk>/`; `catalog:category` `/categories/<int:pk>/`; `catalog:poll` `/polls/<int:pk>/`; `accounts:register` `/accounts/register/`; `accounts:login` `/accounts/login/`; `accounts:logout` `/accounts/logout/`; Django Admin `/admin/`; `/health/` database-backed JSON.
- Context: home `editions`; edition `edition`, `categories`; category `category`, `polls`; poll `poll`, `options`; forms expose `form`. Related names `categories`, `polls`, `options`. Every template inherits `base.html`.
- Templates: `catalog/home.html`, `catalog/edition_detail.html`, `catalog/category_detail.html`, `catalog/poll_detail.html`, `registration/login.html`, `accounts/register.html`, `404.html`, `500.html`; local `static/css/site.css`.
- Environment: `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`, `MYSQL_DATABASE`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_HOST`, `MYSQL_PORT`, `DEMO_ADMIN_USER`, `DEMO_ADMIN_PASSWORD`. Root MySQL password is never given to web container. Test database `test_festival`, application database/user `festival`.
- Initialization command: `python manage.py seed_demo`, idempotent get-or-create, no reset/overwrite of existing admin password or edited catalog rows. Admin passwords are generated locally, never hardcoded. Public catalog exposes only open/closed polls; draft polls remain in Admin and do not leak by direct ID.
- Dependency direction: templates consume contract, backend does not edit templates; parent owns Docker, dependencies, docs and Git. Workers run no repository-wide generators/formatters, installs or Git mutations.

## Log
- L1, 2026-10-25: "Considera pantallazos del documento, considera tambien ejecutable, github, docker para ejecuciuion, migraciones automaticas, para dejar el sistema a punto con 1 solo comando".
- L2, 2026-10-25: "Si, pero el repo privsdo y mi cuenta personal es wesvh".
- L3: Docker client/server 29.4.0 available. `gh` has only a corporate account, not wesvh; no remote account switch, probe or publication performed. Receipt-driven review is globally disabled; ordinary checks and named-risk independent verification remain applicable.
- L4: Existing workspace has only Entrega 1 deliverables and unrelated untracked documents. CodeGraph reports no index and directs filesystem fallback. No project skill registry; installed exact skill paths will be injected. Engram project reads/writes fail with unknown_project; mirror pending, no project guessing.
- L5: Worker launch refused: configured `gpt-6.1-luna` is unavailable; runtime offers `gpt-6-luna`, among other models. No worker launched and no product code was written. Await user authorization for model substitution; do not bypass the fired delegation boundary inline.
- L6, 2026-10-25: "Si, continua" authorizes replacing unavailable writer model with `gpt-6-luna`. Continue authorized local implementation; personal GitHub authentication still pending.
- L7: Backend integration corrected missing static directory discovery and missing seeded admin creation; regression tests added. No meaningful framework RED run was observed before initial code because the Docker runner did not exist; do not claim TDD RED/GREEN. Full suite subsequently ran against MySQL 8.4.13: 23 tests passed; configuration, migration drift and HTTP/static checks passed.
- L8: Real browser registration, login, POST logout, Admin category creation and dynamic public visibility verified. Category ID 3 persisted after stopping web and running the single startup command again. Mobile DOM measured at effective width 360 without horizontal overflow; only unaltered default-viewport JPEG captures are retained. Report layout shows explicitly described fragments for legibility.
- L9: The local Docker credential helper stalled a public image pull. Verification used an isolated anonymous Docker client configuration against the same local Unix-socket engine, without using registry credentials or changing global Docker settings. Temporary client directory must be removed after checks. Fresh installation otherwise requires working access to public registries as documented.
- L10: Runtime commits are larger coherent bootstrap units (backend plus tests: 832 lines; presentation: 274; infrastructure/docs: 371), not separate PR deliveries. No PR requested or created; RDD globally disabled. Existing workspace files and Entrega 1 were not committed or changed.
- L11: Independent verifier checked frozen runtime candidate cfe938d25c1809fe4c7e2f85c454d1359f4a2218 in a fresh system-temporary checkout and isolated Docker project. Fresh startup, 23/23 MySQL tests, migration drift, auth/CSRF/admin/static checks, container restrictions and restart persistence passed. No reproducible blockers. Native assessment with explicit base reported high risk; RDD remains disabled/unmanaged, with no review receipt claimed.
- L12: Parent spot check reran Django check successfully and confirmed original database counts [2,3,4,4] plus category ID 3 against evidence/restart.json. Independent test database was removed separately; main database volume remains intact. Final deliverable package uses tracked files only, excluding local secrets and Git metadata.
- L13: PDF has 11 Letter pages, correct sole author/professor and real screenshot fragments. Program, demonstration video, private publication and teacher access are explicitly pending. No public repository, invented video or team participation is claimed. Engram summary/context still reject detected project; recovery log remains local.
