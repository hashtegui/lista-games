from flask import Flask, render_template, request, redirect, session, flash, url_for

app = Flask(__name__)
app.secret_key = 'guilherme'

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

class Usuario:
    def __init__(self, id, nome, senha) -> None:
        self.__id = id
        self.__nome = nome
        self.__senha = senha

    @property
    def nome(self):
        return self.__nome
    @property
    def id(self):
        return self.__id
    @property
    def senha(self):
        return self.__senha


usuario1 = Usuario('gui','Guilherme', '1234')
usuario2 = Usuario('nico','Nico Steppat', '7a1')
usuario3 = Usuario('flavio','Flavio', 'javascript')

usuarios = {usuario1.id: usuario1,
            usuario2.id:usuario2 , 
            usuario3.id: usuario3}

jogo1 = Jogo('Super Mario', 'Aventura', 'SNES')
jogo2 = Jogo('Pokemom Gold', 'RPG', 'Game Boy')
jogo3 = Jogo('Mortal Kombat', 'Luta', 'N64')
lista = [jogo1, jogo2, jogo3]


@app.route('/')
def index():
    
    return render_template('lista.html', titulo='Jogos', jogos=lista)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login',proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Jogo')

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']

    jogo = Jogo(nome,categoria, console)
    lista.append(jogo)

    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    if request.form['usuario']in usuarios:
       usuario = usuarios[request.form['usuario']]
       if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.id
            flash(usuario.nome + ' logou com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Não logado, tente novamente')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado']=None
    flash('Nenhum usuário logado!')
    return redirect(url_for('index'))

app.run(debug=True)


