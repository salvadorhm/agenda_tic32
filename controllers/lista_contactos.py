import web
import sqlite3

render = web.template.render('views', base='layout')

class ListaContactos:

    def obtenerContactos(self):
        try:
            # Conecta a la base de datos
            conn = sqlite3.connect('sql/agenda.db')
            cursor = conn.cursor()
            # Consulta los registros de la tabla contactos
            query = "SELECT * FROM contactos;"
            cursor.execute(query)
            # Crea un array vacio para almacenar los registros
            contactos = []
            # Almacena cada registro en un diccionario
            for row in cursor.fetchall():
                contacto = {
                    'id_contacto': row[0],
                    'nombre': row[1],
                    'primer_apellido': row[2],
                    'segundo_apellido': row[3],
                    'email': row[4],
                    'telefono': row[5]
                }
                # Agrega el diccionario creado al array
                contactos.append(contacto)

            # Cierra la conexión a la base de datos
            conn.close()

            return contactos
        except sqlite3.Error as error:
            print(f"ERROR 100: {error.args}")
            return []
        except Exception as error:
            print(f"ERROR 101: {error.args}")
            return []
        finally:
            conn.close()


    def GET(self):
        contactos = self.obtenerContactos()
        print(contactos)
        return render.lista_contactos(contactos)
