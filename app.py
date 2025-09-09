from flask import Flask, render_template, request, session, redirect, url_for
import sys
import os

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
app.secret_key = 'your_secret_key_here'

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

@app.route('/')
def index():
    # Clear session when starting over
    session.clear()
    return render_template('index.html')

@app.route('/raca', methods=['GET', 'POST'])
def escolher_raca():
    if request.method == 'POST':
        raca_opcao = request.form.get('raca')
        nome = request.form.get('nome')
        
        if raca_opcao in RACAS and nome:
            session['nome'] = nome
            session['raca_opcao'] = raca_opcao
            
            # Special handling for Humano (alignment choice)
            if raca_opcao == '1':
                return redirect(url_for('escolher_alinhamento'))
            
            return redirect(url_for('escolher_estilo'))
        
        return render_template('raca.html', error="Nome ou raça inválidos")
    
    # If GET request, check if we have a name from previous step
    nome = session.get('nome', '')
    return render_template('raca.html', nome=nome)

@app.route('/alinhamento', methods=['GET', 'POST'])
def escolher_alinhamento():
    if 'nome' not in session or session.get('raca_opcao') != '1':
        return redirect(url_for('index'))
    
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
    
    if request.method == 'POST':
        estilo_opcao = request.form.get('estilo')
        if estilo_opcao in ESTILOS:
            session['estilo_opcao'] = estilo_opcao
            
            # For classic style, go directly to class selection
            if estilo_opcao == '1':
                return redirect(url_for('escolher_classe'))
            else:
                # For styles that need attribute assignment
                return redirect(url_for('definir_atributos'))
    
    return render_template('estilo.html')

@app.route('/atributos', methods=['GET', 'POST'])
def definir_atributos():
    if 'nome' not in session or 'raca_opcao' not in session or 'estilo_opcao' not in session:
        return redirect(url_for('index'))
    
    # Initialize attribute assignment if not already started
    if 'valores' not in session:
        # Create temporary player to get values
        nome = session['nome']
        raca_class = RACAS[session['raca_opcao']]
        
        # Special handling for Humano
        if session['raca_opcao'] == '1':
            raca = raca_class()
            alinhamento_map = {'1': 'Neutro', '2': 'Ordem', '3': 'Caos'}
            raca.alinhamento = alinhamento_map[session.get('alinhamento_opcao', '1')]
        else:
            raca = raca_class()
        
        estilo_class = ESTILOS[session['estilo_opcao']]
        player = estilo_class(nome, raca)
        
        session['valores'] = player.valores
        session['atributos_restantes'] = list(player.atributos.keys())
        session['atributos_atribuidos'] = {}
    
    if request.method == 'POST':
        atributo = request.form.get('atributo')
        valor_str = request.form.get('valor')
        
        # Validate and process
        if atributo and valor_str and valor_str.isdigit():
            valor = int(valor_str)
            valores = session.get('valores', [])
            
            if valor in valores:
                # Update session
                session['valores'].remove(valor)
                session['atributos_restantes'].remove(atributo)
                session['atributos_atribuidos'][atributo] = valor
                session.modified = True
                
                if not session['atributos_restantes']:
                    # All attributes assigned, proceed to class selection
                    return redirect(url_for('escolher_classe_final'))
                
                # Continue with next attribute
                return redirect(url_for('definir_atributos'))
    
    # Get current attribute to assign
    atributos_restantes = session.get('atributos_restantes', [])
    valores = session.get('valores', [])
    
    if not atributos_restantes:
        return redirect(url_for('escolher_classe_final'))
    
    atributo_atual = atributos_restantes[0]
    
    return render_template('atributos.html', 
                         atributo=atributo_atual,
                         valores=valores,
                         atributos_restantes=atributos_restantes)

@app.route('/classe', methods=['GET', 'POST'])
def escolher_classe():
    if 'estilo_opcao' not in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        classe_opcao = request.form.get('classe')
        if classe_opcao in CLASSES:
            # Create the character (for classic style)
            nome = session['nome']
            raca_class = RACAS[session['raca_opcao']]
            
            # Special handling for Humano
            if session['raca_opcao'] == '1':
                raca = raca_class()
                alinhamento_map = {'1': 'Neutro', '2': 'Ordem', '3': 'Caos'}
                raca.alinhamento = alinhamento_map[session.get('alinhamento_opcao', '1')]
            else:
                raca = raca_class()
            
            estilo_class = ESTILOS[session['estilo_opcao']]
            player = estilo_class(nome, raca)
            
            classe_class = CLASSES[classe_opcao]
            classe = classe_class()
            player.escolher_classe(classe)
            
            session['ficha'] = {
                'nome': player.nome,
                'raca': player.raca.nome,
                'classe': player.classe.nome,
                'nivel': player.classe.nivel,
                'habilidades': player.classe.habilidades,
                'pontos_vida': player.classe.pontos_de_vida,
                'movimento': player.raca.movimento,
                'infravisao': player.raca.infravisao,
                'alinhamento': player.raca.alinhamento,
                'atributos': player.atributos
            }
            
            return redirect(url_for('mostrar_ficha'))
    
    return render_template('classe.html')

@app.route('/classe_final', methods=['GET', 'POST'])
def escolher_classe_final():
    if 'atributos_atribuidos' not in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        classe_opcao = request.form.get('classe')
        if classe_opcao in CLASSES:
            # Recreate the character with assigned attributes
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
            
            # Apply assigned attributes
            for atributo, valor in session['atributos_atribuidos'].items():
                player.atributos[atributo] = valor
            
            player.aplicar_bonus_raca()
            
            classe_class = CLASSES[classe_opcao]
            classe = classe_class()
            player.escolher_classe(classe)
            
            session['ficha'] = {
                'nome': player.nome,
                'raca': player.raca.nome,
                'classe': player.classe.nome,
                'nivel': player.classe.nivel,
                'habilidades': player.classe.habilidades,
                'pontos_vida': player.classe.pontos_de_vida,
                'movimento': player.raca.movimento,
                'infravisao': player.raca.infravisao,
                'alinhamento': player.raca.alinhamento,
                'atributos': player.atributos
            }
            
            # Clean up session
            session_keys_to_remove = ['valores', 'atributos_restantes', 'atributos_atribuidos']
            for key in session_keys_to_remove:
                session.pop(key, None)
            
            return redirect(url_for('mostrar_ficha'))
    
    return render_template('classe.html')

@app.route('/ficha')
def mostrar_ficha():
    if 'ficha' not in session:
        return redirect(url_for('index'))
    
    return render_template('ficha.html', ficha=session['ficha'])

@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)