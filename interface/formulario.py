import customtkinter as ctk

def criar_formulario(parent):
    frame = ctk.CTkFrame(parent)
    frame.pack(fill="y", padx=10, pady=10)

    # Lista de campos
    campos = [
        "Data", "Técnico", "Cliente", "Serviço Feito",
        "Observações", "Modelo", "Garantia", "Valor Cobrado", "Lucro"
    ]

    entries = {}

    for campo in campos:
        label = ctk.CTkLabel(frame, text=campo, anchor="w")
        label.pack(fill="x", padx=5, pady=(5,0))

        entry = ctk.CTkEntry(frame)
        entry.pack(fill="x", padx=5, pady=(0,5))
        entries[campo] = entry

    # Botões lado a lado
    frame_botoes = ctk.CTkFrame(frame)
    frame_botoes.pack(fill="x", pady=(10,0))

    btn_salvar = ctk.CTkButton(frame_botoes, text="💾 Salvar")
    btn_editar = ctk.CTkButton(frame_botoes, text="✏️ Editar")
    btn_deletar = ctk.CTkButton(frame_botoes, text="🗑️ Deletar")

    btn_salvar.pack(side="left", expand=True, padx=5)
    btn_editar.pack(side="left", expand=True, padx=5)
    btn_deletar.pack(side="left", expand=True, padx=5)

    return entries, btn_salvar, btn_editar, btn_deletar
