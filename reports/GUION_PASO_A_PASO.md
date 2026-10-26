# Video: guion completo con lado A y lado B

**Autor:** Esteban Villada Henao. **Programa y asignatura:** Desarrollo Web. **Docente:** Deivys Morales Uribe. Duración sugerida: 5 a 6 minutos; el docente no fija duración.

## Cómo utilizarlo

- **Lado A, fuera de la grabación:** este guion. Lee una fila y sigue sus pasos antes de pasar a la siguiente.
- **Lado B, dentro de la grabación:** navegador maximizado o Terminal. Cada enlace abre la pantalla que debes mostrar. En macOS puedes alternar ventanas con `⌘ Tab`.
- Graba la aplicación real en computador, no el prototipo HTML ni el modo móvil. Cambia la ventana capturada cuando pases del navegador a Terminal.
- No muestres `.env`, contraseñas, claves SSH, `docker compose config` ni variables del entorno. Pausa la grabación al introducir contraseñas; reanuda mostrando el resultado.
- No leas «funciona» o «aprobado» sin comprobar la salida. El guion no reemplaza la grabación ni la entrega oficial.

## Paso 0. Preparar todo antes de grabar

### Arranque desde la carpeta nueva

Con Docker Desktop activo, abre Terminal y pega:

```sh
cd "$HOME/Documents/Universidad/festival-vallenato-2027"
./start.sh
```

Espera `Application is healthy`. La primera descarga puede tardar; no necesitas grabar esa espera. Después ejecuta:

```sh
docker compose ps
```

Debes ver `db` y `web` saludables. No continúes si aparecen errores. **Nunca uses `docker compose down -v` para esta prueba: elimina la base de datos.**

### Acceso administrativo, con la grabación detenida

1. Consulta localmente `DEMO_ADMIN_USER` y `DEMO_ADMIN_PASSWORD` en `.env` de la carpeta nueva.
2. Cierra ese archivo y cualquier ventana que muestre credenciales.
3. Abre [Django Admin](http://localhost:8000/admin/) e inicia sesión con esos datos.
4. Conserva esa sesión hasta terminar administración. Después cerrarás sesión para mostrar un usuario normal.

Los enlaces locales suponen puerto 8000. Si lo cambiaste, reemplaza el puerto en las direcciones.

### Pestañas listas para alternar

| Pantalla | Enlace directo |
|---|---|
| Inicio y ediciones | [Abrir catálogo](http://localhost:8000/) |
| Modelos | [Ver catalog/models.py](https://github.com/wesvh/web-dev-areandina-2027/blob/master/catalog/models.py) |
| Vistas ORM | [Ver catalog/views.py](https://github.com/wesvh/web-dev-areandina-2027/blob/master/catalog/views.py) |
| Migración | [Ver 0001_initial.py](https://github.com/wesvh/web-dev-areandina-2027/blob/master/catalog/migrations/0001_initial.py) |
| Administración | [Abrir Admin](http://localhost:8000/admin/) |
| Edición 2027 | [Abrir categorías de 2027](http://localhost:8000/editions/1/) |
| Opciones | [Abrir votación de muestra](http://localhost:8000/polls/1/) |
| Repositorio | [Abrir GitHub y README](https://github.com/wesvh/web-dev-areandina-2027) |
| Informe | [Abrir PDF](https://github.com/wesvh/web-dev-areandina-2027/blob/master/reports/Entrega_2_Vallenato_2027_APA.pdf) |

Los identificadores corresponden a los datos ficticios conservados. Si eliminaste o cambiaste esos registros, navega desde [inicio](http://localhost:8000/) por los nombres disponibles.

## Escena 1. Presentación — 0:00 a 0:30

| Lado A: texto para decir | Lado B: abrir y hacer |
|---|---|
| «Soy Esteban Villada Henao y presento la segunda entrega del sistema del Festival de la Leyenda Vallenata 2027, para Desarrollo Web, con el docente Deivys Morales Uribe. El objetivo es implementar una aplicación Django con MySQL, autenticación, administración y consulta dinámica. Los datos son ficticios. En esta fase todavía no se registran votos ni se publican resultados». | **1.** Abre [inicio](http://localhost:8000/). **2.** Muestra título, aviso académico y tarjetas de 2027/2028. **3.** No pulses botones mientras te presentas. |

**Debes ver:** catálogo de ediciones en disposición de computador, sin errores.

## Escena 2. Ejecución, MVT y relaciones — 0:30 a 1:20

| Lado A: texto para decir | Lado B: abrir y hacer |
|---|---|
| «El proyecto sigue MVT: los modelos definen los datos, las vistas consultan mediante el ORM y las plantillas generan la interfaz. Accounts gestiona autenticación y catalog organiza el catálogo». | **1.** Abre [repositorio](https://github.com/wesvh/web-dev-areandina-2027). Señala `accounts`, `catalog` y `templates`. **2.** Abre [modelos](https://github.com/wesvh/web-dev-areandina-2027/blob/master/catalog/models.py) y señala `Edition`, `Category`, `Poll`, `Option` y sus `ForeignKey`. |
| «La relación principal es edición, categoría, votación y opción. Docker inicia MySQL y Django; el arranque espera la base y aplica migraciones versionadas». | **3.** Abre [migración](https://github.com/wesvh/web-dev-areandina-2027/blob/master/catalog/migrations/0001_initial.py). **4.** Pasa a Terminal y ejecuta los comandos siguientes. |
| «Aquí se ven los servicios saludables y las migraciones aplicadas. El volumen conserva los datos entre reinicios». | **5.** Señala `healthy` y las marcas `[X]`. No afirmes haber reiniciado durante esta escena si solo muestras el estado. |

```sh
docker compose ps
docker compose exec -T web python manage.py showmigrations
```

No hace falta repetir el arranque durante la grabación si ya está iniciado. Puedes mostrar [start.sh](https://github.com/wesvh/web-dev-areandina-2027/blob/master/start.sh) para explicar qué hace.

## Escena 3. Guardar un dato y comprobarlo públicamente — 1:20 a 2:15

| Lado A: texto para decir | Lado B: abrir y hacer |
|---|---|
| «Utilizo Django Admin, permitido en esta entrega, para administrar ediciones, categorías, votaciones y opciones». | **1.** Abre [Admin](http://localhost:8000/admin/). Señala los cuatro modelos. Consulta [ediciones](http://localhost:8000/admin/catalog/edition/), [categorías](http://localhost:8000/admin/catalog/category/), [votaciones](http://localhost:8000/admin/catalog/poll/) y [opciones](http://localhost:8000/admin/catalog/option/). |
| «Voy a registrar una categoría ficticia vinculada a la edición 2027». | **2.** Abre [añadir categoría](http://localhost:8000/admin/catalog/category/add/). En **Edition**, selecciona `Festival Vallenato 2027`. En **Name**, escribe `Demostración del video 2026-10-26`. En **Description**, escribe `Categoría ficticia creada durante la demostración académica.` |
| «Al guardar, Django valida la relación y almacena el registro en MySQL». | **3.** Pulsa **Guardar** y espera la confirmación real. Si el nombre ya existe, utiliza otro, por ejemplo el mismo terminado en `2`. No borres registros anteriores para repetir la toma. |
| «Al consultar la página pública aparece el mismo registro. Esto demuestra que la interfaz obtiene datos de MySQL y no de una lista fija escrita en HTML». | **4.** Abre [edición 2027](http://localhost:8000/editions/1/). Recarga si estaba abierta y señala la tarjeta que acabas de guardar. |

**Debes ver:** confirmación de Admin y categoría nueva en la interfaz pública. Este paso crea un dato ficticio real, pero no cambia modelos ni exige crear migraciones nuevas.

## Escena 4. Edición, categoría, votación y opciones — 2:15 a 2:50

| Lado A: texto para decir | Lado B: abrir y hacer |
|---|---|
| «La navegación conserva las relaciones entre edición, categoría y votación. Aquí se muestran las opciones consultadas mediante el ORM». | **1.** Abre [edición 2027](http://localhost:8000/editions/1/). **2.** Entra en [Rey Vallenato - muestra ficticia](http://localhost:8000/categories/1/). **3.** Entra en [Artista favorito 2027 - muestra](http://localhost:8000/polls/1/). Señala estado, descripción y opciones. Usa la categoría de muestra: la recién creada puede estar vacía. |
| «Las ediciones se configuran por separado. La pantalla informa que todavía no registra votos: esa funcionalidad corresponde a una entrega posterior». | **4.** Abre [edición 2028](http://localhost:8000/editions/2/). **5.** Para enseñar la consulta, abre [vistas ORM](https://github.com/wesvh/web-dev-areandina-2027/blob/master/catalog/views.py) y señala la consulta de ediciones o `get_object_or_404`. |

## Escena 5. Registro, inicio y cierre de sesión — 2:50 a 3:45

Primero vuelve al [catálogo](http://localhost:8000/). Si aparece la sesión administrativa, pulsa **Cerrar sesión**. Ese botón envía POST: no debes abrir manualmente una URL GET de cierre.

| Lado A: texto para decir | Lado B: abrir y hacer |
|---|---|
| «El registro utiliza formularios y validadores de Django. Las contraseñas se almacenan mediante hash, no en texto plano». | **1.** Abre [crear cuenta](http://localhost:8000/accounts/register/) y muestra los campos vacíos. **2.** Pausa la grabación. Introduce un usuario ficticio disponible, por ejemplo `video_esteban_20261026`, y una contraseña segura elegida por ti; confírmala y pulsa **Crear cuenta**. |
| «La cuenta se creó y ahora puedo iniciar sesión con ella». | **3.** El registro vuelve al inicio; **no inicia sesión automáticamente**. Abre [iniciar sesión](http://localhost:8000/accounts/login/). Con la grabación pausada, introduce esa cuenta y pulsa el botón de acceso. Reanuda cuando ya no aparezca la contraseña. |
| «Un usuario registrado no recibe privilegios administrativos. Aquí aparece su nombre y no se muestra el enlace de administración». | **4.** Señala el nombre de la cuenta ficticia. No uses `admin_demo` para afirmar que es un usuario sin privilegios. |
| «Al cerrar sesión vuelven los enlaces de acceso. Los formularios incluyen protección CSRF y el cierre se envía mediante POST». | **5.** Pulsa **Cerrar sesión**. Muestra de nuevo **Iniciar sesión** y **Crear cuenta**. |

Si el usuario ya existe, usa uno nuevo. Si una contraseña es rechazada, corrígela con la grabación pausada. No presentes un error como registro satisfactorio.

## Escena 6. Pruebas — 3:45 a 4:35

Pasa a Terminal. Si abriste otra terminal, sitúate primero en la carpeta nueva:

```sh
cd "$HOME/Documents/Universidad/festival-vallenato-2027"
```

Ejecuta **uno por uno**, esperando cada resultado:

```sh
docker compose exec -T web python manage.py test accounts catalog --noinput
```

```sh
docker compose exec -T web python manage.py check
```

```sh
docker compose exec -T web python manage.py makemigrations --check --dry-run
```

| Lado A: decir solo si coincide con la salida | Lado B: señalar |
|---|---|
| «La suite contiene 23 pruebas y todas finalizaron correctamente contra una base MySQL de prueba aislada». | **1.** Señala `Ran 23 tests` y `OK`. La base de prueba es `test_festival`, separada del catálogo `festival`. |
| «La comprobación de configuración no reporta problemas y no hay diferencias pendientes entre modelos y migraciones». | **2.** Señala `System check identified no issues` y `No changes detected`. |
| «Se revisan autenticación, permisos, relaciones y consultas públicas. Esto no sustituye una evaluación de seguridad o carga de producción». | **3.** Si quieres mostrar ejemplos, abre [pruebas de autenticación](https://github.com/wesvh/web-dev-areandina-2027/blob/master/accounts/tests.py) y [pruebas del catálogo](https://github.com/wesvh/web-dev-areandina-2027/blob/master/catalog/tests.py). |

Si el número o resultado cambia, describe lo observado. No leas «23 aprobadas» sin salida que lo respalde.

## Escena 7. Repositorio, informe y cierre — 4:35 a 5:30

| Lado A: texto para decir | Lado B: abrir y hacer |
|---|---|
| «El repositorio es público e incluye código, migraciones, pruebas y README de instalación. Con Docker activo se ejecuta mediante start.sh. Los secretos locales no se publican». | **1.** Abre [repositorio](https://github.com/wesvh/web-dev-areandina-2027). **2.** Abre [README](https://github.com/wesvh/web-dev-areandina-2027/blob/master/README.md) y señala el comando de inicio. |
| «El informe documenta arquitectura, datos, pruebas y capturas reales de la aplicación en computador». | **3.** Abre [PDF](https://github.com/wesvh/web-dev-areandina-2027/blob/master/reports/Entrega_2_Vallenato_2027_APA.pdf). Muestra portada y una página de capturas, sin leerlo completo. |
| «Aprendí a integrar MVT, ORM y MySQL. Las dificultades principales fueron configurar los estáticos y crear el administrador de forma idempotente. Quedan para futuras entregas el registro definitivo de votos, elegibilidad y resultados. Soy responsable de revisar, explicar y validar el trabajo presentado». | **4.** Vuelve al [inicio](http://localhost:8000/) y termina la grabación. |

GitHub aloja el código, no la aplicación Django en ejecución. No afirmes participación de otras personas ni aprobación docente de la entrega individual.

## Después de grabar

1. Revisa audio, legibilidad y ausencia de credenciales; recorta pausas de contraseña.
2. Publica el video con permisos de consulta para el docente. Comprueba el enlace desde otra sesión.
3. Proporciona el enlace real para incorporarlo, clicable, en el PDF. El guion no sustituye el video.
4. Revisa [checklist académico](https://github.com/wesvh/web-dev-areandina-2027/blob/master/reports/CHECKLIST_ENTREGA.md). Programa confirmado: **DESARROLLO WEB**.
5. Envía el único PDF oficial en plataforma antes del plazo indicado: **26 de octubre de 2026**. No se ha realizado un envío desde esta preparación.

**Requisito grupal:** la guía exige cuatro integrantes y participación demostrable. El autor único fue solicitado expresamente, pero no satisface ese requisito: la entrega individual obtiene 0/5 en trabajo en equipo. No hay una excepción por empresa en la guía recibida ni autorización docente aportada. No inventes compañeros ni una excepción.
