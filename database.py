import sqlite3
import csv
import random
import string
from pathlib import Path

DB_FILE = 'clientes.db'
CSV_FILE = 'clientes.csv'

def init_db():
    if not Path(DB_FILE).is_file():
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('''CREATE TABLE clientes (
                        id TEXT PRIMARY KEY,
                        nome TEXT NOT NULL,
                        telefone TEXT,
                        endereco TEXT,
                        valor_devedor REAL
                     )''')
        conn.commit()
        conn.close()
        populate_db()

#Função para gerar IDs
def criar_id():
    letras = ''.join(random.choices(string.ascii_uppercase, k=3))  # Três letras aleatórias
    numeros = ''.join(random.choices(string.digits, k=2))  # Dois números aleatórios
    return letras + numeros

def populate_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    with open(CSV_FILE, 'r') as file:
        reader = csv.reader(file)
        next(reader)  
        for row in reader:
            cliente_id = criar_id()  # Gerar um novo ID personalizado
            c.execute("INSERT INTO clientes (id, nome, telefone, endereco, valor_devedor) VALUES (?, ?, ?, ?, ?)", 
                      (cliente_id, row[0], row[1], row[2], row[3]))
    conn.commit()
    conn.close()

def get_all_clients():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM clientes")
    clients = c.fetchall()
    conn.close()
    return clients

def add_client(nome, telefone, endereco, valor_devedor):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    cliente_id = criar_id()  # Gerar um novo ID personalizado
    c.execute("INSERT INTO clientes (id, nome, telefone, endereco, valor_devedor) VALUES (?, ?, ?, ?, ?)",
              (cliente_id, nome, telefone, endereco, valor_devedor))
    conn.commit()
    conn.close()

def update_client(client_id, nome, telefone, endereco, valor_devedor):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE clientes SET nome=?, telefone=?, endereco=?, valor_devedor=? WHERE id=?",
              (nome, telefone, endereco, valor_devedor, client_id))
    conn.commit()
    conn.close()

def get_client_by_id(client_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM clientes WHERE id=?", (client_id,))
    client = c.fetchone()
    conn.close()
    if client:
        return {
            'id': client[0],
            'nome': client[1],
            'telefone': client[2],
            'endereco': client[3],
            'valor_devedor': client[4]
        }
    else:
        return None