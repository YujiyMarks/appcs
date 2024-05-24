import streamlit as st

import sqlite3

dados = sqlite3.connect('bd_app.db')
cursor = dados.cursor()


st.set_page_config(page_title="Cadastro CS",page_icon=":gear:",)
st.sidebar.header("Cadastro")

st.title("Cadastro")


st.header("Inserção")

funcionario = st.text_input("Digite o nome do funcionário a ser cadastrado:")
if st.button("Cadastrar funcionário"):
    cursor.execute(f"INSERT INTO Funcionarios (nome) VALUES ('{funcionario}')")
    dados.commit()
    
cliente = st.text_input("Digite o nome do cliente a ser cadastrado:")
if st.button("Cadastrar cliente"):
    cursor.execute(f"INSERT INTO Clientes (nome) VALUES ('{cliente}')")
    dados.commit()


ufv = st.text_input("Digite o nome da usina a ser cadastrada e escolha o cliente:")
cursor.execute("SELECT * FROM Clientes")
lista = []
for linha in cursor.fetchall():
    lista.append(linha[1])
cliente_ufv = st.selectbox(f"Escolha o Cliente relativo a usina",lista)
if st.button("Cadastrar UFV"):
    cursor.execute(f"INSERT INTO Usinas (UFV, Cliente) VALUES ('{ufv}','{cliente_ufv}')")
    dados.commit()

equipamento = st.text_input("Digite o nome do equipamento a ser cadastrado:")
if st.button("Cadastrar equipamento"):
    cursor.execute(f"INSERT INTO Equipamentos (nome) VALUES ('{equipamento}')")
    dados.commit()


st.header("Remoção")

cursor.execute("SELECT * FROM Funcionarios")
lista = []
for linha in cursor.fetchall():
    lista.append(linha[1])
func_item = st.selectbox(f"Escolha o funcionário a ser removido",lista)
if st.button("Remover funcionário"):
    cursor.execute(f"DELETE FROM Funcionarios WHERE nome = '{func_item}'")
    dados.commit()

cursor.execute("SELECT * FROM Clientes")
lista = []
for linha in cursor.fetchall():
    lista.append(linha[1])
cliente_item = st.selectbox(f"Escolha o cliente a ser removido",lista)
if st.button("Remover cliente"):
    cursor.execute(f"DELETE FROM Clientes WHERE nome = '{cliente_item}'")
    dados.commit()

cursor.execute("SELECT * FROM Equipamentos")
lista = []
for linha in cursor.fetchall():
    lista.append(linha[1])
equip_item = st.selectbox(f"Escolha o equipamento a ser removido",lista)
if st.button("Remover equipamento"):
    cursor.execute(f"DELETE FROM Equipamentos WHERE nome = '{equip_item}'")
    dados.commit()
