import web
import sqlite3
from models.contactos import ContactosDB as ContactosDB

render = web.template.render('views', base='layout')

class ListaContactos:

    def __init__(self) -> None:
        self.contactos = ContactosDB()

    def GET(self):
        contactos = self.contactos.select_all()
        # print(contactos)
        return render.lista_contactos(contactos) # type: ignore
