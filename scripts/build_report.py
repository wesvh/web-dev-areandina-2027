"""Build a concise APA report from actual browser captures and test evidence."""
from datetime import datetime
from html import escape
from pathlib import Path
from zoneinfo import ZoneInfo
import json
import re
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, PageBreak,
                               Table, TableStyle, Preformatted, Flowable)

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'evidence'
OUT = ROOT / 'reports/Entrega_2_Vallenato_2027_APA.pdf'
OUT.parent.mkdir(exist_ok=True)
verification = json.loads((EVIDENCE/'verification.json').read_text())
restart = json.loads((EVIDENCE/'restart.json').read_text())
mobile = json.loads((EVIDENCE/'mobile.json').read_text())
assert verification['passed'] and restart['passed']
test_output = next(c['output'] for c in verification['checks'] if c['name'].startswith('Full Django'))
test_count = int(re.search(r'Ran (\d+) tests', test_output).group(1))
FONT = Path('/System/Library/Fonts/Supplemental')
for name,file in [('TNR','Times New Roman.ttf'),('TNRB','Times New Roman Bold.ttf'),('TNRI','Times New Roman Italic.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(FONT/file)))
pdfmetrics.registerFontFamily('TNR',normal='TNR',bold='TNRB',italic='TNRI',boldItalic='TNRB')
body = ParagraphStyle('body',fontName='TNR',fontSize=12,leading=24,firstLineIndent=36)
plain = ParagraphStyle('plain',parent=body,firstLineIndent=0)
center = ParagraphStyle('center',parent=plain,alignment=TA_CENTER)
heading = ParagraphStyle('heading',parent=center,fontName='TNRB',keepWithNext=True)
caption = ParagraphStyle('caption',parent=plain,fontName='TNRB',keepWithNext=True)
title = ParagraphStyle('title',parent=plain,fontName='TNRI',keepWithNext=True)
cell = ParagraphStyle('cell',fontName='TNR',fontSize=10,leading=13)
head = ParagraphStyle('head',parent=cell,fontName='TNRB')
reference = ParagraphStyle('reference',parent=body,leftIndent=36,firstLineIndent=-36,splitLongWords=True)
code_style = ParagraphStyle('code',fontName='Courier',fontSize=8.5,leading=11)
W = 468
story=[]
table_number=figure_number=0

def paragraph(text, style=body):
    story.append(Paragraph(text,style))
def section(text,new_page=True):
    if new_page:
        story.append(PageBreak())
    paragraph(text,heading)
def table(name,headers,rows,widths):
    global table_number
    table_number+=1
    paragraph(f'Tabla {table_number}',caption)
    paragraph(name,title)
    data=[[Paragraph(escape(h),head) for h in headers]]
    data += [[Paragraph(escape(str(v)),cell) for v in row] for row in rows]
    t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('LEFTPADDING',(0,0),(-1,-1),4),('RIGHTPADDING',(0,0),(-1,-1),4),
        ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),
        ('LINEABOVE',(0,0),(-1,0),.75,colors.black),
        ('LINEBELOW',(0,0),(-1,0),.75,colors.black),
        ('LINEBELOW',(0,-1),(-1,-1),.75,colors.black)]))
    story.append(t)

class CaptureFragment(Flowable):
    """Clip a source capture in PDF layout without editing its pixel content."""
    def __init__(self,path,top=0,height=None,max_width=224,max_height=470):
        super().__init__()
        self.reader=ImageReader(str(path))
        self.source_width,self.source_height=self.reader.getSize()
        self.top=top
        self.crop_height=height or self.source_height-top
        self.scale=min(max_width/self.source_width,max_height/self.crop_height)
        self.width=self.source_width*self.scale
        self.height=self.crop_height*self.scale
    def draw(self):
        c=self.canv
        c.saveState()
        p=c.beginPath();p.rect(0,0,self.width,self.height)
        c.clipPath(p,stroke=0)
        c.drawImage(self.reader,0,(self.top+self.crop_height-self.source_height)*self.scale,
                    width=self.source_width*self.scale,height=self.source_height*self.scale)
        c.restoreState()

def figure(name,left,right,note):
    global figure_number
    figure_number+=1
    paragraph(f'Figura {figure_number}',caption)
    paragraph(name,title)
    t=Table([[left,right]],colWidths=[234,234],hAlign='LEFT')
    t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),4),
                           ('RIGHTPADDING',(0,0),(-1,-1),4)]))
    story.append(t)
    paragraph('<i>Nota.</i> '+note,plain)

def footer(canvas,doc):
    canvas.setFont('TNR',12)
    canvas.drawRightString(540,750,str(doc.page))

story.append(Spacer(1,96))
paragraph('Desarrollo inicial del sistema de votaciones<br/>Festival de la Leyenda Vallenata 2027',heading)
paragraph('Entrega 2',center)
story.append(Spacer(1,24))
paragraph('Esteban Villada Henao',center)
paragraph('Fundación Universitaria del Área Andina',center)
paragraph('Programa académico: pendiente de confirmar',center)
story.append(Spacer(1,24))
paragraph('Desarrollo Web',center)
paragraph('Docente: DEIVYS MORALES URIBE',center)
paragraph('26 de octubre de 2026',center)

section('Introducción y objetivo')
paragraph('La segunda entrega convierte el diseño inicial en una aplicación Django MVT conectada a MySQL. Implementa autenticación, administración del catálogo y consulta pública dinámica. Las ediciones, categorías, votaciones y opciones son datos ficticios; la emisión de votos corresponde a etapas posteriores (<i>Entrega 2 - Festival Vallenato 2027</i>, 2026).')
paragraph('<b>Objetivo:</b> construir y verificar una base funcional, persistente y ejecutable con un comando, manteniendo separadas la presentación, las reglas y el almacenamiento.')
table('Estructura y relaciones implementadas',['Componente','Responsabilidad'],[
    ['config','Configuración MySQL, rutas raíz y WSGI.'],
    ['accounts','Registro, inicio y cierre de sesión mediante Django User.'],
    ['catalog','Modelos, vistas ORM, administración y migración 0001_initial.'],
    ['templates / static','Interfaz responsive en español y estilos locales.'],
    ['Edición → Categoría → Votación → Opción','Claves foráneas de uno a muchos; nombres únicos por contexto.']
],[140,328])
paragraph('Las vistas consultan el ORM y entregan objetos a plantillas. Django Admin permite modificar los datos sin construir otro panel. Los borradores no se muestran públicamente ni se recuperan por acceso directo a su URL.')

section('Desarrollo técnico')
paragraph('MySQL utiliza utf8mb4 y modo estricto. Django conserva validadores y hash de contraseñas, sesiones y protección CSRF. El registro público no concede privilegios; cerrar sesión exige POST. Las redirecciones de acceso se limitan a destinos seguros (Django Software Foundation, s. f.-a, s. f.-c).')
paragraph('Fragmentos del código implementado',heading)
models_source=(ROOT/'catalog/models.py').read_text()
auth_source=(ROOT/'accounts/views.py').read_text()
snippet=('# catalog/models.py\n'+
         models_source[models_source.index('class Category'):models_source.index('class Poll')].strip()+
         '\n\n# accounts/views.py\n'+auth_source[auth_source.index('class FestivalLogoutView'):].strip())
story.append(Preformatted(snippet,code_style,maxLineLength=88,splitChars=' ,',newLineChars='    '))
paragraph('Las migraciones versionadas crean tablas y restricciones. El arranque aplica migrate, crea datos de prueba de forma condicional y recopila estáticos. No genera migraciones nuevas ni borra datos al reiniciar (Django Software Foundation, s. f.-b).')

section('Ejecución y pruebas')
paragraph('Con Docker y Compose instalados, ejecutar <b>./start.sh</b> desde la carpeta del proyecto. El comando genera secretos locales si faltan, construye imágenes y espera MySQL antes de iniciar Django. Aplicación: <link href="http://localhost:8000/">http://localhost:8000/</link>. La primera descarga requiere internet (Docker Inc., s. f.).')
table('Comprobaciones observadas',['Prueba / procedimiento','Resultado'],[
    ['python manage.py test --noinput',f'{test_count} pruebas aprobadas con MySQL real; base aislada test_festival.'],
    ['check; makemigrations --check --dry-run','Sin errores de configuración; modelos y migraciones coinciden.'],
    ['showmigrations','Migraciones de catálogo, autenticación, Admin y sesiones aplicadas.'],
    ['SELECT VERSION(); consultas ORM','MySQL 8.4.13; dos ediciones y catálogo persistido.'],
    ['Registro, login, logout y Admin en navegador','Cuenta ficticia creada; sesión iniciada/cerrada; categoría guardada.'],
    ['Detener web y ejecutar ./start.sh','Mismos registros y categoría de evidencia con ID 3: persistencia aprobada.'],
    ['Inspección DOM móvil',f'Ancho efectivo {mobile["viewport"]} px; sin desbordamiento horizontal.']
],[218,250])
paragraph('El contenedor web no recibe la contraseña root de MySQL y se ejecuta sin root. La base no publica puertos; la aplicación se enlaza a localhost. Los secretos permanecen en .env, excluido del repositorio, del ZIP y de las capturas. No es un despliegue productivo.')

section('Evidencia: consulta de ediciones')
figure('Catálogo público con ediciones almacenadas en MySQL',
       CaptureFragment(EVIDENCE/'01-ediciones.jpg',0,600),
       CaptureFragment(EVIDENCE/'01-ediciones.jpg',600),
       'Fragmentos superior e inferior de una misma captura real. Se observan las ediciones 2027 y 2028 y el aviso de datos ficticios. El contenido proviene del ORM, no de arreglos estáticos.')

section('Evidencia: votación y opciones')
figure('Recorrido público hasta las opciones de una votación',
       CaptureFragment(EVIDENCE/'02-opciones-mysql.jpg',0,600),
       CaptureFragment(EVIDENCE/'02-opciones-mysql.jpg',600),
       'Dos fragmentos de la misma pantalla. La ruta conserva edición y categoría; se muestran estado, descripción y opciones relacionadas. La interfaz declara que todavía no registra votos.')

section('Evidencia: autenticación')
figure('Registro y sesión de un usuario sin permisos administrativos',
       CaptureFragment(EVIDENCE/'03-registro.jpg',180,950),
       CaptureFragment(EVIDENCE/'04-sesion-iniciada.jpg',0,340),
       'Izquierda: formulario real con validadores de contraseña. Derecha: sesión de visitante_evidencia iniciada tras el registro y login; no aparece el enlace administrativo. La prueba posterior de logout devolvió los enlaces de acceso. No se muestran contraseñas.')

section('Evidencia: administración')
figure('Modelos administrables y confirmación de guardado',
       CaptureFragment(EVIDENCE/'05-admin.jpg'),
       CaptureFragment(EVIDENCE/'06-admin-guardado.jpg',95,690),
       'Izquierda: Django Admin reconoce ediciones, categorías, votaciones y opciones. Derecha: mensaje de guardado y nueva categoría ficticia vinculada a 2027. El cambio se realizó mediante el formulario, no modificando la base manualmente.')

section('Evidencia: visualización dinámica y persistencia')
figure('La categoría registrada en Admin aparece en la interfaz pública',
       CaptureFragment(EVIDENCE/'07-categoria-publica.jpg',0,600),
       CaptureFragment(EVIDENCE/'07-categoria-publica.jpg',600),
       'Fragmentos de la consulta pública de 2027. Aparece Evidencia de persistencia - ficticia, creada desde Admin. Después de detener web y arrancar con ./start.sh se conservaron tres categorías, cuatro votaciones y cuatro opciones; la categoría mantuvo ID 3.')

section('Repositorio, video y conclusiones')
paragraph('<b>Repositorio público:</b> <link href="https://github.com/wesvh/web-dev-areandina-2027">https://github.com/wesvh/web-dev-areandina-2027</link>. Código, migraciones, pruebas y evidencias publicados en la rama master mediante SSH de la cuenta personal wesvh. La publicación pública fue autorizada expresamente el 26 de octubre de 2026. El README explica la ejecución local con Docker; publicar el código no implica alojar la aplicación en internet.')
paragraph('<b>Video:</b> enlace pendiente de proporcionar. Se incluye un guion de grabación en el proyecto; no se inventó una demostración grabada ni la participación de otras personas. Antes del envío, publicar el video con permisos para el docente y reemplazar este pendiente.')
paragraph('Se logró una base ejecutable con relaciones persistentes, autenticación nativa, administración y consulta dinámica. Las pruebas y el reinicio respaldan el alcance funcional; no prueban seguridad productiva, carga ni reglas definitivas de votación.')
paragraph('<b>Responsabilidades:</b> Esteban Villada Henao figura como único autor, responsable de revisar y justificar análisis, código, pruebas y evidencias. Se utilizó IA como apoyo técnico. La guía exige cuatro integrantes y establece 0/5 en el criterio de trabajo grupal para entregas individuales; esta presentación no declara una excepción aprobada.')
paragraph('<b>Antes de entregar:</b> completar programa académico y enlace del video; verificar permisos del video desde otra sesión. El repositorio es público y no requiere invitación para consultar el código. Registro definitivo de votos, resultados, elegibilidad avanzada y producción quedan para próximas fases.')

section('Referencias')
refs=[
 ('Django Software Foundation. (s. f.-a). <i>Databases</i>.','https://docs.djangoproject.com/en/5.2/ref/databases/'),
 ('Django Software Foundation. (s. f.-b). <i>Migrations</i>.','https://docs.djangoproject.com/en/5.2/topics/migrations/'),
 ('Django Software Foundation. (s. f.-c). <i>Using the Django authentication system</i>.','https://docs.djangoproject.com/en/5.2/topics/auth/default/'),
 ('Docker Inc. (s. f.). <i>Control startup and shutdown order in Compose</i>.','https://docs.docker.com/compose/how-tos/startup-order/'),
 ('<i>Entrega 2 - Festival Vallenato 2027</i>. (2026). [Guía académica suministrada por el docente]. Fundación Universitaria del Área Andina.','')]
for text,url in refs:
    paragraph(text+(' <link href="'+url+'">'+url+'</link>' if url else ''),reference)
SimpleDocTemplate(str(OUT),pagesize=letter,leftMargin=72,rightMargin=72,topMargin=72,bottomMargin=72,
                  title='Entrega 2 - Festival Vallenato 2027',author='Esteban Villada Henao').build(
                      story,onFirstPage=footer,onLaterPages=footer)
print(OUT)
