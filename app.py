from flask import Flask, render_template, request, session, redirect, url_for
import sys
import os
import html

# Add the models directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'models'))

# Import your existing classes
from models.estilos.EstiloAventureiro import Estilo_Aventureiro
from models.estilos.EstiloClassico import Estilo_Classico
from models.estilos.EstiloHeroico import Estilo_Heroico
from models.racas.Humano import Humano
from models.racas.Elfo import Elfo
from models.racas.Anao import Anao
from models.racas.Halfling import Halfling
from models.racas.Gnomo import Gnomo
from models.racas.Meio_Elfo import Meio_Elfo
from models.classe.Mago import Mago
from models.classe.Bardo import Bardo
from models.classe.Ladrao import Ladrao

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev_secret_key_medieval_rpg_2024')
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Mapping for races and classes
RACAS = {
    '1': Humano,
    '2': Elfo,
    '3': Anao,
    '4': Meio_Elfo,
    '5': Gnomo,
    '6': Halfling
}

CLASSES = {
    '1': Mago,
    '2': Ladrao,
    '3': Bardo
}

ESTILOS = {
    '1': Estilo_Classico,
    '2': Estilo_Aventureiro,
    '3': Estilo_Heroico
}

# Progress steps for UI
ETAPAS = ['index', 'raca', 'alinhamento', 'estilo', 'atributos', 'classe', 'ficha']

@app.route('/')
def index():
    session.clear()
    session['etapa_atual'] = 'index'
    return render_template('index.html')

@app.route('/raca', methods=['GET', 'POST'])
def escolher_raca():
    session['etapa_atual'] = 'raca'
    
    if request.method == 'POST':
        raca_opcao = request.form.get('raca')
        nome = request.form.get('nome', '').strip()
        
        if not nome or len(nome) > 50:
            return render_template('raca.html', nome=nome)
        
        if raca_opcao not in RACAS:
            return render_template('raca.html', nome=nome)
        
        session['nome'] = html.escape(nome)
        session['raca_opcao'] = raca_opcao
        
        if raca_opcao == '1':
            return redirect(url_for('escolher_alinhamento'))
        
        return redirect(url_for('escolher_estilo'))
    
    nome = session.get('nome', '')
    return render_template('raca.html', nome=nome)

@app.route('/alinhamento', methods=['GET', 'POST'])
def escolher_alinhamento():
    if 'nome' not in session or session.get('raca_opcao') != '1':
        return redirect(url_for('index'))
    
    session['etapa_atual'] = 'alinhamento'
    
    if request.method == 'POST':
        alinhamento_opcao = request.form.get('alinhamento')
        if alinhamento_opcao in ['1', '2', '3']:
            session['alinhamento_opcao'] = alinhamento_opcao
            return redirect(url_for('escolher_estilo'))
    
    return render_template('alinhamento.html')

@app.route('/estilo', methods=['GET', 'POST'])
def escolher_estilo():
    if 'nome' not in session or 'raca_opcao' not in session:
        return redirect(url_for('index'))
    
    session['etapa_atual'] = 'estilo'
    
    if request.method == 'POST':
        estilo_opcao = request.form.get('estilo')
        if estilo_opcao in ESTILOS:
            session['estilo_opcao'] = estilo_opcao
            
            nome = session['nome']
            raca_class = RACAS[session['raca_opcao']]
            
            if session['raca_opcao'] == '1':
                raca = raca_class()
                alinhamento_map = {'1': 'Neutro', '2': 'Ordem', '3': 'Caos'}
                raca.alinhamento = alinhamento_map[session.get('alinhamento_opcao', '1')]
            else:
                raca = raca_class()
            
            estilo_class = ESTILOS[estilo_opcao]
            player = estilo_class(nome, raca)
            
            session['valores'] = player.valores
            session['atributos_restantes'] = list(player.atributos.keys())
            session['atributos_atribuidos'] = {}
            
            if estilo_opcao == '1':  # Clássico aplica automaticamente
                player.aplicar_bonus_raca()
                session['player_data'] = player.get_ficha_dict()
                return redirect(url_for('escolher_classe'))
            else:
                return redirect(url_for('definir_atributos'))
    
    return render_template('estilo.html')

@app.route('/atributos', methods=['GET', 'POST'])
def definir_atributos():
    if 'valores' not in session or 'atributos_restantes' not in session:
        return redirect(url_for('index'))
    
    session['etapa_atual'] = 'atributos'
    
    if request.method == 'POST':
        atributo = request.form.get('atributo')
        valor_str = request.form.get('valor')
        
        if atributo and valor_str and valor_str.isdigit():
            valor = int(valor_str)
            valores = session.get('valores', [])
            
            if valor in valores:
                valores.remove(valor)
                session['valores'] = valores
                atributos_restantes = session.get('atributos_restantes', [])
                
                if atributo in atributos_restantes:
                    atributos_restantes.remove(atributo)
                    session['atributos_restantes'] = atributos_restantes
                session['atributos_atribuidos'][atributo] = valor
                session.modified = True
                
                if not session['atributos_restantes']:
                    return criar_personagem_final()
                
                return redirect(url_for('definir_atributos'))
    
    atributos_restantes = session.get('atributos_restantes', [])
    valores = session.get('valores', [])
    
    if not atributos_restantes:
        return criar_personagem_final()
    
    atributo_atual = atributos_restantes[0]
    
    return render_template('atributos.html', 
                         atributo=atributo_atual,
                         valores=valores,
                         atributos_restantes=atributos_restantes)

def criar_personagem_final():
    nome = session['nome']
    raca_class = RACAS[session['raca_opcao']]
    
    if session['raca_opcao'] == '1':
        raca = raca_class()
        alinhamento_map = {'1': 'Neutro', '2': 'Ordem', '3': 'Caos'}
        raca.alinhamento = alinhamento_map[session.get('alinhamento_opcao', '1')]
    else:
        raca = raca_class()
    
    estilo_class = ESTILOS[session['estilo_opcao']]
    player = estilo_class(nome, raca)
    
    # aplica os atributos escolhidos
    for atributo, valor in session.get('atributos_atribuidos', {}).items():
        player.atributos[atributo] = valor
    
    player.aplicar_bonus_raca()
    
    # agora guarda o dict completo no session
    session['player_data'] = player.get_ficha_dict()
    
    # limpa variáveis auxiliares
    for key in ['valores', 'atributos_restantes', 'atributos_atribuidos']:
        session.pop(key, None)
    
    return redirect(url_for('escolher_classe'))

@app.route('/classe', methods=['GET', 'POST'])
def escolher_classe():
    if 'player_data' not in session:
        return redirect(url_for('index'))
    
    session['etapa_atual'] = 'classe'
    
    if request.method == 'POST':
        classe_opcao = request.form.get('classe')
        if classe_opcao in CLASSES:
            # carrega player já pronto
            player_data = session['player_data']
            
            classe_class = CLASSES[classe_opcao]
            classe = classe_class()
            
            # adiciona classe no dicionário final
            player_data['classe'] = classe.__class__.__name__
            
            # salva ficha final
            session['ficha'] = player_data
            session.pop('player_data', None)
            
            return redirect(url_for('mostrar_ficha'))
    
    return render_template('classe.html')

@app.route('/ficha')
def mostrar_ficha():
    if 'ficha' not in session:
        return redirect(url_for('index'))
    
    session['etapa_atual'] = 'ficha'
    return render_template('ficha.html', ficha=session['ficha'])

@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('index'))

@app.route('/voltar/<etapa>')
def voltar_etapa(etapa):
    if etapa in ETAPAS:
        current_index = ETAPAS.index(etapa)
        for step in ETAPAS[current_index + 1:]:
            if step in session:
                session.pop(step, None)
        
        session['etapa_atual'] = etapa
        return redirect(url_for(etapa))
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
