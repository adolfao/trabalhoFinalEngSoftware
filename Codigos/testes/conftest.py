# Arquivo: testes/conftest.py
import sys
import os

# Adiciona o diretório 'Codigos' ao path para que o pytest encontre os módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))