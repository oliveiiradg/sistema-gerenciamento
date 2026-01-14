import os
import pandas as pd

PASTA_DADOS = "dados"
ARQUIVO_EXCEL = os.path.join(PASTA_DADOS, "controle.xlsx")

def criar_excel_base():
    os.makedirs(PASTA_DADOS, exist_ok=True)
    colunas = [
        "Mês", "Data", "Técnico", "Cliente", "Serviço Feito",
        "Observações", "Modelo", "Garantia", "Valor Cobrado", "Lucro"
    ]
    if not os.path.exists(ARQUIVO_EXCEL):
        df = pd.DataFrame(columns=colunas)
        df.to_excel(ARQUIVO_EXCEL, index=False)
        print("Arquivo Excel criado com sucesso!")

def ler_dados():
    if not os.path.exists(ARQUIVO_EXCEL):
        criar_excel_base()
    df = pd.read_excel(ARQUIVO_EXCEL, engine="openpyxl")
    df["Valor Cobrado"] = pd.to_numeric(df["Valor Cobrado"], errors="coerce").fillna(0)
    df["Lucro"] = pd.to_numeric(df["Lucro"], errors="coerce").fillna(0)
    return df

def adicionar_registro(registro: dict):
    df = ler_dados()
    df = pd.concat([pd.DataFrame([registro]), df], ignore_index=True)
    salvar_excel(df)

def atualizar_registro(indice, registro: dict):
    df = ler_dados()
    for key, value in registro.items():
        df.at[indice, key] = value
    salvar_excel(df)

def deletar_registro(indice):
    df = ler_dados()
    df = df.drop(indice).reset_index(drop=True)
    salvar_excel(df)

def salvar_excel(df):
    df["Valor Cobrado"] = pd.to_numeric(df["Valor Cobrado"], errors="coerce").fillna(0)
    df["Lucro"] = pd.to_numeric(df["Lucro"], errors="coerce").fillna(0)
    df.to_excel(ARQUIVO_EXCEL, index=False)