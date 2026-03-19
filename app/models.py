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