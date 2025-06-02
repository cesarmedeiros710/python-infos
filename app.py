import os
import csv
from flask import Flask, render_template, url_for, request, redirect, flash
from dotenv import load_dotenv
import google.generativeai as genai

app = Flask(__name__)
app.secret_key = 'secret_key'
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
else:
    print(" AVISO: GEMINI_API_KEY não está definida no .env")

GLOSSARIO_FILE = 'bd_glossario.csv'

def carregar_glossario():
    glossario = []
    if os.path.exists(GLOSSARIO_FILE):
        try:
            with open(GLOSSARIO_FILE, 'r', newline='', encoding='utf-8') as arquivo:
                reader = csv.reader(arquivo, delimiter=';')
                next(reader, None)
                for row in reader:
                    if len(row) == 2:
                        glossario.append(row)
        except Exception as e:
            flash(f'Erro ao carregar glossário: {str(e)}', 'error')
    return glossario

def salvar_glossario(glossario):
    try:
        with open(GLOSSARIO_FILE, 'w', newline='', encoding='utf-8') as arquivo:
            writer = csv.writer(arquivo, delimiter=';')
            writer.writerows(glossario)
    except Exception as e:
        flash(f'Erro ao salvar glossário: {str(e)}', 'error')


@app.route('/')
def ola():
    return render_template('index.html')

@app.route('/sobre-equipe')
def sobre_equipe():
    return render_template('sobre_equipe.html')

@app.route('/glossario')
def glossario():
    termos = carregar_glossario()
    return render_template('glossario.html', glossario=termos)

@app.route('/novo-termo')
def novo_termo():
    return render_template('novo_termo.html')

@app.route('/criar_termo', methods=['POST'])
def criar_termo():
    termo = request.form.get('termo', '').strip()
    definicao = request.form.get('definicao', '').strip()

    if not termo or not definicao:
        flash('Termo e definição são obrigatórios!', 'error')
        return redirect(url_for('novo_termo'))

    glossario = carregar_glossario()
    glossario.append([termo, definicao])
    salvar_glossario(glossario)

    flash('Termo adicionado com sucesso!', 'success')
    return redirect(url_for('glossario'))

@app.route('/editar-termo/<int:index>')
def editar_termo(index):
    termos = carregar_glossario()
    if 0 <= index < len(termos):
        return render_template('editar_termo.html', termo=termos[index], index=index)
    return redirect(url_for('glossario'))

@app.route('/atualizar-termo/<int:index>', methods=['POST'])
def atualizar_termo(index):
    termo = request.form['termo']
    definicao = request.form['definicao']

    termos = carregar_glossario()
    if 0 <= index < len(termos):
        termos[index] = [termo, definicao]
        salvar_glossario(termos)

    return redirect(url_for('glossario'))

@app.route('/deletar-termo/<int:index>')
def deletar_termo(index):
    termos = carregar_glossario()
    if 0 <= index < len(termos):
        termos.pop(index)
        salvar_glossario(termos)
    return redirect(url_for('glossario'))

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        respostas_corretas = {
            'q1': 'if',
            'q2': 'for',
            'q3': 'lista',
            'q4': 'def'
        }
        acertos = 0
        mensagens = []

        for pergunta, correta in respostas_corretas.items():
            resposta_usuario = request.form.get(pergunta)
            if resposta_usuario == correta:
                acertos += 1
                mensagens.append(f"Pergunta {pergunta[1:]}: Correto!")
            else:
                mensagens.append(f"Pergunta {pergunta[1:]}: Errado! A resposta correta é {correta}")

        return render_template('quiz.html', resultado=acertos, mensagens=mensagens)

    return render_template('quiz.html')


@app.route('/estruturas-selecao')
def estruturas_selecao():
    return render_template('selecao.html')

@app.route('/estruturas-repeticao')
def estruturas_repeticao():
    return render_template('repeticao.html')

@app.route('/vetores-matrizes')
def vetores_matrizes():
    return render_template('vetores_matrizes.html')

@app.route('/funcoes-procedimentos')
def funcoes_procedimentos():
    return render_template('funcoes.html')

@app.route('/tratamento-excecoes')
def tratamento_excecoes():
    return render_template('excecoes.html')


@app.route('/gemini', methods=['GET', 'POST'])
def gemini_chat():
    resposta = None
    pergunta_anterior = None

    if request.method == 'POST':
        pergunta_anterior = request.form.get('pergunta')
        try:
            model = genai.GenerativeModel('gemini-1.0-pro')
            response = model.generate_content(pergunta_anterior)
            resposta = response.text
        except Exception as e:
            resposta = f"Erro ao acessar a API: {str(e)}"

    return render_template('gemini.html', resposta=resposta, pergunta_anterior=pergunta_anterior)


if __name__ == '__main__':
    app.run(debug=True)
