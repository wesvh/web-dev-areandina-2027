# Guion para grabar la demostración - Entrega 2

Para grabar alternando entre narración y demostración, utiliza [el guion paso a paso con enlaces directos](GUION_PASO_A_PASO.md). Carpeta local del proyecto: `~/Documents/Universidad/festival-vallenato-2027`, fuera de ChatGPT.

Duración sugerida: 5 a 6 minutos; la guía del docente no fija duración. Grabar desde computador, con texto legible y la aplicación Django real, no el prototipo HTML. Adaptar las frases a lo que se muestre efectivamente.

**Advertencia académica:** el docente exige cuatro integrantes y su participación en el video. Este guion conserva a Esteban Villada Henao como único autor, por solicitud expresa, pero no subsana ese requisito. La entrega individual obtiene 0/5 en trabajo en equipo. No inventar participantes ni una excepción del docente.

## Antes de grabar

- Tener Docker activo y el proyecto abierto. Iniciar con `./start.sh` antes de grabar para evitar tiempos de descarga.
- Abrir catálogo, Admin, editor con `catalog/models.py` y `catalog/views.py`, y repositorio público.
- Entrar a Admin fuera de la grabación. No abrir `.env`, `config/settings.py` con valores locales desplegados, historial de contraseñas ni configuración SSH.
- Preparar una cuenta y una categoría ficticias para la demostración; no usar datos personales reales.
- Al registrar o iniciar sesión, pausar la grabación durante la entrada de contraseñas y reanudar al mostrar el resultado. Nunca revelar credenciales, incluso si son de prueba.

## 1. Presentación y alcance - 0:00 a 0:30

**Mostrar:** portada o página principal.

**Decir:**

> Soy Esteban Villada Henao y presento la segunda entrega del sistema del Festival de la Leyenda Vallenata 2027, para Desarrollo Web, con el docente Deivys Morales Uribe. El objetivo es implementar una aplicación Django con MySQL, autenticación, administración y consulta dinámica. Los datos son ficticios. En esta fase todavía no se registran votos ni se publican resultados.

## 2. Ejecución y estructura técnica - 0:30 a 1:20

**Mostrar:** comando de inicio y servicios saludables; después, árbol del proyecto y un fragmento de modelos.

```sh
./start.sh
docker compose ps
docker compose exec -T web python manage.py showmigrations
```

Si el sistema ya está iniciado, mostrar el comando y el estado sin ejecutar otro arranque durante el video. No afirmar que una operación se ejecutó en ese momento si no ocurrió.

**Decir:**

> El proyecto sigue MVT: los modelos definen los datos, las vistas consultan mediante el ORM y las plantillas generan la interfaz. La aplicación accounts gestiona autenticación y catalog organiza el catálogo. Docker inicia MySQL y Django; el arranque espera la base de datos y aplica migraciones versionadas. La relación principal es edición, categoría, votación y opción. Las marcas de migraciones muestran cuáles están aplicadas.

## 3. Administración y persistencia - 1:20 a 2:15

**Mostrar:** Admin con ediciones 2027 y 2028, categorías, votaciones y opciones. Crear una categoría ficticia, por ejemplo `Demostración del video`, asociada a 2027. Guardar y mostrar confirmación real. Abrir la edición pública y comprobar que aparece.

**Decir:**

> Utilizo Django Admin, permitido en esta entrega, para administrar las entidades. Esta categoría queda vinculada a la edición 2027. Al guardarla y consultar la página pública aparece el mismo registro. Esto demuestra que la interfaz obtiene datos persistidos en MySQL y no una lista fija escrita en HTML.

No simular confirmaciones ni borrar registros previos. Si se demuestra un reinicio, detener solo web y arrancar de nuevo; no ejecutar `down -v`, porque elimina la base de datos.

## 4. Navegación pública - 2:15 a 2:50

**Mostrar:** edición 2027, categoría de muestra, votación y opciones; regresar y consultar 2028. Evitar la categoría recién creada para el recorrido de opciones, porque todavía puede estar vacía.

**Decir:**

> La navegación conserva las relaciones entre edición, categoría y votación. Aquí se muestran las opciones participantes consultadas mediante el ORM. Las ediciones se configuran por separado. La pantalla informa que todavía no registra votos: esa funcionalidad corresponde a una entrega posterior.

## 5. Registro, inicio y cierre de sesión - 2:50 a 3:45

**Mostrar:** formulario de registro, resultado de crear una cuenta ficticia, inicio de sesión y cierre. Pausar o recortar la entrada de contraseñas. Usar un nombre de usuario disponible; si hay un error, corregirlo antes de continuar.

**Decir:**

> El registro utiliza formularios y validadores de Django. Las contraseñas se almacenan mediante hash, no en texto plano. Un usuario registrado no recibe privilegios administrativos. Después de iniciar sesión aparece su nombre; al cerrar sesión vuelven los enlaces de acceso. El cierre se envía mediante POST y los formularios incluyen protección CSRF.

Si la cuenta utilizada es administradora, identificarla como tal; no presentarla como prueba de un usuario sin privilegios.

## 6. Pruebas y resultados - 3:45 a 4:35

**Mostrar:** salida real de las pruebas y comprobación de configuración.

```sh
docker compose exec -T web python manage.py test accounts catalog --noinput
docker compose exec -T web python manage.py check
docker compose exec -T web python manage.py makemigrations --check --dry-run
```

**Decir, únicamente si la salida lo confirma:**

> La suite contiene 23 pruebas y todas finalizaron correctamente contra una base MySQL de prueba aislada. Se revisan autenticación, permisos, relaciones y consultas públicas. La comprobación de configuración no reporta problemas y no hay diferencias pendientes entre modelos y migraciones. Estos resultados no sustituyen una evaluación de seguridad o carga de producción.

Si falla una comprobación, no afirmar que pasó ni ocultar el resultado como una verificación satisfactoria.

## 7. Repositorio, aprendizajes y cierre - 4:35 a 5:30

**Mostrar:** https://github.com/wesvh/web-dev-areandina-2027, README y PDF con capturas de escritorio.

**Decir:**

> El repositorio es público e incluye código, migraciones, pruebas y README de instalación. Con Docker activo se ejecuta mediante start.sh. Los secretos locales no se publican. Aprendí a integrar MVT, ORM y MySQL; las dificultades principales fueron configurar los estáticos y la creación idempotente del administrador. Quedan para futuras entregas el registro definitivo de votos, elegibilidad y resultados. Soy responsable de revisar, explicar y validar el trabajo presentado.

Publicar el código en GitHub no aloja la aplicación en internet. No afirmar participación de otras personas ni aprobación docente de la entrega individual.

## Después de grabar

1. Revisar legibilidad, audio y ausencia de credenciales o datos personales.
2. Subir el video y habilitar consulta para el docente. Comprobar el enlace desde otra sesión.
3. Incorporar el enlace real y clicable en el PDF; no entregar este guion como sustituto del video.
4. Comprobar que la portada indique **Programa académico: DESARROLLO WEB**, confirmado por el autor, y revisar la advertencia de trabajo grupal.
5. Enviar el único PDF oficial en la plataforma antes del plazo: **26 de octubre de 2026**. La guía indica que cada integrante realiza su envío.

La guía suministrada no contiene una excepción por trabajar en una empresa. Cualquier solicitud de entregar individualmente sería una petición al docente, no un permiso ya otorgado. Si existe una comunicación adicional, debe revisarse antes de afirmar una modificación del requisito o de la rúbrica.
