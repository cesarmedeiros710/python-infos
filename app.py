import os
import google.generativeai as genai
import csv
from flask import Flask, render_template, url_for, request, redirect, flash

app = Flask(__name__)
app.secret_key = 'secret_key'

genai.configure(api_key="AIzaSyCiCstFGWXynLSzUIRFKGP38eTOVGNRRcw")  

@app.route('/gemini', methods=['GET', 'POST'])
def gemini_chat():
    if request.method == 'POST':
        user_input = request.form.get('pergunta')
        
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        response = model.generate_content(user_input)
        
        return render_template('gemini.html', resposta=response.text)
    
    return render_template('gemini.html')

GLOSSARIO_FILE = 'bd_glossario.csv'

def carregar_glossario():
    glossario = []
    if os.path.exists(GLOSSARIO_FILE):
        with open(GLOSSARIO_FILE, 'r', newline='', encoding='utf-8') as arquivo:
            reader = csv.reader(arquivo, delimiter=';')
            glossario = list(reader)
    return glossario

def salvar_glossario(glossario):
    with open(GLOSSARIO_FILE, 'w', newline='', encoding='utf-8') as arquivo:
        writer = csv.writer(arquivo, delimiter=';')
        writer.writerows(glossario)

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
    glossario_de_termos = []
    with open('bd_glossario.csv', 'r', newline='', encoding='utf-8') as arquivo:
        reader = csv.reader(arquivo, delimiter=';')
        for linha in reader:
            glossario_de_termos.append(linha)
    
    if 0 <= index < len(glossario_de_termos):
        return render_template('editar_termo.html', termo=glossario_de_termos[index], index=index)
    else:
        return redirect(url_for('glossario'))

@app.route('/atualizar-termo/<int:index>', methods=['POST'])
def atualizar_termo(index):
    termo = request.form['termo']
    definicao = request.form['definicao']
    
    glossario_de_termos = []
    with open('bd_glossario.csv', 'r', newline='', encoding='utf-8') as arquivo:
        reader = csv.reader(arquivo, delimiter=';')
        for linha in reader:
            glossario_de_termos.append(linha)
    
    if 0 <= index < len(glossario_de_termos):
        glossario_de_termos[index] = [termo, definicao]
        
        with open('bd_glossario.csv', 'w', newline='', encoding='utf-8') as arquivo:
            writer = csv.writer(arquivo, delimiter=';')
            writer.writerows(glossario_de_termos)
    
    return redirect(url_for('glossario'))

@app.route('/deletar-termo/<int:index>')
def deletar_termo(index):
    glossario_de_termos = []
    with open('bd_glossario.csv', 'r', newline='', encoding='utf-8') as arquivo:
        reader = csv.reader(arquivo, delimiter=';')
        for linha in reader:
            glossario_de_termos.append(linha)
    
    if 0 <= index < len(glossario_de_termos):
        glossario_de_termos.pop(index)
        
        with open('bd_glossario.csv', 'w', newline='', encoding='utf-8') as arquivo:
            writer = csv.writer(arquivo, delimiter=';')
            writer.writerows(glossario_de_termos)
    
    return redirect(url_for('glossario'))

@app.route('/conteudo-python')
def conteudo_python():
    return render_template('conteudo_python.html')

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
        
        for pergunta, resposta_correta in respostas_corretas.items():
            resposta_usuario = request.form.get(pergunta)
            if resposta_usuario == resposta_correta:
                acertos += 1
                mensagens.append(f"Pergunta {pergunta[1:]}: Correto!")
            else:
                mensagens.append(f"Pergunta {pergunta[1:]}: Errado! A resposta correta é {resposta_correta}")
        
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




app.run(debug=True)