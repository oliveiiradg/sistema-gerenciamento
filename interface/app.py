import customtkinter as ctk
from tkinter import ttk, messagebox
import config

from dados import (
    ler_dados,
    adicionar_registro,
    atualizar_registro,
    deletar_registro
)

from interface.formulario import criar_formulario
from interface.titulo import criar_titulo


# ================= FUNÇÃO AUXILIAR =================
def parse_moeda(valor):
    if valor is None:
        return 0.0

    valor = str(valor).strip()
    if valor == "":
        return 0.0

    # padrão BR -> float seguro
    if "," in valor and "." in valor:
        valor = valor.replace(".", "").replace(",", ".")
    else:
        valor = valor.replace(",", ".")

    try:
        return float(valor)
    except ValueError:
        return 0.0


def formatar_moeda(valor):
    return f'R$ {valor:,.2f}'.replace(",", "X").replace(".", ",").replace("X", ".")


def iniciar_app():
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title(config.NOME_SISTEMA)
    app.geometry(f"{config.LARGURA_JANELA}x{config.ALTURA_JANELA}")

    frame_principal = ctk.CTkFrame(app)
    frame_principal.pack(fill="both", expand=True, padx=20, pady=20)

    frame_conteudo = ctk.CTkFrame(frame_principal)
    frame_conteudo.pack(fill="both", expand=True)

    criar_titulo(frame_conteudo)

    frame_formulario = ctk.CTkFrame(frame_conteudo, width=250)
    frame_formulario.pack(side="left", fill="y", padx=5, pady=5)

    entries, btn_salvar, btn_editar, btn_deletar = criar_formulario(frame_formulario)

    cols = [
        "ID","Data","Técnico","Cliente","Serviço Feito",
        "Observações","Modelo","Garantia","Valor Cobrado","Lucro"
    ]

    frame_tree = ctk.CTkFrame(frame_conteudo)
    frame_tree.pack(side="right", fill="both", expand=True, padx=5, pady=5)

    tree = ttk.Treeview(frame_tree, columns=cols, show="headings")
    tree.pack(fill="both", expand=True)

    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=110, anchor="center")

    tree.column("ID", width=50)

    frame_totais = ctk.CTkFrame(frame_tree)
    frame_totais.pack(fill="x", pady=5)

    label_total_cobrado = ctk.CTkLabel(frame_totais, text="Total Cobrado: R$ 0,00", font=ctk.CTkFont(weight="bold"))
    label_total_lucro = ctk.CTkLabel(frame_totais, text="Total Lucro: R$ 0,00", font=ctk.CTkFont(weight="bold"))

    label_total_cobrado.pack(side="left", padx=10)
    label_total_lucro.pack(side="left", padx=50)

    editar_id = None

    def atualizar_treeview():
        total_valor = 0.0
        total_lucro = 0.0

        tree.delete(*tree.get_children())

        for r in ler_dados():
            valor = r["valor_cobrado"] or 0.0
            lucro = r["lucro"] or 0.0

            tree.insert("", "end", values=[
                r["id"],
                r["data"],
                r["tecnico"],
                r["cliente"],
                r["servico_feito"],
                r["observacoes"],
                r["modelo"],
                r["garantia"],
                formatar_moeda(valor),
                formatar_moeda(lucro)
            ])

            total_valor += valor
            total_lucro += lucro

        label_total_cobrado.configure(text=f"Total Cobrado: {formatar_moeda(total_valor)}")
        label_total_lucro.configure(text=f"Total Lucro: {formatar_moeda(total_lucro)}")

    def salvar():
        nonlocal editar_id
        dados = {}

        for campo in entries:
            valor = entries[campo].get().strip()

            if campo in ["Valor Cobrado", "Lucro"]:
                dados[campo] = parse_moeda(valor)

            elif campo == "Garantia":
                if valor == "":
                    valor = "Sem garantia"
                elif valor.isdigit():
                    valor = f"{valor} dias"
                dados[campo] = valor

            else:
                dados[campo] = valor

        if editar_id is None:
            adicionar_registro(dados)
        else:
            atualizar_registro(editar_id, dados)
            editar_id = None

        atualizar_treeview()

        for campo in entries:
            entries[campo].delete(0, ctk.END)

    def editar():
        nonlocal editar_id
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Erro", "Selecione um registro")
            return

        valores = tree.item(selected[0])["values"]
        editar_id = valores[0]

        for i, col in enumerate(cols[1:]):
            entries[col].delete(0, ctk.END)

            if col in ["Valor Cobrado", "Lucro"]:
                entries[col].insert(0, parse_moeda(valores[i + 1]))
            else:
                entries[col].insert(0, valores[i + 1])

    def deletar():
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Erro", "Selecione um registro")
            return

        if messagebox.askyesno("Confirmação", "Deseja realmente deletar?"):
            deletar_registro(tree.item(selected[0])["values"][0])
            atualizar_treeview()

    btn_salvar.configure(command=salvar)
    btn_editar.configure(command=editar)
    btn_deletar.configure(command=deletar)

    atualizar_treeview()
    app.mainloop()
