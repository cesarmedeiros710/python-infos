# 🌐 Projeto Flask com Integração API Gemini

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-2.x-lightgrey?logo=flask)
![Gemini API](https://img.shields.io/badge/Gemini-API-yellow?logo=google)
![Status](https://img.shields.io/badge/status-em%20desenvolvimento-orange)

Este é um projeto web desenvolvido com **Flask** que oferece seções educativas e interativas sobre Python, com glossário, conteúdo explicativo e integração com a **API Gemini** (Google AI) para respostas inteligentes.

---

## 📁 Estrutura do Site

├── app.py # Código principal Flask
├── bd_glossario.csv # Base de dados do glossário
├── templates/
│ ├── index.html # Página inicial
│ ├── glossario.html # Lista de termos e significados
│ ├── conteudo.html # Conteúdo educativo de Python
│ └── quiz.html # (em desenvolvimento)
├── .venv/ # Ambiente virtual
├── .env # Variáveis de ambiente


---

## 📚 Seções do Site

- **Página Inicial (`/`)**: Apresentação do site.
- **Glossário (`/glossario`)**: Lista de termos e significados sobre programação.
- **Conteúdo (`/conteudo`)**: Explicações detalhadas sobre Python.
- **Quiz (`/quiz`)**: Avaliação dos conhecimentos adquiridos.

---

## 🚀 Tecnologias Utilizadas

- **Python 3.10+**
- **Flask** (framework web)
- **Google Generative AI SDK** (`google.generativeai`)
- **dotenv** para carregar variáveis de ambiente
- **HTML + Bootstrap** para os templates

---

## 🤖 Integração com a API Gemini

A integração está no arquivo `app.py`:

```python
genai.configure(api_key=os.getenv("API_KEY"))

def call_gemini_api(prompt):
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    return response.text
```

## 🧩 Principais Partes do Código
app.py: Controla rotas e lógica principal.

call_gemini_api(): Chama a API Gemini com um prompt.

carregar_glossario(): Lê o CSV de termos.

templates/: Contém páginas renderizadas com Flask (Jinja2).

bd_glossario.csv: Base local de glossário (termo;significado).

## 🚀 Como Executar
Clone o repositório

Configure o ambiente:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```
Crie um arquivo .env:
```ini
GENAI_API_KEY=sua_chave
FLASK_SECRET_KEY=chave_secreta
```

Inicie o servidor:
```bash
flask run
