import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Servicos.interface_usuario import InterfaceUsuario


if __name__ == "__main__":
    interface = InterfaceUsuario()
    interface.executar()
