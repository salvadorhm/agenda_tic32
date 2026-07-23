import sqlite3

class ContactosDB:
    def __init__(self, db_path='sql/agenda.db'):
        self.db_path = db_path

    def _connect(self):
        """Establishes a connection to the SQLite database."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def select_all(self):
        """Selects all records from the contactos table."""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contactos")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def insert_contacto(self, nombre, primer_apellido, segundo_apellido, email, telefono):
        """Inserts a new contact into the contactos table."""
        conn = self._connect()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO contactos(nombre, primer_apellido, segundo_apellido, email, telefono) VALUES (?, ?, ?, ?, ?)",
                (nombre, primer_apellido, segundo_apellido, email, telefono)
            )
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error inserting contact: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()

    def delete_contacto(self, id_contacto):
        """Deletes a contact by ID."""
        conn = self._connect()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM contactos WHERE id_contacto = ?", (id_contacto,))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error deleting contact: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    def update_contacto(self, id_contacto, nombre=None, primer_apellido=None, segundo_apellido=None, email=None, telefono=None):
        """Updates an existing contact."""
        conn = self._connect()
        cursor = conn.cursor()
        updates = []
        params = []

        if nombre is not None:
            updates.append("nombre = ?")
            params.append(nombre)
        if primer_apellido is not None:
            updates.append("primer_apellido = ?")
            params.append(primer_apellido)
        if segundo_apellido is not None:
            updates.append("segundo_apellido = ?")
            params.append(segundo_apellido)
        if email is not None:
            updates.append("email = ?")
            params.append(email)
        if telefono is not None:
            updates.append("telefono = ?")
            params.append(telefono)

        if not updates:
            return False # No changes made
            
        query = f"UPDATE contactos SET {', '.join(updates)} WHERE id_contacto = ?"
        params.append(id_contacto)

        try:
            cursor.execute(query, tuple(params))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error updating contact: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    def search_contacto(self, nombre=None, email=None, telefono=None):
        """Searches for contacts based on partial match in name, email, or phone."""
        try:
            conn = self._connect()
            cursor = conn.cursor()
            where_clauses = []
            params = []

            if nombre is not None:
                where_clauses.append("nombre LIKE ?")
                params.append(f"%{nombre}%")
            if email is not None:
                where_clauses.append("email LIKE ?")
                params.append(f"%{email}%")
            if telefono is not None:
                where_clauses.append("telefono LIKE ?")
                params.append(f"%{telefono}%")

            if where_clauses:
                query = "SELECT * FROM contactos WHERE " + " AND ".join(where_clauses)
                cursor.execute(query, tuple(params))
                rows = cursor.fetchall()
                return rows
            else:
                # Return all if no search criteria provided (optional, depends on desired behavior)
                return self.select_all() 
        except Exception as e:
            print(f"ERROR: {e}")
        finally:
            conn.close()

