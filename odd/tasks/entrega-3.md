# Entrega 3 - Voting module
Outcome: real voting module on top of Entrega 2 (Vote model, POST vote flow with confirmation, uniqueness per user/category/edition, my-votes page, read-only admin, GET /api/categorias/), CP-01..CP-10 automated against MySQL. Branch `feat/entrega-3-votaciones` from `codex/entrega-2`.
Scope: code, tests, seed and README only. PDF, video and team composition are out of scope for this unit.

## Specs
- S1 "Regla central: cada usuario puede elegir una sola opción por categoría y edición. Puede votar en otras categorías, pero no emitir un segundo voto en la misma categoría, aunque esta contenga varios subeventos."
- S2 "Agregar o adaptar el modelo de votos, vinculando usuario, edición, categoría y opción. Aplicar migraciones en MySQL."
- S3 "Implementar formularios y vistas Django para votar mediante POST y protección CSRF." Flow: "Iniciar sesión → Elegir categoría → Seleccionar una opción → Confirmar → Validar en Django → Registrar en MySQL".
- S4 "Validar en el servidor que la opción pertenece a la categoría y edición, que la votación está habilitada y que el usuario no ha votado previamente."
- S5 "Incluir una restricción de unicidad en la base de datos por usuario, categoría y edición (...), gestionando los errores de integridad." Includes concurrency (CP-09).
- S6 "Mostrar categorías votadas al usuario y permitir consulta administrativa de registros."
- S7 "Crear GET /api/categorias/ que entregue categorías y opciones desde MySQL en formato JSON."
- S8 README: "descripción, tecnologías, versión de Python/Django, dependencias, instalación, configuración de MySQL sin secretos, migraciones, creación de datos de prueba y comandos"; PDF must cite API file and uniqueness file paths.

Design decision (user-approved 2026-11-08): "categoría habilitada" = the option's Poll (subevento) has status OPEN. Edition/category/poll on Vote are derived server-side from the option, never from the client.

## Tasks
- [x] T1 Vote model + migration 0002 + DB unique constraint (S1, S2, S5)
- [x] T2 voting service, form, vote/confirm views, my-votes, templates (S3, S4, S6)
- [x] T3 read-only VoteAdmin (S6)
- [x] T4 GET /api/categorias/ (S7)
- [x] T5 seed: multi-subevent category, second open category, closed category
- [x] T6 tests CP-01..CP-10 + CSRF + constraint; full suite, check, makemigrations --check
- [x] T7 README update (S8)

## Log
- L1 User: "Implementalo, implementa todo lo relacionado a codigo que menciona la tarea"
- L2 GREEN: catalog.test_voting 19/19; full suite accounts+catalog 43/43 on MySQL; check clean; makemigrations --check: no changes.
- L3 Test runner note: bind-mounted ephemeral container needs collectstatic before tests (manifest storage).
