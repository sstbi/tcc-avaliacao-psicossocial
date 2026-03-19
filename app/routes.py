from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Empresa

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/empresas")
def listar_empresas():
    empresas = Empresa.query.order_by(Empresa.id.desc()).all()
    return render_template("empresas/listar.html", empresas=empresas)

@main.route("/empresas/nova", methods=["GET", "POST"])
def nova_empresa():
    if request.method == "POST":
        empresa = Empresa(
            razao_social=request.form["razao_social"],
            nome_fantasia=request.form["nome_fantasia"],
            cnpj=request.form["cnpj"],
            email=request.form["email"],
            telefone=request.form["telefone"],
            responsavel=request.form["responsavel"],
            status=request.form["status"]
        )
        db.session.add(empresa)
        db.session.commit()

        flash("Empresa cadastrada com sucesso!", "success")
        return redirect(url_for("main.listar_empresas"))

    return render_template("empresas/nova.html")

@main.route("/empresas/<int:id>/editar", methods=["GET", "POST"])
def editar_empresa(id):
    empresa = Empresa.query.get_or_404(id)

    if request.method == "POST":
        empresa.razao_social = request.form["razao_social"]
        empresa.nome_fantasia = request.form["nome_fantasia"]
        empresa.cnpj = request.form["cnpj"]
        empresa.email = request.form["email"]
        empresa.telefone = request.form["telefone"]
        empresa.responsavel = request.form["responsavel"]
        empresa.status = request.form["status"]

        db.session.commit()

        flash("Empresa atualizada com sucesso!", "success")
        return redirect(url_for("main.listar_empresas"))

    return render_template("empresas/editar.html", empresa=empresa)

@main.route("/empresas/<int:id>/inativar", methods=["POST"])
def inativar_empresa(id):
    empresa = Empresa.query.get_or_404(id)
    empresa.status = "Inativa"
    db.session.commit()

    flash("Empresa inativada com sucesso!", "warning")
    return redirect(url_for("main.listar_empresas"))