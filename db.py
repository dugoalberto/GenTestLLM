import sqlite3


class DataBase:

    def __init__(self):
        self.conn = sqlite3.connect('identifier.sqlite') #identifier.sqlite
        self.cursor = self.conn.cursor()

    def reset(self):
        self.cursor.execute("DROP TABLE IF EXISTS classes")
        self.cursor.execute("DROP TABLE IF EXISTS methods")
        self.cursor.execute("DROP TABLE IF EXISTS projects")

        self.conn.commit()

    def create_tables(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS projects (
                            projectName TEXT PRIMARY KEY NOT NULL
                        )""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS classes (
                    projectName TEXT NOT NULL,
                    filepath TEXT,
                    classIdentifier TEXT PRIMARY KEY NOT NULL,
                    fullText TEXT NOT NULL
                )""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS methods (
            methodId INTEGER PRIMARY KEY AUTOINCREMENT,
            methodIdentifier TEXT NOT NULL,
            classIdentifier TEXT NOT NULL,
            fullText TEXT,
            FOREIGN KEY (classIdentifier) REFERENCES classes(classIdentifier)
        )""")
        self.conn.commit()

    def insert_project(self, project_name):
        self.cursor.execute("INSERT INTO projects VALUES (?)", (project_name,))
        self.conn.commit()

    def insert_class(self,
                     project_name,
                     filepath,
                     class_identifier,
                     full_text
                     ):
        print("Inserting class: ", class_identifier)
        self.cursor.execute("INSERT INTO classes VALUES (?, ?, ?, ?)",
                            (
                                project_name,
                                filepath,
                                 class_identifier,
                                 full_text
                            ))
        self.conn.commit()


    def insert_method(self, method_identifier, class_identifier, full_text):
        self.cursor.execute("INSERT INTO methods VALUES (NULL, ?, ?, ?)",
                            (method_identifier, class_identifier, full_text))
        self.conn.commit()



    def get_method_id(self, method_identifier, class_identifier):
        self.cursor.execute("SELECT methodId FROM methods WHERE methodIdentifier=? AND classIdentifier =?",
                            (method_identifier, class_identifier))
        result = self.cursor.fetchone()
        if result is None:
            return None
        return result[0]

    def get_class_id(self, class_identifier):
        # return class id or None if class does not exist
        self.cursor.execute("SELECT classIdentifier FROM classes WHERE classIdentifier=?", (class_identifier,))
        result = self.cursor.fetchone()
        if result is None:
            return None
        return result[0]

    def get_method_by_id(self, method_id):
        self.cursor.execute("SELECT * FROM methods WHERE methodId=?", (method_id,))
        result = self.cursor.fetchone()
        if result:
            column_names = [description[0] for description in self.cursor.description]
            result_dict = dict(zip(column_names, result))
            return result_dict
        return None
    def get_class(self, class_identifier):
        self.cursor.execute("SELECT * FROM classes WHERE classIdentifier=?", (class_identifier,))
        result = self.cursor.fetchone()
        if result:
            column_names = [description[0] for description in self.cursor.description]
            result_dict = dict(zip(column_names, result))
            return result_dict
        return None

    def get_filepath_for_method(self, method_id):
        self.cursor.execute("""SELECT filepath
                                FROM methods
                                INNER JOIN classes ON methods.classIdentifier = classes.classIdentifier
                                WHERE methods.methodId = ?""", (method_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None
    def get_filepath_for_class(self, class_identifier):
        self.cursor.execute("""SELECT filepath
                                FROM classes
                                WHERE classes.classIdentifier = ?""", (class_identifier,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None
    def get_class_identifier_for_method(self, method_id):
        self.cursor.execute("SELECT classIdentifier FROM methods WHERE methodId=?", (method_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None

    def get_num_of_methods(self):
        self.cursor.execute("SELECT COUNT(*) FROM methods")
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None

