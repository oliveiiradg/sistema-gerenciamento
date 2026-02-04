from database.database import criar_tabelas
from interface.app import iniciar_app

def main():
    criar_tabelas()   # 🔥 ESSENCIAL
    iniciar_app()

if __name__ == "__main__":
    main()
