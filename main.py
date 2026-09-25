"""
Ponto de entrada do Gerenciador de Notas.

Executar com:
    python main.py
"""

import tkinter as tk

from interface import AppGerenciadorNotas


def main() -> None:
    root = tk.Tk()
    AppGerenciadorNotas(root)
    root.mainloop()


if __name__ == "__main__":
    main()
