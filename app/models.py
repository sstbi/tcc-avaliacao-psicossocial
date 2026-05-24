from datetime import datetime
from app import db


class Empresa(db.Model):
    __tablename__ = "empresas"

    id = db.Column(db.Integer, primary_key=True)
    razao_social = db.Column(db.String(150), nullable=False)
    nome_fantasia = db.Column(db.String(150), nullable=True)
    cnpj = db.Column(db.String(18), unique=True, nullable=False)
    email = db.Column(db.String(120), nullable=True)
    telefone = db.Column(db.String(20), nullable=True)
    responsavel = db.Column(db.String(120), nullable=True)
    status = db.Column(db.String(20), nullable=False, default="Ativa")
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Empresa {self.razao_social}>"


class Unidade(db.Model):
    __tablename__ = "unidades"

    id = db.Column(db.Integer, primary_key=True)
    empresa_id = db.Column(db.Integer, db.ForeignKey("empresas.id"), nullable=False)
    nome = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(20), nullable=False, default="Ativa")
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    empresa = db.relationship("Empresa", backref="unidades")

    def __repr__(self):
        return f"<Unidade {self.nome}>"


class Setor(db.Model):
    __tablename__ = "setores"

    id = db.Column(db.Integer, primary_key=True)
    empresa_id = db.Column(db.Integer, db.ForeignKey("empresas.id"), nullable=False)
    unidade_id = db.Column(db.Integer, db.ForeignKey("unidades.id"), nullable=True)
    nome = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(20), nullable=False, default="Ativa")
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    empresa = db.relationship("Empresa", backref="setores")
    unidade = db.relationship("Unidade", backref="setores")

    def __repr__(self):
        return f"<Setor {self.nome}>"


class Cargo(db.Model):
    __tablename__ = "cargos"

    id = db.Column(db.Integer, primary_key=True)
    empresa_id = db.Column(db.Integer, db.ForeignKey("empresas.id"), nullable=False)
    unidade_id = db.Column(db.Integer, db.ForeignKey("unidades.id"), nullable=True)
    setor_id = db.Column(db.Integer, db.ForeignKey("setores.id"), nullable=True)

    nome = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(20), nullable=False, default="Ativa")
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    empresa = db.relationship("Empresa", backref="cargos")
    unidade = db.relationship("Unidade", backref="cargos")
    setor = db.relationship("Setor", backref="cargos")

    def __repr__(self):
        return f"<Cargo {self.nome}>"


class Questionario(db.Model):
    __tablename__ = "questionarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(20), nullable=False, default="Ativo")
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Questionario {self.nome}>"


class Pergunta(db.Model):
    __tablename__ = "perguntas"

    id = db.Column(db.Integer, primary_key=True)
    questionario_id = db.Column(
        db.Integer,
        db.ForeignKey("questionarios.id"),
        nullable=False
    )

    texto = db.Column(db.Text, nullable=False)

    tipo_resposta = db.Column(
        db.String(50),
        nullable=False,
        default="escala_1_5"
    )

    obrigatoria = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    ordem = db.Column(
        db.Integer,
        nullable=False,
        default=1
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="Ativa"
    )

    criado_em = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    questionario = db.relationship(
        "Questionario",
        backref="perguntas"
    )

    def __repr__(self):
        return f"<Pergunta {self.id}>"


class Aplicacao(db.Model):
    __tablename__ = "aplicacoes"

    id = db.Column(db.Integer, primary_key=True)

    questionario_id = db.Column(
        db.Integer,
        db.ForeignKey("questionarios.id"),
        nullable=False
    )

    empresa_id = db.Column(
        db.Integer,
        db.ForeignKey("empresas.id"),
        nullable=False
    )

    unidade_id = db.Column(
        db.Integer,
        db.ForeignKey("unidades.id"),
        nullable=True
    )

    setor_id = db.Column(
        db.Integer,
        db.ForeignKey("setores.id"),
        nullable=True
    )

    cargo_id = db.Column(
        db.Integer,
        db.ForeignKey("cargos.id"),
        nullable=True
    )

    titulo = db.Column(
        db.String(150),
        nullable=False
    )

    data_inicio = db.Column(
        db.Date,
        nullable=True
    )

    data_fim = db.Column(
        db.Date,
        nullable=True
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="Aberta"
    )

    criado_em = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    questionario = db.relationship(
        "Questionario",
        backref="aplicacoes"
    )

    empresa = db.relationship(
        "Empresa",
        backref="aplicacoes"
    )

    unidade = db.relationship(
        "Unidade",
        backref="aplicacoes"
    )

    setor = db.relationship(
        "Setor",
        backref="aplicacoes"
    )

    cargo = db.relationship(
        "Cargo",
        backref="aplicacoes"
    )

    def __repr__(self):
        return f"<Aplicacao {self.titulo}>"


class Resposta(db.Model):
    __tablename__ = "respostas"

    id = db.Column(db.Integer, primary_key=True)

    aplicacao_id = db.Column(
        db.Integer,
        db.ForeignKey("aplicacoes.id"),
        nullable=False
    )

    pergunta_id = db.Column(
        db.Integer,
        db.ForeignKey("perguntas.id"),
        nullable=False
    )

    valor_resposta = db.Column(
        db.Text,
        nullable=False
    )

    criado_em = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    aplicacao = db.relationship(
        "Aplicacao",
        backref="respostas"
    )

    pergunta = db.relationship(
        "Pergunta",
        backref="respostas"
    )

    def __repr__(self):
        return f"<Resposta {self.id}>"