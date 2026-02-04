from database.database import get_connection

def criar_conserto(data, tecnico, cliente, servico, obs, modelo, garantia, valor, lucro):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO consertos
        (data, tecnico, cliente, servico_feito, observacoes, modelo, garantia, valor_cobrado, lucro)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (data, tecnico, cliente, servico, obs, modelo, garantia, valor, lucro))
    conn.commit()
    conn.close()


def listar_consertos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM consertos")
    dados = cursor.fetchall()
    conn.close()
    return dados


def buscar_por_cliente(nome_cliente):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM consertos
        WHERE cliente LIKE ?
    """, (f"%{nome_cliente}%",))
    dados = cursor.fetchall()
    conn.close()
    return dados


def atualizar_conserto(conserto_id, data, tecnico, cliente, servico, obs, modelo, garantia, valor, lucro):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE consertos SET
            data = ?, tecnico = ?, cliente = ?, servico_feito = ?,
            observacoes = ?, modelo = ?, garantia = ?, valor_cobrado = ?, lucro = ?
        WHERE id = ?
    """, (data, tecnico, cliente, servico, obs, modelo, garantia, valor, lucro, conserto_id))
    conn.commit()
    conn.close()


def deletar_conserto(conserto_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM consertos WHERE id = ?", (conserto_id,))
    conn.commit()
    conn.close()
