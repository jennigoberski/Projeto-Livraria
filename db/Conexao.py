import sqlite3
import os
import shutil
from datetime import datetime


class Conexao:
    def __init__(self, db_name='data/livraria.db'):
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        self.create_data_directory()
        self.connect()

    def create_data_directory(self):
        os.makedirs('data', exist_ok=True)

    def connect(self):
        if not os.path.exists(self.db_name):
            print(f"Database {self.db_name} não existe. Criando uma nova.")
        else:
            print(f"Conectando em uma base existente: {self.db_name}")

        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        print("Conexão deu boa.")

    def close(self):
        if self.connection:
            self.connection.close()
            print("Conexão fechada.")

    def execute_query(self, query, params=None):
        try:
            self.backup_database()
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            print("Query executada.")
        except sqlite3.Error as e:
            print(f"Erro na query: {e}")

    def fetch_all(self):
        return self.cursor.fetchall()

    def create_livro_table(self):
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS Livro (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            ano_publicacao INTEGER,
            preco REAL
        );
        '''
        self.execute_query(create_table_query)

    def backup_database(self):
        backup_directory = 'backup'
        os.makedirs(backup_directory, exist_ok=True)

        # Create the new backup file
        backup_file = os.path.join(backup_directory, f"backup_livraria_{datetime.now().strftime('%Y-%m-%d')}.db")
        shutil.copy(self.db_name, backup_file)
        print(f"Backup do banco de dados criado: {backup_file}")

        # Manage backup files: keep only the last 5 backups
        self.manage_backups(backup_directory)

    def manage_backups(self, backup_directory):
        backups = sorted(
            [f for f in os.listdir(backup_directory) if f.startswith('backup_livraria')],
            key=lambda x: os.path.getmtime(os.path.join(backup_directory, x))
        )

        while len(backups) > 5:
            oldest_backup = backups.pop(0)
            os.remove(os.path.join(backup_directory, oldest_backup))
            print(f"Backup removido: {oldest_backup}")
