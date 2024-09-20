import os

from Report import Report
from model.Livro import Livro


class Menu:
    def __init__(self, livro_repository, connection):
        self.connection = connection
        self.livro_repository = livro_repository
        self.report = Report(self.livro_repository)

    def start_livraria(self):
        self.connection.create_livro_table()

    def display(self):
        while True:
            print("\n--- Menu ---")
            print("1. Adicionar um novo Livro")
            print("2. Exibir todos os Livros")
            print("3. Atualizar o preço de um Livro")
            print("4. Remover um Livro")
            print("5. Buscar Livros por autor")
            print("6. Exportar Relatório")
            print("7. Importar Dados")
            print("8. Sair")

            escolha = input("Selecione uma opção (1-8): ")

            if escolha == '1':
                self.adicionar_livro()
            elif escolha == '2':
                self.exibir_todos_livros()
            elif escolha == '3':
                self.atualizar_preco_livro()
            elif escolha == '4':
                self.remover_livro()
            elif escolha == '5':
                self.buscar_livros_por_autor()
            elif escolha == '6':
                self.exportar_relatorio()
            elif escolha == '7':
                self.importar_dados()
            elif escolha == '8':
                print("Saindo...")
                self.connection.close()
                break
            else:
                print("Opção inválida. Por favor, tente novamente.")

    def adicionar_livro(self):
        titulo = input("Digite o título: ")
        autor = input("Digite o autor: ")
        ano_publicacao = int(input("Digite o ano de publicação: "))
        preco = float(input("Digite o preço: "))
        livro = Livro(titulo=titulo, autor=autor, ano_publicacao=ano_publicacao, preco=preco)
        self.livro_repository.add(livro)
        print(f"Livro '{livro.titulo}' adicionado com sucesso!")

    def exibir_todos_livros(self):
        todos_livros = self.livro_repository.get_all()
        if todos_livros:
            print("Livros cadastrados:")
            for livro in todos_livros:
                print(livro)
        else:
            print("Nenhum livro encontrado.")

    def atualizar_preco_livro(self):
        livro_id = int(input("Digite o ID do livro para atualizar: "))
        novo_preco = float(input("Digite o novo preço: "))
        livro = self.livro_repository.get_by_id(livro_id)
        if livro:
            self.livro_repository.update_price(livro, novo_preco)
            print(f"Preço do livro '{livro.titulo}' atualizado para R$ {novo_preco}.")
        else:
            print("Livro não encontrado.")

    def remover_livro(self):
        livro_id = int(input("Digite o ID do livro para remover: "))
        livro = self.livro_repository.get_by_id(livro_id)
        if livro:
            self.livro_repository.delete(livro)
            print(f"Livro '{livro.titulo}' removido com sucesso.")
        else:
            print("Livro não encontrado.")

    def buscar_livros_por_autor(self):
        autor = input("Digite o nome do autor: ")
        livros_por_autor = self.livro_repository.get_by_author(autor)
        if livros_por_autor:
            print(f"Livros de {autor}:")
            for livro in livros_por_autor:
                print(livro)
        else:
            print(f"Nenhum livro encontrado do autor '{autor}'.")

    def exportar_relatorio(self):
        print("\n--- Exportar Relatório ---")
        print("1. Exportar para CSV")
        print("2. Exportar para PDF")
        print("3. Exportar para HTML")

        escolha = input("Selecione uma opção (1-2): ")

        if escolha == '1':
            self.report.generate_csv()
        elif escolha == '2':
            self.report.generate_pdf()
        elif escolha == '3':
            self.report.generate_html()
        else:
            print("Opção inválida. Por favor, tente novamente.")

    def importar_dados(self):
        exports_dir = 'exports'
        files = [f for f in os.listdir(exports_dir) if f.endswith(('.csv', '.pdf'))]

        if not files:
            print("Nenhum arquivo encontrado na pasta 'exports'.")
            return

        print("\n--- Importar Dados ---")
        for index, file in enumerate(files, start=1):
            print(f"{index}. {file}")

        escolha = int(input("Selecione o número do arquivo a ser importado: ")) - 1
        if escolha < 0 or escolha >= len(files):
            print("Opção inválida. Por favor, tente novamente.")
            return

        selected_file = os.path.join(exports_dir, files[escolha])
        if selected_file.endswith('.csv'):
            self.report.import_csv(selected_file)
        elif selected_file.endswith('.pdf'):
            self.report.import_pdf(selected_file)
