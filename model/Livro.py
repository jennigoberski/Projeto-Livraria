class Livro:
    def __init__(self, id=None, titulo='', autor='', ano_publicacao=0, preco=0.0):
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.ano_publicacao = ano_publicacao
        self.preco = preco

    def __repr__(self):
        return f"Livro(id={self.id}, titulo='{self.titulo}', autor='{self.autor}', ano_publicacao={self.ano_publicacao}, preco={self.preco})"
