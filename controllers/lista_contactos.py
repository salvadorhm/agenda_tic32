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
            resultado = cursor.execute("SELECT * FROM contactos;")
            print(f"RESULTADO: {resultado}")
            
            # Almacena los resultados en un diccionario
            contactos = []
            for row in resultado.fetchall():
                contacto = {
                    'id_contacto': row[0],
                    'nombre': row[1],
                    'primer_apellido': row[2],
                    'segundo_apellido': row[3],
                    'email': row[4],
                    'telefono': row[5]
                }
                contactos[row[0]] = contacto
        
            # Cierra la conexión a la base de datos
            conn.close()

            return contactos
        except sqlite3.Error as error:
            print(f"ERROR 100: {error.args}")
            return []
        except Exception as error:
            print(f"ERROR 101: {error.args}")
            return []



    def GET(self):
        print(self.obtenerContactos())
        return render.lista_contactos()
