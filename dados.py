from database.consertos_crud import (
    criar_conserto,
    listar_consertos,
    buscar_por_cliente,
    atualizar_conserto,
    deletar_conserto
)

def ler_dados():
    return listar_consertos()

def adicionar_registro(registro: dict):
    criar_conserto(
        registro["Data"],
        registro["Técnico"],
        registro["Cliente"],
        registro["Serviço Feito"],
        registro.get("Observações", ""),
        registro.get("Modelo", ""),
        registro.get("Garantia", ""),
        float(registro["Valor Cobrado"]),
        float(registro.get("Lucro", 0))
    )

def atualizar_registro(id_conserto: int, registro: dict):
    atualizar_conserto(
        id_conserto,
        registro["Data"],
        registro["Técnico"],
        registro["Cliente"],
        registro["Serviço Feito"],
        registro.get("Observações", ""),
        registro.get("Modelo", ""),
        registro.get("Garantia", ""),
        float(registro["Valor Cobrado"]),
        float(registro.get("Lucro", 0))
    )

def deletar_registro(id_conserto: int):
    deletar_conserto(id_conserto)
