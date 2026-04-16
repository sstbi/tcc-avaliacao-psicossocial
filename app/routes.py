from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Empresa, Unidade, Setor

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")


# =========================
# EMPRESAS
# =========================
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


# =========================
# UNIDADES
# =========================
@main.route("/unidades")
def listar_unidades():
    unidades = Unidade.query.order_by(Unidade.id.desc()).all()
    return render_template("unidades/listar.html", unidades=unidades)

@main.route("/unidades/nova", methods=["GET", "POST"])
def nova_unidade():
    empresas = Empresa.query.filter_by(status="Ativa").order_by(Empresa.razao_social.asc()).all()

    if request.method == "POST":
        unidade = Unidade(
            empresa_id=request.form["empresa_id"],
            nome=request.form["nome"],
            descricao=request.form["descricao"],
            status=request.form["status"]
        )
        db.session.add(unidade)
        db.session.commit()

        flash("Unidade cadastrada com sucesso!", "success")
        return redirect(url_for("main.listar_unidades"))

    return render_template("unidades/nova.html", empresas=empresas)

@main.route("/unidades/<int:id>/editar", methods=["GET", "POST"])
def editar_unidade(id):
    unidade = Unidade.query.get_or_404(id)
    empresas = Empresa.query.filter_by(status="Ativa").order_by(Empresa.razao_social.asc()).all()

    if request.method == "POST":
        unidade.empresa_id = request.form["empresa_id"]
        unidade.nome = request.form["nome"]
        unidade.descricao = request.form["descricao"]
        unidade.status = request.form["status"]

        db.session.commit()

        flash("Unidade atualizada com sucesso!", "success")
        return redirect(url_for("main.listar_unidades"))

    return render_template("unidades/editar.html", unidade=unidade, empresas=empresas)

@main.route("/unidades/<int:id>/inativar", methods=["POST"])
def inativar_unidade(id):
    unidade = Unidade.query.get_or_404(id)
    unidade.status = "Inativa"
    db.session.commit()

    flash("Unidade inativada com sucesso!", "warning")
    return redirect(url_for("main.listar_unidades"))


# =========================
# SETORES
# =========================
@main.route("/setores")
def listar_setores():
    setores = Setor.query.order_by(Setor.id.desc()).all()
    return render_template("setores/listar.html", setores=setores)

@main.route("/setores/novo", methods=["GET", "POST"])
def novo_setor():
    empresas = Empresa.query.filter_by(status="Ativa").order_by(Empresa.razao_social.asc()).all()
    unidades = Unidade.query.filter_by(status="Ativa").order_by(Unidade.nome.asc()).all()

    if request.method == "POST":
        unidade_id = request.form.get("unidade_id")

        if unidade_id == "":
            unidade_id = None

        setor = Setor(
            empresa_id=request.form["empresa_id"],
            unidade_id=unidade_id,
            nome=request.form["nome"],
            descricao=request.form["descricao"],
            status=request.form["status"]
        )
        db.session.add(setor)
        db.session.commit()

        flash("Setor cadastrado com sucesso!", "success")
        return redirect(url_for("main.listar_setores"))

    return render_template("setores/novo.html", empresas=empresas, unidades=unidades)

@main.route("/setores/<int:id>/editar", methods=["GET", "POST"])
def editar_setor(id):
    setor = Setor.query.get_or_404(id)
    empresas = Empresa.query.filter_by(status="Ativa").order_by(Empresa.razao_social.asc()).all()
    unidades = Unidade.query.filter_by(status="Ativa").order_by(Unidade.nome.asc()).all()

    if request.method == "POST":
        unidade_id = request.form.get("unidade_id")

        if unidade_id == "":
            unidade_id = None

        setor.empresa_id = request.form["empresa_id"]
        setor.unidade_id = unidade_id
        setor.nome = request.form["nome"]
        setor.descricao = request.form["descricao"]
        setor.status = request.form["status"]

        db.session.commit()

        flash("Setor atualizado com sucesso!", "success")
        return redirect(url_for("main.listar_setores"))

    return render_template("setores/editar.html", setor=setor, empresas=empresas, unidades=unidades)

@main.route("/setores/<int:id>/inativar", methods=["POST"])
def inativar_setor(id):
    setor = Setor.query.get_or_404(id)
    setor.status = "Inativa"
    db.session.commit()

    flash("Setor inativado com sucesso!", "warning")
    return redirect(url_for("main.listar_setores"))