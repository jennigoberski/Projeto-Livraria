import csv
import os
import re

import pandas as pd
from PyPDF2 import PdfReader
from fpdf import FPDF
from jinja2 import Environment, FileSystemLoader

from model.Livro import Livro


class Report:
    def __init__(self, livro_repository):
        self.livro_repository = livro_repository
        self.export_directory = 'exports'
        os.makedirs(self.export_directory, exist_ok=True)

    def generate_csv(self):
        livros = self.livro_repository.get_all()
        csv_file = os.path.join(self.export_directory, 'dados_livraria.csv')
        df = pd.DataFrame([livro.__dict__ for livro in livros])
        df.to_csv(csv_file, index=False)
        print(f"CSV exportado com sucesso: {csv_file}")

    def generate_pdf(self):
        livros = self.livro_repository.get_all()
        pdf_file = os.path.join(self.export_directory, 'dados_livraria.pdf')
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        for livro in livros:
            pdf.cell(200, 10, txt=str(livro), ln=True)

        pdf.output(pdf_file)
        print(f"PDF exportado com sucesso: {pdf_file}")

    def generate_html(self):
        livros = self.livro_repository.get_all()
        html_file = os.path.join(self.export_directory, 'dados_livraria.html')

        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template('livros_template.html')

        with open(html_file, 'w') as f:
            f.write(template.render(livros=livros))

        print(f"HTML exportado com sucesso: {html_file}")

    def import_csv(self, file_path):
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                if len(row) != 5:
                    continue

                _, titulo, autor, ano_publicacao, preco = row  # Ignore the ID
                ano_publicacao = int(ano_publicacao)
                preco = float(preco)

                existing_books = self.livro_repository.get_by_author(autor)
                if not any(livro.titulo == titulo for livro in existing_books):
                    livro = Livro(titulo=titulo, autor=autor, ano_publicacao=ano_publicacao, preco=preco)
                    self.livro_repository.add(livro)
                    print(f"Livro '{titulo}' adicionado com sucesso a partir do CSV.")
                else:
                    print(f"Livro '{titulo}' já existe e não será adicionado.")

    def import_pdf(self, file_path):
        reader = PdfReader(file_path)
        for page in reader.pages:
            text = page.extract_text()
            lines = text.split('\n')
            for line in lines:
                if line.strip():
                    match = re.match(
                        r"Livro\(id=(\d+), titulo='([^']*)', autor='([^']*)', ano_publicacao=(\d+), preco=(\d+\.\d+)\)",
                        line.strip()
                    )
                    if match:
                        livro_id = int(match.group(1))
                        titulo = match.group(2).strip()
                        autor = match.group(3).strip()
                        ano_publicacao = int(match.group(4))
                        preco = float(match.group(5))

                        existing_books = self.livro_repository.get_by_author(autor)
                        if not any(livro.titulo == titulo for livro in existing_books):
                            livro = Livro(titulo=titulo, autor=autor, ano_publicacao=ano_publicacao, preco=preco)
                            self.livro_repository.add(livro)
                            print(f"Livro '{titulo}' adicionado com sucesso a partir do PDF.")
                        else:
                            print(f"Livro '{titulo}' já existe e não será adicionado.")
                    else:
                        print(f"Linha ignorada, não corresponde ao formato esperado: '{line}'")
