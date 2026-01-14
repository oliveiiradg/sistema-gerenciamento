import customtkinter as ctk
from tkinter import ttk, messagebox
import config
import pandas as pd
from dados_excel import ler_dados, adicionar_registro, atualizar_registro, deletar_registro
from interface.formulario import criar_formulario
from interface.titulo import criar_titulo

def iniciar_app():
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title(config.NOME_SISTEMA)
    app.geometry(f"{config.LARGURA_JANELA}x{config.ALTURA_JANELA}")

    # --- Frame principal ---
    frame_principal = ctk.CTkFrame(app)
    frame_principal.pack(fill="both", expand=True, padx=20, pady=20)

    # --- Frame conteúdo ---
    frame_conteudo = ctk.CTkFrame(frame_principal)
    frame_conteudo.pack(fill="both", expand=True)

    # --- Título ---
    criar_titulo(frame_conteudo)

    # --- Formulário ---
    frame_formulario = ctk.CTkFrame(frame_conteudo, width=250)
    frame_formulario.pack(side="left", fill="y", padx=5, pady=5)
    entries, btn_salvar, btn_editar, btn_deletar = criar_formulario(frame_formulario)

    # --- Treeview ---
    cols = ["Mês","Data","Técnico","Cliente","Serviço Feito","Observações","Modelo","Garantia","Valor Cobrado","Lucro"]
    frame_tree = ctk.CTkFrame(frame_conteudo)
    frame_tree.pack(side="right", fill="both", expand=True, padx=5, pady=5)

    tree = ttk.Treeview(frame_tree, columns=cols, show="headings")
    tree.pack(fill="both", expand=True, side="top")

    vsb = ttk.Scrollbar(frame_tree, orient="vertical", command=tree.yview)
    vsb.pack(side="right", fill="y")
    tree.configure(yscrollcommand=vsb.set)

    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")

    # --- Totais ---
    frame_totais = ctk.CTkFrame(frame_tree, height=30)
    frame_totais.pack(fill="x", side="bottom", pady=(5,5))
    label_total_cobrado = ctk.CTkLabel(frame_totais, text="Total Cobrado: R$ 0.00", font=ctk.CTkFont(weight="bold"))
    label_total_lucro = ctk.CTkLabel(frame_totais, text="Total Lucro: R$ 0.00", font=ctk.CTkFont(weight="bold"))
    label_total_cobrado.pack(side="left", padx=(10,0))
    label_total_lucro.pack(side="left", padx=(50,0))

    # --- Funções ---
    editar_index = None

    def atualizar_treeview():
        total_valor = 0
        total_lucro = 0
        for item in tree.get_children():
            tree.delete(item)
        df = ler_dados()
        for _, row in df.iterrows():
            tree.insert("", "end", values=[
                row["Data"],
                row["Técnico"],
                row["Cliente"],
                row["Serviço Feito"],
                row["Observações"],
                row["Modelo"],
                row["Garantia"],
                f'R$ {row["Valor Cobrado"]:,.2f}',
                f'R$ {row["Lucro"]:,.2f}'
            ])
            total_valor += row["Valor Cobrado"]
            total_lucro += row["Lucro"]

        label_total_cobrado.configure(text=f"Total Cobrado: R$ {total_valor:,.2f}")
        label_total_lucro.configure(text=f"Total Lucro: R$ {total_lucro:,.2f}")

    def salvar():
        nonlocal editar_index
        dados = {}
        for campo in entries:
            valor = entries[campo].get().replace("R$","").strip() if campo in ["Valor Cobrado","Lucro"] else entries[campo].get()
            dados[campo] = valor
        if editar_index is None:
            adicionar_registro(dados)
        else:
            atualizar_registro(editar_index, dados)
            editar_index = None
        atualizar_treeview()
        for campo in entries:
            entries[campo].delete(0, ctk.END)

    def editar():
        nonlocal editar_index
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Erro","Selecione um registro para editar!")
            return
        editar_index = tree.index(selected[0])
        for i, col in enumerate(cols):
            entries[col].delete(0, ctk.END)
            entries[col].insert(0, tree.item(selected[0])["values"][i])

    def deletar():
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Erro","Selecione um registro para deletar!")
            return
        index = tree.index(selected[0])
        if messagebox.askyesno("Confirmação","Deseja realmente deletar este registro?"):
            deletar_registro(index)
            atualizar_treeview()

    # --- Conecta botões ---
    btn_salvar.configure(command=salvar)
    btn_editar.configure(command=editar)
    btn_deletar.configure(command=deletar)

    # --- Inicializa ---
    atualizar_treeview()
    app.mainloop()