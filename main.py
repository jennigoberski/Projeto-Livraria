from Menu import Menu
from db.Conexao import Conexao
from db.Repository import Repository

if __name__ == "__main__":
    connection = Conexao()
    connection.create_livro_table()
    livro_repository = Repository(connection)

    menu = Menu(livro_repository, connection)
    menu.display()

    connection.close()

