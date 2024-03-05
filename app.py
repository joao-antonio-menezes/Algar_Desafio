from flask import Flask, render_template, request, redirect, url_for
from database import init_db, get_all_clients, add_client, update_client, get_client_by_id

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro_cliente', methods=['GET', 'POST'])
def cadastro_cliente():
    if request.method == 'POST':
        nome = request.form['name']
        telefone = request.form['phone']
        endereco = request.form['address']
        valor_devedor = request.form['debt']
        add_client(nome, telefone, endereco, valor_devedor)
        return redirect(url_for('index'))
    return render_template('cadastro_cliente.html')

@app.route('/exibir_clientes')
def exibir_clientes():
    clientes = get_all_clients()
    return render_template('exibir_clientes.html', clientes=clientes)

@app.route('/alterar_cliente', methods=['GET', 'POST'])
def alterar_cliente():
    if request.method == 'POST':
        cliente = get_client_by_id(request.form['client-id'])
        change_option = request.form['change-option']
        new_value = request.form['new-value']
        
        if change_option == 'phone':
            cliente['telefone'] = new_value
        elif change_option == 'address':
            cliente['endereco'] = new_value
        
        update_client(cliente['id'],cliente['nome'], cliente['telefone'], cliente['endereco'], cliente['valor_devedor'])
        return redirect(url_for('exibir_clientes'))
    else:
        return render_template('alterar_cliente.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
