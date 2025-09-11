import os

def limpar_tela():
    """Limpa a tela do console de forma cross-platform"""
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Linux, macOS, etc.
        os.system('clear')

def mostrar_mensagem(mensagem, tipo="info"):
    """Exibe mensagens formatadas no console"""
    cores = {
        "info": "\033[94m",    # Azul
        "success": "\033[92m", # Verde
        "warning": "\033[93m", # Amarelo
        "error": "\033[91m",   # Vermelho
        "reset": "\033[0m"     # Reset
    }
    
    print(f"{cores.get(tipo, '')}{mensagem}{cores['reset']}")

def pedir_entrada(mensagem, tipo="string"):
    """Solicita entrada do usuário com validação básica"""
    try:
        if tipo == "int":
            return int(input(mensagem))
        elif tipo == "float":
            return float(input(mensagem))
        else:
            return input(mensagem).strip()
    except (ValueError, EOFError):
        return None