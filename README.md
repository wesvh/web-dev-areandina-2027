# Festival Vallenato 2027 - Entrega 2

Aplicación académica funcional con **Django 5.2 LTS, MySQL 8.4 y Docker Compose**. Datos ficticios, no oficiales. Autor: **Esteban Villada Henao**. Docente: **DEIVYS MORALES URIBE**.

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

No incluye todavía emisión de votos, resultados oficiales, jurados ni controles definitivos de elegibilidad. El diseño conserva esa ampliación para fases posteriores.

## Modelo y estructura MVT

```text
config/                 configuración, rutas raíz y WSGI
accounts/               registro e inicio/cierre de sesión; pruebas
catalog/                modelos, vistas, Admin, migraciones y pruebas
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
