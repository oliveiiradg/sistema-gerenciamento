import customtkinter as ctk
from tkinter import ttk

def criar_tabela(parent):
    """
    Cria uma Treeview dentro do frame passado como parent.
    """
    # Frame da tabela ocupa o lado direito
    frame_tree = ctk.CTkFrame(parent)
    frame_tree.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    colunas = ["Data", "Técnico", "Cliente", "Serviço Feito", "Observações", 
               "Modelo", "Garantia", "Valor Cobrado", "Lucro"]

    tree = ttk.Treeview(frame_tree, columns=colunas, show="headings")
    tree.pack(fill="both", expand=True)

    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")

    return tree
