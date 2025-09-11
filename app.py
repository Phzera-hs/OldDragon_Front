from flask import Flask, render_template, request, session, redirect, url_for, flash, abort
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
app.secret_key = os.environ.get('SECRET_KEY', 'dev_secret_key_change_in_production')
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
        try:
            raca_opcao = request.form.get('raca')
            nome = request.form.get('nome', '').strip()
            
            # Validate input
            if not nome or len(nome) > 50:
                flash("Nome inválido. Deve ter entre 1 e 50 caracteres.", "error")
                return render_template('raca.html', nome=nome, error="Nome inválido")
            
            if raca_opcao not in RACAS:
                flash("Raça inválida selecionada.", "error")
                return render_template('raca.html', nome=nome, error="Raça inválida")
            
            # Sanitize inputs
            session['nome'] = html.escape(nome)
            session['raca_opcao'] = raca_opcao
            
            # Special handling for Humano (alignment choice)
            if raca_opcao == '1':
                return redirect(url_for('escolher_alinhamento'))
            
            return redirect(url_for('escolher_estilo'))
            
        except Exception as e:
            flash(f"Erro ao processar raça: {str(e)}", "error")
            return render_template('raca.html', error="Erro interno")
    
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
        else:
            flash("Alinhamento inválido selecionado.", "error")
    
    return render_template('alinhamento.html')

@app.route('/estilo', methods=['GET', 'POST'])
def escolher_estilo():
    if 'nome' not in session or 'raca_opcao' not in session:
        return redirect(url_for('index'))
    
    session['etapa_atual'] = 'estilo'
    
    if request.method == 'POST':
        estilo_opcao = request.form.get('estilo')
        if estilo_opcao in ESTILOS:
            try:
                session['estilo_opcao'] = estilo_opcao
                
                # Create character instance
                nome = session['nome']
                raca_class = RACAS[session['raca_opcao']]
                
                # Handle Humano alignment
                if session['raca_opcao'] == '1':
                    raca = raca_class()
                    alinhamento_map = {'1': 'Neutro', '2': 'Ordem', '3': 'Caos'}
                    raca.alinhamento = alinhamento_map[session.get('alinhamento_opcao', '1')]
                else:
                    raca = raca_class()
                
                estilo_class = ESTILOS[estilo_opcao]
                player = estilo_class(nome, raca)
                
                # Store values for attribute assignment
                session['valores'] = player.valores
                session['atributos_restantes'] = list(player.atributos.keys())
                session['atributos_atribuidos'] = {}
                
                # For classic style, attributes are pre-set
                if estilo_opcao == '1':
                    player.aplicar_bonus_raca()
                    session['player_data'] = player.get_ficha_dict()
                    return redirect(url_for('escolher_classe'))
                else:
                    return redirect(url_for('definir_atributos'))
                    
            except Exception as e:
                flash(f"Erro ao criar personagem: {str(e)}", "error")
                return redirect(url_for('escolher_estilo'))
        else:
            flash("Estilo de geração inválido.", "error")
    
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
                # Update session
                session['valores'].remove(valor)
                session['atributos_restantes'].remove(atributo)
                session['atributos_atribuidos'][atributo] = valor
                session.modified = True
                
                if not session['atributos_restantes']:
                    return criar_personagem_final()
                
                return redirect(url_for('definir_atributos'))
            else:
                flash("Valor não disponível para seleção.", "error")
        else:
            flash("Selecione um valor válido.", "error")
    
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
    """Cria o personagem final com os atributos atribuídos"""
    try:
        nome = session['nome']
        raca_class = RACAS[session['raca_opcao']]
        
        # Handle Humano alignment
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
        
        # Store player data for class selection
        session['player_data'] = player.get_ficha_dict()
        
        # Clean up temporary data
        for key in ['valores', 'atributos_restantes', 'atributos_atribuidos']:
            session.pop(key, None)
        
        return redirect(url_for('escolher_classe'))
        
    except Exception as e:
        flash(f"Erro ao finalizar personagem: {str(e)}", "error")
        return redirect(url_for('index'))

@app.route('/classe', methods=['GET', 'POST'])

@app.route('/classe', methods=['GET', 'POST'])
def escolher_classe():
    if 'player_data' not in session:
        return redirect(url_for('index'))
    
    session['etapa_atual'] = 'classe'
    
    if request.method == 'POST':
        classe_opcao = request.form.get('classe')
        if classe_opcao in CLASSES:
            try:
                # Recreate character with class
                nome = session['nome']
                raca_class = RACAS[session['raca_opcao']]
                
                # Handle Humano alignment
                if session['raca_opcao'] == '1':
                    raca = raca_class()
                    alinhamento_map = {'1': 'Neutro', '2': 'Ordem', '3': 'Caos'}
                    raca.alinhamento = alinhamento_map[session.get('alinhamento_opcao', '1')]
                else:
                    raca = raca_class()
                
                estilo_class = ESTILOS[session['estilo_opcao']]
                player = estilo_class(nome, raca)
                
                # Apply attributes based on style
                if session['estilo_opcao'] in ['2', '3']:  # Aventureiro ou Heroico
                    # Use os atributos atribuídos pelo usuário
                    for atributo, valor in session.get('atributos_atribuidos', {}).items():
                        player.atributos[atributo] = valor
                else:  # Clássico - os atributos já foram definidos no construtor
                    pass
                
                player.aplicar_bonus_raca()
                
                # Add class
                classe_class = CLASSES[classe_opcao]
                classe = classe_class()
                player.escolher_classe(classe)
                
                # Store final character sheet
                session['ficha'] = player.get_ficha_dict()
                
                # Clean up
                for key in ['player_data']:
                    session.pop(key, None)
                
                return redirect(url_for('mostrar_ficha'))
                
            except Exception as e:
                flash(f"Erro ao adicionar classe: {str(e)}", "error")
        else:
            flash("Classe inválida selecionada.", "error")
    
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
    flash("Personagem resetado com sucesso.", "info")
    return redirect(url_for('index'))

@app.route('/voltar/<etapa>')
def voltar_etapa(etapa):
    """Permite voltar para etapas anteriores"""
    if etapa in ETAPAS:
        # Clear session data from subsequent steps
        current_index = ETAPAS.index(etapa)
        for step in ETAPAS[current_index + 1:]:
            if step in session:
                session.pop(step, None)
        
        session['etapa_atual'] = etapa
        return redirect(url_for(etapa))
    
    return redirect(url_for('index'))

@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error="Página não encontrada"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error="Erro interno do servidor"), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)