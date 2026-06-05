import csv
from app import create_app, db
from app.models import Questionario, Pergunta

ARQUIVO_CSV = "copsoq_pt_2024.csv"

app = create_app()

with app.app_context():
    questionario = Questionario.query.filter_by(
        nome="COPSOQ III - Versão Curta Portuguesa 2024"
    ).first()

    if not questionario:
        questionario = Questionario(
            nome="COPSOQ III - Versão Curta Portuguesa 2024",
            descricao="Versão curta portuguesa do COPSOQ III, conforme validação publicada em 2024.",
            status="Ativo"
        )
        db.session.add(questionario)
        db.session.commit()

    with open(ARQUIVO_CSV, "r", encoding="latin-1", newline="") as arquivo:
        linhas_corrigidas = []

        for linha in arquivo:
            linha = linha.strip()

            if linha.startswith('"') and linha.endswith('"'):
                linha = linha[1:-1]

            linhas_corrigidas.append(linha)

        leitor = csv.DictReader(linhas_corrigidas, delimiter=";")

        print("Cabeçalho encontrado:", leitor.fieldnames)

        for linha in leitor:
            ordem = int(linha["ordem"])
            dominio = linha["dominio"].strip()
            dimensao = linha["dimensao"].strip()
            texto = linha["texto"].strip()

            texto_final = f"[{dominio} | {dimensao}] {texto}"

            existe = Pergunta.query.filter_by(
                questionario_id=questionario.id,
                ordem=ordem
            ).first()

            if not existe:
                pergunta = Pergunta(
                    questionario_id=questionario.id,
                    texto=texto_final,
                    tipo_resposta="escala_1_5",
                    obrigatoria=True,
                    ordem=ordem,
                    status="Ativa"
                )
                db.session.add(pergunta)

    db.session.commit()

    print("Questionário COPSOQ III - Versão Curta Portuguesa 2024 importado com sucesso!")