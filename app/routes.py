from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy import func, cast, Integer

from app import db
from app.models import Empresa, Unidade, Setor, Cargo, Questionario, Pergunta, Aplicacao, Resposta


main = Blueprint("main", __name__)


@main.route("/")
def index():
    total_empresas = Empresa.query.count()
    total_questionarios = Questionario.query.count()
    total_aplicacoes = Aplicacao.query.count()
    total_respostas = Resposta.query.count()

    aplicacoes_abertas = Aplicacao.query.filter_by(status="Aberta").count()
    aplicacoes_encerradas = Aplicacao.query.filter_by(status="Encerrada").count()

    media_respostas = db.session.query(
        func.avg(cast(Resposta.valor_resposta, Integer))
    ).join(
        Pergunta,
        Pergunta.id == Resposta.pergunta_id
    ).filter(
        Pergunta.tipo_resposta == "escala_1_5"
    ).scalar()

    media_respostas = 0 if media_respostas is None else round(float(media_respostas), 2)

    respostas_por_pergunta = db.session.query(
        Pergunta.texto,
        func.avg(cast(Resposta.valor_resposta, Integer))
    ).join(
        Resposta,
        Resposta.pergunta_id == Pergunta.id
    ).filter(
        Pergunta.tipo_resposta == "escala_1_5"
    ).group_by(
        Pergunta.id,
        Pergunta.texto,
        Pergunta.ordem
    ).order_by(
        Pergunta.ordem.asc()
    ).all()

    labels_perguntas = [
        item[0][:40] + "..." if len(item[0]) > 40 else item[0]
        for item in respostas_por_pergunta
    ]

    medias_perguntas = [
        round(float(item[1]), 2)
        for item in respostas_por_pergunta
    ]

    return render_template(
        "index.html",
        total_empresas=total_empresas,
        total_questionarios=total_questionarios,
        total_aplicacoes=total_aplicacoes,
        total_respostas=total_respostas,
        aplicacoes_abertas=aplicacoes_abertas,
        aplicacoes_encerradas=aplicacoes_encerradas,
        media_respostas=media_respostas,
        labels_perguntas=labels_perguntas,
        medias_perguntas=medias_perguntas
    )


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
# QUESTIONÁRIOS
# =========================
@main.route("/questionarios")
def listar_questionarios():
    questionarios = Questionario.query.order_by(Questionario.id.desc()).all()
    return render_template("questionarios/listar.html", questionarios=questionarios)


@main.route("/questionarios/novo", methods=["GET", "POST"])
def novo_questionario():
    if request.method == "POST":
        questionario = Questionario(
            nome=request.form["nome"],
            descricao=request.form["descricao"],
            status=request.form["status"]
        )
        db.session.add(questionario)
        db.session.commit()

        flash("Questionário cadastrado com sucesso!", "success")
        return redirect(url_for("main.listar_questionarios"))

    return render_template("questionarios/novo.html")


@main.route("/questionarios/<int:id>/editar", methods=["GET", "POST"])
def editar_questionario(id):
    questionario = Questionario.query.get_or_404(id)

    if request.method == "POST":
        questionario.nome = request.form["nome"]
        questionario.descricao = request.form["descricao"]
        questionario.status = request.form["status"]

        db.session.commit()

        flash("Questionário atualizado com sucesso!", "success")
        return redirect(url_for("main.listar_questionarios"))

    return render_template("questionarios/editar.html", questionario=questionario)


@main.route("/questionarios/<int:id>/inativar", methods=["POST"])
def inativar_questionario(id):
    questionario = Questionario.query.get_or_404(id)
    questionario.status = "Inativo"
    db.session.commit()

    flash("Questionário inativado com sucesso!", "warning")
    return redirect(url_for("main.listar_questionarios"))


# =========================
# PERGUNTAS
# =========================
@main.route("/perguntas")
def listar_perguntas():
    perguntas = Pergunta.query.order_by(Pergunta.ordem.asc(), Pergunta.id.asc()).all()
    return render_template("perguntas/listar.html", perguntas=perguntas)


@main.route("/perguntas/nova", methods=["GET", "POST"])
def nova_pergunta():
    questionarios = Questionario.query.filter_by(status="Ativo").order_by(Questionario.nome.asc()).all()

    if request.method == "POST":
        obrigatoria = True if request.form.get("obrigatoria") == "sim" else False

        pergunta = Pergunta(
            questionario_id=request.form["questionario_id"],
            texto=request.form["texto"],
            tipo_resposta=request.form["tipo_resposta"],
            obrigatoria=obrigatoria,
            ordem=request.form["ordem"],
            status=request.form["status"]
        )
        db.session.add(pergunta)
        db.session.commit()

        flash("Pergunta cadastrada com sucesso!", "success")
        return redirect(url_for("main.listar_perguntas"))

    return render_template("perguntas/nova.html", questionarios=questionarios)


@main.route("/perguntas/<int:id>/editar", methods=["GET", "POST"])
def editar_pergunta(id):
    pergunta = Pergunta.query.get_or_404(id)
    questionarios = Questionario.query.filter_by(status="Ativo").order_by(Questionario.nome.asc()).all()

    if request.method == "POST":
        obrigatoria = True if request.form.get("obrigatoria") == "sim" else False

        pergunta.questionario_id = request.form["questionario_id"]
        pergunta.texto = request.form["texto"]
        pergunta.tipo_resposta = request.form["tipo_resposta"]
        pergunta.obrigatoria = obrigatoria
        pergunta.ordem = request.form["ordem"]
        pergunta.status = request.form["status"]

        db.session.commit()

        flash("Pergunta atualizada com sucesso!", "success")
        return redirect(url_for("main.listar_perguntas"))

    return render_template("perguntas/editar.html", pergunta=pergunta, questionarios=questionarios)


@main.route("/perguntas/<int:id>/inativar", methods=["POST"])
def inativar_pergunta(id):
    pergunta = Pergunta.query.get_or_404(id)
    pergunta.status = "Inativa"
    db.session.commit()

    flash("Pergunta inativada com sucesso!", "warning")
    return redirect(url_for("main.listar_perguntas"))


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

        unidade_id = None if unidade_id == "" else unidade_id
        setor_id = None if setor_id == "" else setor_id
        cargo_id = None if cargo_id == "" else cargo_id

        aplicacao = Aplicacao(
            questionario_id=request.form["questionario_id"],
            empresa_id=request.form["empresa_id"],
            unidade_id=unidade_id,
            setor_id=setor_id,
            cargo_id=cargo_id,
            titulo=request.form["titulo"],
            data_inicio=request.form["data_inicio"] or None,
            data_fim=request.form["data_fim"] or None,
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

        unidade_id = None if unidade_id == "" else unidade_id
        setor_id = None if setor_id == "" else setor_id
        cargo_id = None if cargo_id == "" else cargo_id

        aplicacao.questionario_id = request.form["questionario_id"]
        aplicacao.empresa_id = request.form["empresa_id"]
        aplicacao.unidade_id = unidade_id
        aplicacao.setor_id = setor_id
        aplicacao.cargo_id = cargo_id
        aplicacao.titulo = request.form["titulo"]
        aplicacao.data_inicio = request.form["data_inicio"] or None
        aplicacao.data_fim = request.form["data_fim"] or None
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


# =========================
# RESPOSTAS DO QUESTIONÁRIO
# =========================
@main.route("/aplicacoes/<int:id>/responder", methods=["GET", "POST"])
def responder_aplicacao(id):
    aplicacao = Aplicacao.query.get_or_404(id)

    perguntas = Pergunta.query.filter_by(
        questionario_id=aplicacao.questionario_id,
        status="Ativa"
    ).order_by(Pergunta.ordem.asc()).all()

    if request.method == "POST":
        for pergunta in perguntas:
            campo = f"pergunta_{pergunta.id}"
            valor = request.form.get(campo)

            if valor:
                resposta = Resposta(
                    aplicacao_id=aplicacao.id,
                    pergunta_id=pergunta.id,
                    valor_resposta=valor
                )
                db.session.add(resposta)

        db.session.commit()

        flash("Respostas salvas com sucesso!", "success")
        return redirect(url_for("main.listar_aplicacoes"))

    return render_template(
        "respostas/responder.html",
        aplicacao=aplicacao,
        perguntas=perguntas
    )


@main.route("/aplicacoes/<int:id>/respostas")
def visualizar_respostas(id):
    aplicacao = Aplicacao.query.get_or_404(id)

    respostas = Resposta.query.filter_by(
        aplicacao_id=aplicacao.id
    ).order_by(Resposta.id.asc()).all()

    return render_template(
        "respostas/listar.html",
        aplicacao=aplicacao,
        respostas=respostas
    )

# =========================
# RESULTADO DA APLICAÇÃO
# =========================
@main.route("/aplicacoes/<int:id>/resultado")
def resultado_aplicacao(id):
    aplicacao = Aplicacao.query.get_or_404(id)

    respostas = Resposta.query.filter_by(
        aplicacao_id=aplicacao.id
    ).join(
        Pergunta,
        Pergunta.id == Resposta.pergunta_id
    ).filter(
        Pergunta.tipo_resposta == "escala_1_5"
    ).all()

    valores = []

    resultado_dimensoes = {}

    for resposta in respostas:
        try:
            valor = int(resposta.valor_resposta)
        except ValueError:
            continue

        valores.append(valor)

        texto = resposta.pergunta.texto

        dominio = "Não informado"
        dimensao = "Não informado"

        if texto.startswith("[") and "]" in texto:
            cabecalho = texto.split("]")[0].replace("[", "")
            partes = cabecalho.split("|")

            if len(partes) == 2:
                dominio = partes[0].strip()
                dimensao = partes[1].strip()

        chave = (dominio, dimensao)

        if chave not in resultado_dimensoes:
            resultado_dimensoes[chave] = []

        resultado_dimensoes[chave].append(valor)

    media_geral = 0

    if valores:
        media_geral = round(sum(valores) / len(valores), 2)

    if media_geral == 0:
       classificacao = "Sem dados"
       descricao_classificacao = "Não há respostas suficientes para gerar uma classificação."
       recomendacao = "Realizar a aplicação do questionário e coletar respostas válidas."
    elif media_geral < 2:
        classificacao = "Baixo"
        descricao_classificacao = "Os resultados indicam baixo nível de exposição aos fatores psicossociais avaliados."
        recomendacao = "Manter as práticas organizacionais atuais e acompanhar periodicamente os indicadores."
    elif media_geral < 3:
        classificacao = "Moderado"
        descricao_classificacao = "Os resultados indicam atenção moderada aos fatores psicossociais avaliados."
        recomendacao = "Monitorar os fatores identificados e avaliar ações preventivas junto aos setores envolvidos."
    elif media_geral < 4:
        classificacao = "Alto"
        descricao_classificacao = "Os resultados indicam alto nível de atenção para riscos psicossociais."
        recomendacao = "Recomenda-se análise detalhada dos fatores críticos e definição de plano de ação preventivo."
    else:
        classificacao = "Crítico"
        descricao_classificacao = "Os resultados indicam nível crítico de exposição aos fatores psicossociais avaliados."
        recomendacao = "Recomenda-se intervenção prioritária, investigação aprofundada e acompanhamento técnico especializado."

    linhas_resultado = []

    for chave, lista_valores in resultado_dimensoes.items():
        dominio, dimensao = chave
        media = round(sum(lista_valores) / len(lista_valores), 2)

        linhas_resultado.append({
            "dominio": dominio,
            "dimensao": dimensao,
            "media": media,
            "quantidade": len(lista_valores)
        })

    linhas_resultado = sorted(
        linhas_resultado,
        key=lambda item: (item["dominio"], item["dimensao"])
    )

    labels_dimensoes = [
        item["dimensao"] for item in linhas_resultado
    ]

    medias_dimensoes = [
        item["media"] for item in linhas_resultado
    ]

    return render_template(
    "resultados/aplicacao.html",
    aplicacao=aplicacao,
    media_geral=media_geral,
    classificacao=classificacao,
    descricao_classificacao=descricao_classificacao,
    recomendacao=recomendacao,
    linhas_resultado=linhas_resultado,
    labels_dimensoes=labels_dimensoes,
    medias_dimensoes=medias_dimensoes
)