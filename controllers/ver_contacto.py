import web
import sqlite3

render = web.template.render('views', base='layout')

class VerContacto:

    def GET(self):

        return render.ver_contacto()