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


def buscaQuestao(materia, idPessoa):
    dados = None
    questoesProibidas = None
    id_prefix = None

    for jogador in data["jogadores"]:
        if jogador["id"] == idPessoa:
            questoesProibidas = jogador["questoesRespondidas"]
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

    questoes = []   

    for questao in dados:
        questao["id"] = str( questao["id"]) + id_prefix

        if len(questoesProibidas) != 0:
            if questao["id"] in questoesProibidas:
                continue

            questoes.append(questao)

        else:
            questoes.append(questao)

    if len(questoes) == 0:
        return None

    questaoEscolhida = random.choice(questoes)

    return questaoEscolhida

def addQuestion(nome, id_question):
    for jogador in data["jogadores"]:
        if jogador["nome"] == nome:
            jogador["questoesRespondidas"].append(id_question)

def verificaNome(nome):
    for jogador in data["jogadores"]:
        
        if jogador["nome"] == nome:
            return False

    return True

def carregaIdJogadores():
    ids = []
    for jogador in data["jogadores"]:
        ids.append(jogador["id"])
    
    return ids

def gerarIdAleatorio():
    idGerado = random.randint(10000,100000)
    if idGerado in carregaIdJogadores():
        idGerado = gerarIdAleatorio()
    return idGerado

def pegaId(nome):
    for jogador in data["jogadores"]:
        if jogador["nome"] == nome:
            return jogador["id"]

def addPessoa(nomePassado):
    pessoa = {
        "nome":nomePassado,
        "id": gerarIdAleatorio(),
        "questoesRespondidas": []
    }
    data["jogadores"].append(pessoa)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        nomeUser = request.form.get("username")
        if verificaNome(nomeUser):
            addPessoa(nomeUser)
            return redirect(url_for("choose", nomeusuario = nomeUser))
        return render_template("login.html", invalido="Nome indisponível!", jogadores = data["jogadores"])
    else:
        return render_template("login.html", jogadores = data["jogadores"])

@app.route("/choose/<nomeusuario>")
def choose(nomeusuario):
    return render_template("choose.html")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/teste/<nomeusuario>/<materia>", methods = ['POST', 'GET'])
def teste(nomeusuario, materia):
    questao = buscaQuestao(materia, pegaId(nomeusuario))

    if questao == None:
        return redirect(url_for("choose", nomeusuario = nomeusuario))

    if request.method == "POST":
        acertou = request.form['info_data']
        id_question = request.form['id_question']

        addQuestion(nomeusuario, id_question)

    return render_template("teste.html", data = questao)

@app.route("/calendario")
def calendario():
    return render_template("calendario.html")

if __name__ == "__main__":
    app.run(debug = True)