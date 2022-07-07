from flask import Flask, redirect, render_template, request, url_for
import json
import random
import yaml

app = Flask(__name__)

data = None

with open("data.json", "r", encoding="utf8") as f:
    data = json.load(f)

def abrirArquivo(nomeArquivo):
    questoes = []
    with open(nomeArquivo, "r", encoding="utf8") as f:
        dados = yaml.load_all(f, Loader = yaml.Loader)
        for questao in dados:
            questoes.append(questao)

    return questoes

def makeRelatorio(id_da_pessoa):
    for pessoa in data["users"]:
        if pessoa["id"] != id_da_pessoa:
            continue
        if len(pessoa["questoesRespondidas"]) == 0:
            return None
        relatorio = [i for i in pessoa["questoesRespondidas"]]
        return relatorio

def buscaQuestao(materia, idPessoa, nivelpassado = None):
    dados = None
    questoesProibidas = None
    id_prefix = None
    questoes = [] 

    for pessoa in data["users"]:
        if pessoa["id"] == idPessoa:
            questoesProibidas = [x["id_questao"] for x in pessoa["questoesRespondidas"]]
            break

    if materia == "ga":
        dados = abrirArquivo("yaml/ga.yaml")
        id_prefix = "0"
    elif materia == "imm":
        dados = abrirArquivo("yaml/modelagem.yaml")
        id_prefix = "1"
    elif materia == "ic":
        dados = abrirArquivo("yaml/ic.yaml")
        id_prefix = "2"
    elif materia == "fun":
        dados = abrirArquivo("yaml/fundamentos.yaml")
        id_prefix = "3"
    else:
        dados = abrirArquivo("yaml/calculo.yaml")
        id_prefix = "4"  

    for questao in dados:
        questao["id"] = str(questao["id"]) + id_prefix

        if nivelpassado != None and questao["nivel"] != nivelpassado:
            continue

        if len(questoesProibidas) != 0 and questao["id"] in questoesProibidas:
            continue

        questoes.append(questao)

    if len(questoes) == 0:
        return None

    questaoEscolhida = random.choice(questoes)

    return questaoEscolhida

def descobrirProximoNive(nivelAnterior, acertouAnterior):
    nivelAnterior = str(nivelAnterior)
    if nivelAnterior == "1":
        if acertouAnterior == "true":
            return 2
        else:
            return 1 
    elif nivelAnterior == "2":
        if acertouAnterior == "true":
            return 3
        else:
            return 1 
    else:
        if acertouAnterior == "true":
            return 3
        else:
            return 2 

def addQuestion(nome, id_question, acertouPassado,nivelQuestao):
    for pessoa in data["users"]:
        if pessoa["nome"] == nome:
            objetoTeste = {
                "id_questao" : id_question,
                "acertou" : acertouPassado,
                "nivel" : nivelQuestao
            }
            pessoa["questoesRespondidas"].append(objetoTeste)

def verificaNome(nome):
    for pessoa in data["users"]:
        
        if pessoa["nome"] == nome:
            return False

    return True

def carregaIdUsuarios():
    ids = []
    for pessoa in data["users"]:
        ids.append(pessoa["id"])
    
    return ids

def gerarIdAleatorio():
    idGerado = random.randint(10000,100000)
    if idGerado in carregaIdUsuarios():
        idGerado = gerarIdAleatorio()
    return idGerado

def pegaId(nome):
    for pessoa in data["users"]:
        if pessoa["nome"] == nome:
            return pessoa["id"]

def addPessoa(nomePassado):
    pessoa = {
        "nome":nomePassado,
        "id": gerarIdAleatorio(),
        "questoesRespondidas": [],
        "relatorio": []
    }
    data["users"].append(pessoa)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        nomeUser = request.form.get("username")
        if verificaNome(nomeUser):
            addPessoa(nomeUser)
            return redirect(url_for("choose", nomeusuario = nomeUser))
        return render_template("login.html", invalido="Nome indisponível!", pessoas = data["users"])
    else:
        return render_template("login.html", pessoas = data["users"])

@app.route("/choose/<nomeusuario>")
def choose(nomeusuario):
    id_pessoa = pegaId(nomeusuario)
    relatorio = makeRelatorio(id_pessoa)
    return render_template("choose.html", relatorio = relatorio)

@app.route("/teste/<nomeusuario>/<materia>", methods = ['POST', 'GET'])
def teste(nomeusuario, materia):
    questao = buscaQuestao(materia, pegaId(nomeusuario))

    if request.method == "POST":
        acertou = request.form['info_data']
        id_question = request.form['id_question']
        nv_questao = request.form['nivel_question']

        addQuestion(nomeusuario, id_question, acertou, nv_questao)
        proximoNivel = descobrirProximoNive(nv_questao, acertou)
        id_user = pegaId(nomeusuario)

        questao = buscaQuestao(materia, id_user , proximoNivel)

        if questao == None:
            return "end"
        else: 
            return questao

    else:
        if questao == None:
            return redirect(url_for("choose", nomeusuario = nomeusuario))
        return render_template("teste.html", data = questao)

@app.route("/calendario", methods = ['POST','GET'])
def calendario():
    if request.method == "POST":
        number_day = request.form['info_dia']
        number_ano = request.form['info_ano']
        number_mes = str(int(request.form['info_mes']) + 1)

        def verificarData(dt):
            dadosCalendario = abrirArquivo("yaml/calendario.yaml")
            for row in dadosCalendario:
                if row["data"] == dt:
                    return row["evento"]
            return "Sem evento"

        return verificarData(number_day+"/"+ number_mes +"/"+number_ano)

    return render_template("calendario.html")

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug = True)