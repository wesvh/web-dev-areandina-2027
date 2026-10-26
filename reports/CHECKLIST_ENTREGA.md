# Estado frente a lo solicitado por el docente

Revisión: 26 de octubre de 2026. Fuente: guía suministrada por el usuario, **Entrega 2 - Festival Vallenato 2027**, secciones 02, 03, 05, 06, 07 y 08. La fecha máxima indicada es **26 de octubre de 2026**; no se especifica hora en la guía.

**Estado global: implementación técnica lista y verificada; entrega académica todavía incompleta.** Programa académico confirmado e incorporado: **DESARROLLO WEB**. Faltan video real con enlace incorporado y envío oficial. Además, la entrega individual no cumple el requisito obligatorio de cuatro integrantes.

## Requisitos técnicos

| Solicitud del docente | Estado | Evidencia disponible |
|---|---|---|
| Proyecto Python/Django, aplicaciones, rutas, vistas, plantillas y patrón MVT | CHECK | `config`, `accounts`, `catalog`, `templates` y explicación técnica en PDF. |
| MySQL, modelos relacionados y migraciones ejecutadas | CHECK | MySQL real, migración versionada y prueba de reinicio persistente. |
| Relación edición → categoría → votación → opción | CHECK | Claves foráneas y restricciones en `catalog/models.py`. |
| Registro, inicio y cierre de sesión con mecanismo Django | CHECK | Formularios y sesiones nativas; pruebas de hash, permisos y CSRF. |
| Registrar y consultar diferentes ediciones | CHECK | Ediciones ficticias 2027 y 2028 administrables y visibles. |
| Categorías vinculadas a edición; votaciones y opciones administrables | CHECK | Django Admin y relaciones verificadas. La guía permite usar Admin. |
| Interfaz pública con datos reales de MySQL | CHECK | Consultas ORM y categoría ID 3 creada en Admin visible públicamente. |
| Pruebas y resultados documentados | CHECK | 23/23 pruebas MySQL observadas y repetidas por verificador independiente. No se afirma una nueva ejecución de la suite por cambiar capturas. |

## Documento y entrega oficial

| Solicitud del docente | Estado | Qué falta o cómo se comprueba |
|---|---|---|
| Único PDF con portada, introducción, objetivo y desarrollo técnico | CHECK | PDF de 11 páginas preparado; programa **DESARROLLO WEB** incorporado. La falta de cuatro integrantes se evalúa por separado en la fila siguiente. |
| Nombres completos de cuatro integrantes | NO CUMPLE | El usuario solicitó conservar solo a Esteban Villada Henao. No se inventaron compañeros ni una excepción. |
| Capturas legibles y comentadas de Admin, datos, interfaz y operaciones | CHECK | Siete capturas reales de escritorio, ventana 1440×900; figuras explicadas. Un detalle de cabecera de sesión está identificado como tal. |
| Fragmentos relevantes de código, sin copiar todo el proyecto | CHECK | Modelo y autenticación extraídos del código real en el PDF. |
| Conclusiones, aprendizajes, dificultades, pendientes y responsabilidades | PARCIAL | Se documentan aprendizajes, dificultades de estáticos/administrador, alcance futuro y responsabilidad individual. Falta distribución entre cuatro personas porque no hay equipo declarado. |
| Repositorio con código y README de instalación/ejecución | CHECK | https://github.com/wesvh/web-dev-areandina-2027, público; acceso sin autenticación comprobado. |
| Enlace clicable al repositorio en PDF | CHECK | Enlace real incorporado; no se requiere invitación para el código público. |
| Video real demostrativo y participación de cuatro integrantes | FALTA / NO CUMPLE EQUIPO | Hay guion; todavía no hay grabación ni URL. El guion no reemplaza el video ni la participación requerida. |
| Enlace clicable al video dentro del PDF, accesible desde otra sesión | FALTA | Subir video, habilitar consulta, verificar sin depender de la sesión del autor y actualizar el PDF. |
| No incluir contraseñas, tokens, claves privadas o credenciales MySQL | CHECK EN LO REVISADO | `.env` excluido; historial y paquete revisados frente a secretos locales conocidos y patrones comprobados. Ninguna revisión garantiza detectar todo secreto posible. |
| PDF enviado en la plataforma dentro del plazo | FALTA CONFIRMAR | No se ha realizado ni comprobado un envío. Un enlace a GitHub o un ZIP no sustituye el PDF oficial. |

## Impacto de la rúbrica

| Criterio | Puntos del docente | Situación |
|---|---:|---|
| Django, conexión MySQL y modelo de datos | 5 | Implementado y verificado; calificación final depende del docente. |
| Autenticación y administración de entidades | 6 | Implementado y verificado; debe demostrarse en video. |
| Interfaces dinámicas, funcionamiento y evidencias: PDF, repositorio y video | 4 | Parcial mientras falte video y su enlace. No se calcula una nota parcial no definida por la guía. |
| Trabajo en equipo y participación demostrable de cuatro integrantes | 5 | La guía establece **0/5 para entregas individuales**. |

La implementación por sí sola no garantiza 20/20. Si la entrega sigue siendo individual, el máximo aritmético es **15/20**, incluso con puntuación completa en los otros tres criterios. No se presume una excepción aprobada por el docente.

**Sobre una excepción por empresa:** no figura en la guía recibida. Solicitar una autorización escrita al docente sería una posibilidad de consulta, no una excepción existente ni concedida. Para depender de ella habría que recibir una respuesta que autorice el cambio de modalidad y aclare cómo se evaluará el criterio grupal. No se dispone de esa comunicación.

## No se exige todavía

Registro definitivo de votos, control avanzado de duplicados, elegibilidad completa, resultados finales, auditoría avanzada, pruebas de carga y despliegue productivo. Tampoco es obligatorio un panel administrativo propio. Docker y arranque con un comando son facilidades adicionales solicitadas por el usuario, no un reemplazo de los requisitos académicos.

## Orden para cerrar pendientes

1. Revisar la portada ya completada con el programa **DESARROLLO WEB**.
2. Resolver con el docente la entrega individual o incorporar participación real de cuatro integrantes; no cambiar nombres ficticiamente.
3. Grabar siguiendo `reports/GUION_VIDEO.md`, publicar y verificar el enlace desde otra sesión.
4. Insertar enlace del video en el PDF y revisar todos los campos pendientes.
5. Enviar el PDF oficial en la plataforma antes de terminar el plazo indicado; conservar comprobante. La guía exige envío individual de cada integrante del equipo.
