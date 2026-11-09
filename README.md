# Festival Vallenato 2027 - Entrega 3

Aplicación académica funcional con **Python 3.12, Django 5.2 LTS, MySQL 8.4 y Docker Compose**. Dependencias Python en `requirements.txt`. Datos ficticios, no oficiales. Autor: **Esteban Villada Henao**. Docente: **DEIVYS MORALES URIBE**.

## Iniciar con un comando

Ubicación de trabajo del autor en macOS, fuera de ChatGPT: `~/Documents/Universidad/festival-vallenato-2027`.

```sh
cd "$HOME/Documents/Universidad/festival-vallenato-2027"
./start.sh
```

Requisitos: Docker con Compose v2, motor iniciado, conexión a internet durante la primera descarga y puerto 8000 libre. Ejecutar desde una terminal macOS/Linux o WSL en Windows:

```sh
./start.sh
```

El comando genera secretos locales aleatorios en `.env` si no existe, construye la imagen, espera MySQL, aplica migraciones, registra datos ficticios y un administrador, recopila estáticos e inicia Gunicorn. La primera ejecución descarga imágenes y dependencias y puede tardar varios minutos. No se requiere instalar Python o MySQL en el equipo.

- Aplicación: http://localhost:8000/
- Administración: http://localhost:8000/admin/
- Estado: http://localhost:8000/health/
- Usuario y contraseña administrativos: consultar **solo localmente** `DEMO_ADMIN_USER` y `DEMO_ADMIN_PASSWORD` dentro de `.env`. No adjuntar ese archivo al PDF, video, ZIP o repositorio.

Si 8000 está ocupado, modificar únicamente `WEB_PORT` en `.env` y ejecutar otra vez `./start.sh`. No cambiar contraseñas de MySQL en `.env` después de inicializar el volumen sin realizar una rotación coordinada.

## Funcionalidades

- Registro público con validadores y hash de contraseñas de Django.
- Inicio de sesión y cierre mediante POST con CSRF; registro público sin permisos administrativos.
- Django Admin para crear, consultar y editar ediciones, categorías, votaciones y opciones.
- Catálogo público dinámico obtenido de MySQL: **Edición → Categoría → Votación → Opción**.
- Votaciones en borrador ocultas en interfaces públicas y en accesos directos.
- Datos de ejemplo de 2027 y 2028; estados vacíos y errores 404.
- Interfaz responsive sin recursos remotos; estáticos mediante WhiteNoise.
- **Entrega 3:** emisión de votos con confirmación, un voto por usuario, categoría y edición, página «Mis votos», consulta administrativa de votos y `GET /api/categorias/` en JSON.

No incluye resultados oficiales, jurados ni controles definitivos de elegibilidad.

## Módulo de votaciones (Entrega 3)

Regla central: cada usuario elige **una sola opción por categoría y edición**. Puede votar en otras categorías, pero no emitir un segundo voto en la misma categoría aunque esta tenga varios subeventos (votaciones).

Flujo: iniciar sesión → elegir categoría → abrir una votación → seleccionar una opción → **confirmar** → validación en Django → registro en MySQL.

- Formulario POST con token CSRF en `templates/catalog/poll_detail.html`; paso de confirmación en `templates/catalog/vote_confirm.html`; vista `vote` en `catalog/views.py`.
- Validaciones del servidor en `catalog/voting.py`: sesión iniciada, votación habilitada (estado «Abierta»), opción perteneciente a la votación y ausencia de un voto previo en la categoría. Edición, categoría y votación se derivan de la opción en el servidor; nunca se toman del cliente.
- Unicidad en base de datos: modelo `Vote` en `catalog/models.py` con `UniqueConstraint(fields=["user", "category", "edition"])` (migración `catalog/migrations/0002_vote.py`). `cast_vote` en `catalog/voting.py` captura `IntegrityError`, de modo que dos solicitudes simultáneas almacenan un único voto.
- «Mis votos»: `/my-votes/`, solo para usuarios autenticados, muestra únicamente los votos propios.
- Administración: Django Admin → Votos, de solo lectura (sin alta, edición ni borrado), con filtros por edición, categoría y votación.
- API: `GET /api/categorias/` en `catalog/api.py` devuelve JSON con categorías, edición, estado `habilitada`, votaciones públicas (abiertas y cerradas) y sus opciones desde MySQL. Las votaciones en borrador no se exponen. Otros métodos HTTP responden 405.

```sh
curl -s http://localhost:8000/api/categorias/
```

Datos de prueba (`seed_demo`, ficticios) por edición: «Rey Vallenato» con dos votaciones abiertas, «Canción inédita» abierta, «Piquería» cerrada y una votación en borrador oculta. Para votar, registrar un usuario de prueba en `/accounts/register/`.

### Casos de prueba automatizados

Archivo `catalog/test_voting.py`, ejecutado contra MySQL real:

| Caso | Prueba |
|------|--------|
| CP-01 voto válido con confirmación | `test_cp01_valid_vote_requires_confirmation_then_persists_derived_relations` |
| CP-02 segundo voto en la misma categoría | `test_cp02_second_vote_in_same_category_is_rejected_for_other_option_and_subevent` |
| CP-03 voto en otra categoría | `test_cp03_vote_in_a_different_category_is_allowed` |
| CP-04 usuario sin sesión | `test_cp04_anonymous_user_is_sent_to_login_and_nothing_is_stored` |
| CP-05 categoría cerrada | `test_cp05_closed_poll_rejects_vote_and_draft_poll_is_not_found` |
| CP-06 opción de otra categoría | `test_cp06_option_from_another_category_is_rejected` |
| CP-07 «Mis votos» | `test_cp07_my_votes_lists_only_the_users_own_voted_categories` |
| CP-08 consulta administrativa | `test_cp08_admin_vote_list_matches_database_and_is_read_only` |
| CP-09 solicitudes simultáneas | `test_cp09_simultaneous_requests_store_a_single_vote` |
| CP-10 API JSON | `test_cp10_get_returns_valid_json_with_categories_and_options_from_database` |

Pruebas adicionales: rechazo sin token CSRF (403), GET al endpoint de voto (405), restricción única en base de datos, consultas constantes en la API.

```sh
docker compose exec -T web python manage.py test catalog.test_voting --noinput
```

## Modelo y estructura MVT

```text
config/                 configuración, rutas raíz y WSGI
accounts/               registro e inicio/cierre de sesión; pruebas
catalog/                modelos, vistas, Admin, votación (voting.py), API (api.py), migraciones y pruebas
catalog/management/     comando seed_demo idempotente
templates/              plantillas Django con datos reales
static/                 estilos locales
docker/                 migraciones de arranque y permisos del test DB
scripts/                generación local de secretos
evidence/               capturas y resultados verificables, sin credenciales
reports/                informe PDF y documentación de demostración
```

Relaciones de uno a muchos mediante claves foráneas. La combinación padre/nombre evita categorías y opciones duplicadas en el mismo contexto. Se usa autenticación nativa de Django, no contraseñas en texto plano.

## Pruebas y migraciones

Con el sistema iniciado, las pruebas usan **MySQL real**, en `test_festival`, separado de `festival`:

```sh
docker compose exec -T web python manage.py test accounts catalog --noinput
docker compose exec -T web python manage.py check
docker compose exec -T web python manage.py makemigrations --check --dry-run
docker compose exec -T web python manage.py showmigrations
```

Las migraciones están versionadas y se aplican automáticamente en cada arranque. No se ejecuta `makemigrations` al iniciar. `seed_demo` usa creación condicional: reiniciar no borra datos, no duplica registros ni restablece contraseñas o cambios existentes.

## Detener y volver a iniciar

```sh
docker compose down
./start.sh
```

Los datos permanecen en un volumen nombrado. **No usar `docker compose down -v` salvo que se desee eliminar toda la base de datos.** Guardar `.env` de forma privada para conservar las credenciales que corresponden al volumen.

## Seguridad y límites

Aplicación enlazada únicamente a `127.0.0.1`, MySQL sin puerto publicado, usuario no root en web, `DEBUG=False`, secretos fuera de Git y del contexto de construcción. El usuario web no recibe la contraseña root de MySQL. El permiso adicional `test_festival.*` es exclusivo de este entorno académico para ejecutar pruebas.

Esto **no es un despliegue productivo**: no incluye TLS, correo de recuperación, política institucional de datos, protección avanzada contra abuso ni respaldo operacional. No introducir información personal real. El código es público por autorización expresa; las credenciales y bases de datos locales no se publican.

## Repositorio y entrega académica

Repositorio **público**: [wesvh/web-dev-areandina-2027](https://github.com/wesvh/web-dev-areandina-2027), rama `master`. Publicado mediante SSH de la cuenta personal `wesvh`; no se utilizó una sesión corporativa. La autorización del 26 de octubre de 2026 reemplaza la solicitud inicial de privacidad.

Para descargar y ejecutar, con Git y Docker disponibles:

```sh
git clone https://github.com/wesvh/web-dev-areandina-2027.git && cd web-dev-areandina-2027 && ./start.sh
```

El repositorio incluye código, migraciones, pruebas, capturas y el PDF en `reports/Entrega_2_Vallenato_2027_APA.pdf`. Publicar código no aloja la aplicación: cada lector la ejecuta localmente con Docker.

Material de cierre: `reports/GUION_PASO_A_PASO.md` contiene un recorrido de dos lados con narración, enlaces, comandos y resultados esperados; `reports/GUION_VIDEO.md` conserva el guion resumido. `reports/CHECKLIST_ENTREGA.md` distingue requisitos cumplidos y pendientes del docente. Las siete capturas actuales son de escritorio, con ventana de 1440×900; dimensiones y rutas constan en `evidence/desktop.json`. El PDF conserva 11 páginas y explica cualquier detalle de cabecera mostrado por separado.

La entrega oficial requiere un único PDF con evidencias, enlace al repositorio y video. El programa académico fue confirmado como **DESARROLLO WEB** e incorporado en la portada. Falta el video real y su enlace. La guía exige cuatro participantes; se conserva autor único por indicación del usuario y se advierte que el criterio grupal otorga 0/5 a entregas individuales. La guía recibida no prevé una excepción por trabajar en una empresa. No se ha aportado autorización docente que modifique el requisito, ni se inventa participación o una revisión efectuada por el docente.
