from db import Conexao
from model.Livro import Livro

class Repository:
    def __init__(self, connection: Conexao):
        self.connection = connection

    def add(self, livro: Livro):
        query = '''INSERT INTO Livro (titulo, autor, ano_publicacao, preco) 
                   VALUES (?, ?, ?, ?)'''
        params = (livro.titulo, livro.autor, livro.ano_publicacao, livro.preco)
        self.connection.execute_query(query, params)
        livro.id = self.connection.cursor.lastrowid

    def get_all(self):
        query = 'SELECT * FROM Livro'
        self.connection.execute_query(query)
        rows = self.connection.fetch_all()
        return [Livro(id=row[0], titulo=row[1], autor=row[2], ano_publicacao=row[3], preco=row[4]) for row in rows]

    def update_price(self, livro: Livro, new_price: float):
        query = '''UPDATE Livro SET preco=? WHERE id=?'''
        params = (new_price, livro.id)
        self.connection.execute_query(query, params)
        livro.preco = new_price

    def delete(self, livro: Livro):
        if livro.id is not None:
            query = 'DELETE FROM Livro WHERE id=?'
            self.connection.execute_query(query, (livro.id,))
            livro.id = None

    def get_by_id(self, livro_id: int):
        query = 'SELECT * FROM Livro WHERE id=?'
        self.connection.execute_query(query, (livro_id,))
        row = self.connection.fetch_all()
        if row:
            return Livro(id=row[0][0], titulo=row[0][1], autor=row[0][2], ano_publicacao=row[0][3], preco=row[0][4])
        return None

    def get_by_author(self, autor: str):
        query = 'SELECT * FROM Livro WHERE autor=?'
        self.connection.execute_query(query, (autor,))
        rows = self.connection.fetch_all()
        return [Livro(id=row[0], titulo=row[1], autor=row[2], ano_publicacao=row[3], preco=row[4]) for row in rows]
