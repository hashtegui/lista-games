from flask import Flask, render_template,request, redirect

app = Flask(__name__)

class Jogo():
    def __init__(self, nome, categoria, console) -> None:
        self.__nome = nome
        self.__categoria = categoria
        self.__console = console
    
    @property
    def nome(self):
        return self.__nome
    
    @property
    def categoria(self):
        return self.__categoria
    
    @property
    def console(self):
        return self.__console

jogo1 = Jogo('Super Mario', 'Aventura', 'SNES')
jogo2 = Jogo('Pokemom Gold', 'RPG', 'Game Boy')
jogo3 = Jogo('Mortal Kombat', 'Luta', 'N64')
lista = [jogo1, jogo2, jogo3]


@app.route('/')
def index():
    
    return render_template('lista.html', titulo='Jogos', jogos=lista)

@app.route('/novo')
def novo():
    return render_template('novo.html', titulo='Novo Jogo')

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']

    jogo = Jogo(nome,categoria, console)
    lista.append(jogo)

    return redirect('/')


app.run(debug=True)

