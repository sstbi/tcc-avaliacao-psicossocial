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