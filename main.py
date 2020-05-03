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
    # dados_pagamento['amount'] = 
    if request.form['credito']:
        dados_pagamento['card_number'] = request.form['credito']
        dados_pagamento['card_cvv'] = request.form['credito_cvv']
        dados_pagamento['card_holder_name'] = request.form['credito_input_credito_titular']
        dados_pagamento['card_expiration_date'] = request.form['credito_data_expiracao']

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

    dados_pagamento['items'] = {
            "id": "1",
            "title": request.form['item_compra'].split('valor=')[0],
            "unit_price": request.form['item_compra'].split('valor=')[1],
            "quantity": "1",
            "tangible": True
    }


    print(dados_pagamento)

    return render_template('index.html')



app.run('127.0.0.1', 8000 )