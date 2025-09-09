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
    
    return render_template('raca.html')

@app.route('/alinhamento', methods=['GET', 'POST'])
def escolher_alinhamento():
    if 'nome' not in session or session['raca_opcao'] != '1':
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
            return redirect(url_for('escolher_classe'))
    
    return render_template('estilo.html')

@app.route('/classe', methods=['GET', 'POST'])
def escolher_classe():
    if 'estilo_opcao' not in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        classe_opcao = request.form.get('classe')
        if classe_opcao in CLASSES:
            # Create the character
            nome = session['nome']
            raca_class = RACAS[session['raca_opcao']]
            
            # Special handling for Humano
            if session['raca_opcao'] == '1':
                raca = raca_class()
                # Set alignment based on user choice
                alinhamento_map = {'1': 'Neutro', '2': 'Ordem', '3': 'Caos'}
                raca.alinhamento = alinhamento_map[session.get('alinhamento_opcao', '1')]
            else:
                raca = raca_class()
            
            estilo_class = ESTILOS[session['estilo_opcao']]
            player = estilo_class(nome, raca)
            
            # Handle attribute assignment for styles that need it
            if session['estilo_opcao'] in ['2', '3']:
                # For web, we need to handle this differently
                # Store values in session and create a multi-step process
                session['valores'] = player.valores
                session['atributos_restantes'] = list(player.atributos.keys())
                return redirect(url_for('definir_atributos'))
            
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

@app.route('/atributos', methods=['GET', 'POST'])
def definir_atributos():
    if 'valores' not in session or 'atributos_restantes' not in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        atributo = request.form.get('atributo')
        valor = request.form.get('valor')
        
        # Validate and process
        if atributo and valor and valor.isdigit():
            valor_int = int(valor)
            if valor_int in session['valores']:
                # Update session
                session['valores'].remove(valor_int)
                session['atributos_restantes'].remove(atributo)
                session.setdefault('atributos_atribuidos', {})[atributo] = valor_int
                
                if not session['atributos_restantes']:
                    # All attributes assigned, proceed to class selection
                    return redirect(url_for('escolher_classe_final'))
    
    # Get current attribute to assign
    atributo_atual = session['atributos_restantes'][0] if session['atributos_restantes'] else None
    
    return render_template('atributos.html', 
                         atributo=atributo_atual,
                         valores=session['valores'])

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
            for key in ['valores', 'atributos_restantes', 'atributos_atribuidos']:
                session.pop(key, None)
            
            return redirect(url_for('mostrar_ficha'))
    
    return render_template('classe.html')

@app.route('/ficha')
def mostrar_ficha():
    if 'ficha' not in session:
        return redirect(url_for('index'))
    
    return render_template('ficha.html', ficha=session['ficha'])

if __name__ == '__main__':
    app.run(debug=True)