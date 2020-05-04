import flask
from flask import Flask, escape, render_template, request, redirect, session, flash, url_for
import services.pagarme as api_pagarme

app = Flask(__name__)

@app.route('/')
def index():
    lista_pagamentos = []
    pagamentos = api_pagarme.busca_todas_transacao().json()
    
    for pagamento in pagamentos: 
        transicao = {}
        dados_transacao = api_pagarme.busca_id_transacao(pagamento['transaction_id']).json()
        transicao['id'] = dados_transacao['tid']
        
        if  len(str(dados_transacao['amount'])) > 3:
            transicao['preco'] = str(dados_transacao['amount'])[:-2]+",00"
        else:
            transicao['preco'] = str(dados_transacao['amount'])+",00"

        transicao['name'] = dados_transacao['customer']['name']
        transicao['email'] = dados_transacao['customer']['email']
        
        if dados_transacao['payment_method'] == 'credit_card':
            transicao['pagamento'] = 'Cartão de crédito'
        else:
            transicao['pagamento'] = 'Boleto'

        lista_pagamentos.append(transicao)
    
    return render_template('index.html', lista_pagamentos = lista_pagamentos)


@app.route('/pay', methods=['POST'])
def pagamento():
    dados_pagamento = {}

    print(request.form['cpf'])

    if request.form['numero_contato'] and len(request.form['numero_contato']) in [10, 12]:
        telefone = request.form['numero_contato']
    else:
        telefone = "1100000000"


    dados_pagamento['customer'] = { 
        'external_id' : "1",
        'name' : request.form['nome'],
        'type' : 'individual',
        "country": "br",
        "email": request.form['email'],
        "documents": [{
            "type": "cpf",
            "number": request.form['cpf']
        }],
        "phone_numbers": ["+55"+telefone],
        "birthday": "1965-01-01"
    }

    dados_pagamento['billing'] = {
        "name": "BKNS - Puppy",
        "address": {
            "country": "br",
            "state": "sp",
            "city": "São Paulo",
            "neighborhood": "São Paulo",
            "street": "Av. Paulista",
            "street_number": "9999",
            "zipcode": "01311922"
        }
    }

    array_itemCompra = request.form['item_compra'].split('valor=')
    dados_pagamento['amount'] = array_itemCompra[1]+"00"
    dados_pagamento['items'] = [{
            "id": "1",
            "title": array_itemCompra[0],
            "unit_price": array_itemCompra[1]+"00",
            "quantity": "1",
            "tangible": True
    }]

    try:
        if request.form['credito']:
            # dados_pagamento['card_id'] = 1
            dados_pagamento['card_number'] = request.form['credito']
            dados_pagamento['card_cvv'] = request.form['credito_cvv']
            dados_pagamento['card_holder_name'] = request.form['credito_input_credito_titular']

            data_tratada = request.form['credito_data_expiracao'].split('-') 
            dados_pagamento['card_expiration_date'] = data_tratada[1]+""+data_tratada[0]

        # if request.form['debito']:

        api_pagarme.realizar_transicao(dados_pagamento)
        print("Pagamento feito")
    except:
        print("Não foi possível capturar dados do cartão")

    return render_template('index.html')



app.run('127.0.0.1', 8000 )