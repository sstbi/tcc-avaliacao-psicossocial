from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Empresa, Unidade, Setor, Cargo
from app.models import Empresa, Unidade, Setor, Cargo, Questionario, Pergunta, Aplicacao

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


# =========================
# CARGOS
# =========================
@main.route("/cargos")
def listar_cargos():
    cargos = Cargo.query.order_by(Cargo.id.desc()).all()
    return render_template("cargos/listar.html", cargos=cargos)


@main.route("/cargos/novo", methods=["GET", "POST"])
def novo_cargo():
    empresas = Empresa.query.filter_by(status="Ativa").order_by(Empresa.razao_social.asc()).all()
    unidades = Unidade.query.filter_by(status="Ativa").order_by(Unidade.nome.asc()).all()
    setores = Setor.query.filter_by(status="Ativa").order_by(Setor.nome.asc()).all()

    if request.method == "POST":
        unidade_id = request.form.get("unidade_id")
        setor_id = request.form.get("setor_id")

        if unidade_id == "":
            unidade_id = None
        if setor_id == "":
            setor_id = None

        cargo = Cargo(
            empresa_id=request.form["empresa_id"],
            unidade_id=unidade_id,
            setor_id=setor_id,
            nome=request.form["nome"],
            descricao=request.form["descricao"],
            status=request.form["status"]
        )
        db.session.add(cargo)
        db.session.commit()

        flash("Cargo cadastrado com sucesso!", "success")
        return redirect(url_for("main.listar_cargos"))

    return render_template(
        "cargos/novo.html",
        empresas=empresas,
        unidades=unidades,
        setores=setores
    )


@main.route("/cargos/<int:id>/editar", methods=["GET", "POST"])
def editar_cargo(id):
    cargo = Cargo.query.get_or_404(id)
    empresas = Empresa.query.filter_by(status="Ativa").order_by(Empresa.razao_social.asc()).all()
    unidades = Unidade.query.filter_by(status="Ativa").order_by(Unidade.nome.asc()).all()
    setores = Setor.query.filter_by(status="Ativa").order_by(Setor.nome.asc()).all()

    if request.method == "POST":
        unidade_id = request.form.get("unidade_id")
        setor_id = request.form.get("setor_id")

        if unidade_id == "":
            unidade_id = None
        if setor_id == "":
            setor_id = None

        cargo.empresa_id = request.form["empresa_id"]
        cargo.unidade_id = unidade_id
        cargo.setor_id = setor_id
        cargo.nome = request.form["nome"]
        cargo.descricao = request.form["descricao"]
        cargo.status = request.form["status"]

        db.session.commit()

        flash("Cargo atualizado com sucesso!", "success")
        return redirect(url_for("main.listar_cargos"))

    return render_template(
        "cargos/editar.html",
        cargo=cargo,
        empresas=empresas,
        unidades=unidades,
        setores=setores
    )


@main.route("/cargos/<int:id>/inativar", methods=["POST"])
def inativar_cargo(id):
    cargo = Cargo.query.get_or_404(id)
    cargo.status = "Inativa"
    db.session.commit()

    flash("Cargo inativado com sucesso!", "warning")
    return redirect(url_for("main.listar_cargos"))

# =========================
# APLICAÇÕES
# =========================
@main.route("/aplicacoes")
def listar_aplicacoes():
    aplicacoes = Aplicacao.query.order_by(Aplicacao.id.desc()).all()
    return render_template("aplicacoes/listar.html", aplicacoes=aplicacoes)


@main.route("/aplicacoes/nova", methods=["GET", "POST"])
def nova_aplicacao():
    questionarios = Questionario.query.filter_by(status="Ativo").order_by(Questionario.nome.asc()).all()
    empresas = Empresa.query.filter_by(status="Ativa").order_by(Empresa.razao_social.asc()).all()
    unidades = Unidade.query.filter_by(status="Ativa").order_by(Unidade.nome.asc()).all()
    setores = Setor.query.filter_by(status="Ativa").order_by(Setor.nome.asc()).all()
    cargos = Cargo.query.filter_by(status="Ativa").order_by(Cargo.nome.asc()).all()

    if request.method == "POST":

        unidade_id = request.form.get("unidade_id")
        setor_id = request.form.get("setor_id")
        cargo_id = request.form.get("cargo_id")

        if unidade_id == "":
            unidade_id = None

        if setor_id == "":
            setor_id = None

        if cargo_id == "":
            cargo_id = None

        aplicacao = Aplicacao(
            questionario_id=request.form["questionario_id"],
            empresa_id=request.form["empresa_id"],
            unidade_id=unidade_id,
            setor_id=setor_id,
            cargo_id=cargo_id,
            titulo=request.form["titulo"],
            data_inicio=request.form["data_inicio"],
            data_fim=request.form["data_fim"],
            status=request.form["status"]
        )

        db.session.add(aplicacao)
        db.session.commit()

        flash("Aplicação cadastrada com sucesso!", "success")
        return redirect(url_for("main.listar_aplicacoes"))

    return render_template(
        "aplicacoes/nova.html",
        questionarios=questionarios,
        empresas=empresas,
        unidades=unidades,
        setores=setores,
        cargos=cargos
    )


@main.route("/aplicacoes/<int:id>/editar", methods=["GET", "POST"])
def editar_aplicacao(id):

    aplicacao = Aplicacao.query.get_or_404(id)

    questionarios = Questionario.query.filter_by(status="Ativo").order_by(Questionario.nome.asc()).all()
    empresas = Empresa.query.filter_by(status="Ativa").order_by(Empresa.razao_social.asc()).all()
    unidades = Unidade.query.filter_by(status="Ativa").order_by(Unidade.nome.asc()).all()
    setores = Setor.query.filter_by(status="Ativa").order_by(Setor.nome.asc()).all()
    cargos = Cargo.query.filter_by(status="Ativa").order_by(Cargo.nome.asc()).all()

    if request.method == "POST":

        unidade_id = request.form.get("unidade_id")
        setor_id = request.form.get("setor_id")
        cargo_id = request.form.get("cargo_id")

        if unidade_id == "":
            unidade_id = None

        if setor_id == "":
            setor_id = None

        if cargo_id == "":
            cargo_id = None

        aplicacao.questionario_id = request.form["questionario_id"]
        aplicacao.empresa_id = request.form["empresa_id"]
        aplicacao.unidade_id = unidade_id
        aplicacao.setor_id = setor_id
        aplicacao.cargo_id = cargo_id
        aplicacao.titulo = request.form["titulo"]
        aplicacao.data_inicio = request.form["data_inicio"]
        aplicacao.data_fim = request.form["data_fim"]
        aplicacao.status = request.form["status"]

        db.session.commit()

        flash("Aplicação atualizada com sucesso!", "success")
        return redirect(url_for("main.listar_aplicacoes"))

    return render_template(
        "aplicacoes/editar.html",
        aplicacao=aplicacao,
        questionarios=questionarios,
        empresas=empresas,
        unidades=unidades,
        setores=setores,
        cargos=cargos
    )


@main.route("/aplicacoes/<int:id>/encerrar", methods=["POST"])
def encerrar_aplicacao(id):

    aplicacao = Aplicacao.query.get_or_404(id)

    aplicacao.status = "Encerrada"

    db.session.commit()

    flash("Aplicação encerrada com sucesso!", "warning")

    return redirect(url_for("main.listar_aplicacoes"))