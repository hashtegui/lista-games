from flask import Flask, render_template, request, redirect, session, flash, url_for
from dao import JogoDao, UsuarioDao
from models import Usuario, Jogo

import mysql.connector
import os


db = mysql.connector.connect(
    host="localhost",
    user="root",
    port = 3306,
    password="123456",
    auth_plugin='mysql_native_password',
    db='jogoteca'
)

jogo_dao = JogoDao(db)
usuario_dao = UsuarioDao(db)

app = Flask(__name__)
app.secret_key = 'guilherme'
app.config['UPLOAD_PATH'] = \
    os.path.dirname(os.path.abspath(__file__)) + '/uploads'

@app.route('/')
def index():
    lista = jogo_dao.listar()
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
    jogo = jogo_dao.salvar(jogo)
    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH'] 
    arquivo.save(f'{upload_path}/capa_{jogo.id}.jpg')

    return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login',proxima=url_for('editar')))
    jogo = jogo_dao.buscar_por_id(id)
    return render_template('editar.html', titulo='Editando Jogo', jogo=jogo)


@app.route('/atualizar', methods=['POST',])
def atualizar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    id = request.form['id']

    jogo = Jogo(nome,categoria, console, id)
    jogo_dao.salvar(jogo)

    return redirect(url_for('index'))


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    usuario = usuario_dao.busca_por_id(request.form['usuario'])

    if usuario:
       if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.id
            flash(usuario.nome + ' logou com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Não logado, tente novamente')
        return redirect(url_for('login'))

@app.route('/deletar/<int:id>')
def deletar(id):
    jogo_dao.deletar(id)
    flash('o jogo foi removido com sucesso')
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session['usuario_logado']=None
    flash('Nenhum usuário logado!')
    return redirect(url_for('index'))

app.run(debug=True)


