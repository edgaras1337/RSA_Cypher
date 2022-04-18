import mysql.connector


class Database:

    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="rootroot",
        )
        self.db_name = "rsa_db"
        self.cipher_table = self.CipherTextTable()
        self.public_key_table = self.PublicKeyTable()

        self.connect()
        self.create_tables()

    def connect(self):
        cursor = self.db.cursor()

        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.db_name}")
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="rootroot",
            database=self.db_name
        )

    def create_tables(self):
        cursor = self.db.cursor()

        cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {self.cipher_table.table_name} (
                    {self.cipher_table.id} INT UNSIGNED AUTO_INCREMENT NOT NULL,
                    {self.cipher_table.text} TEXT NOT NULL,
                    PRIMARY KEY ({self.cipher_table.id})
                )
            ''')
        cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {self.public_key_table.table_name} (
                    {self.public_key_table.cipher_text_id} INT UNSIGNED AUTO_INCREMENT NOT NULL,
                    {self.public_key_table.e} INT UNSIGNED NOT NULL,
                    {self.public_key_table.n} INT UNSIGNED NOT NULL,
                    PRIMARY KEY ({self.public_key_table.cipher_text_id}),
                    FOREIGN KEY ({self.public_key_table.cipher_text_id}) 
                    REFERENCES {self.cipher_table.table_name}({self.cipher_table.id})
                )
            ''')
        cursor.close()

    def add_cipher_text_and_key(self, text, e, n):
        cursor = self.db.cursor()

        sql_insert_text = f'''
            INSERT INTO {self.cipher_table.table_name}
            ({self.cipher_table.text})
            VALUES ('{text}')
        '''
        cursor.execute(sql_insert_text)
        self.db.commit()

        sql_select_latest_id = f'''
            SELECT {self.cipher_table.id} FROM
            {self.cipher_table.table_name}
            ORDER BY {self.cipher_table.id}
            DESC LIMIT 1
        '''
        cursor.execute(sql_select_latest_id)

        result = cursor.fetchone()
        latest_id = result[0]

        sql_insert_public_key = f'''
            INSERT INTO {self.public_key_table.table_name}
            VALUES ({latest_id}, {e}, {n})
        '''
        cursor.execute(sql_insert_public_key)
        self.db.commit()
        cursor.close()

    def select_latest_cipher(self):
        cursor = self.db.cursor()
        query = f'''
            SELECT {self.cipher_table.text}, {self.public_key_table.e}, {self.public_key_table.n} 
            FROM {self.cipher_table.table_name}
            INNER JOIN {self.public_key_table.table_name} ON
            {self.cipher_table.id} = {self.public_key_table.cipher_text_id}
            ORDER BY {self.cipher_table.id}
            DESC LIMIT 1
        '''
        cursor.execute(query)

        result = cursor.fetchone()
        cursor.close()

        return result

    class CipherTextTable:
        def __init__(self):
            self.table_name = "cipher_text"
            self.id = "id"
            self.text = "text"

    class PublicKeyTable:
        def __init__(self):
            self.table_name = "public_key"
            self.cipher_text_id = "cipher_text_id"
            self.e = "e"
            self.n = "n"