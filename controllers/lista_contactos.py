import web

render = web.template.render('views')

class ListaContactos:
    def GET(self):
        return render.lista_contactos()
