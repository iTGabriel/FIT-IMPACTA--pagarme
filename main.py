import flask
from flask import Flask, escape, render_template, request, redirect, session, flash, url_for
import services.pagarme as api_pagarme

app = Flask(__name__)

@app.route('/')
def index():
    
    if request.args.get('message'):
        message = request.args.get('message')
    else:
        message = None

    try:
        lista_pagamentos = []
        pagamentos = api_pagarme.busca_todas_transacao()[0].json()
        
        verificador_id = []
        for pagamento in pagamentos: 
            transicao = {}
            dados_transacao = api_pagarme.busca_id_transacao(pagamento['transaction_id'])[0].json()
            transicao['id'] = dados_transacao['tid']

            if dados_transacao['status'] != "refunded":

                if dados_transacao['tid'] not in verificador_id:
                    verificador_id.append(dados_transacao['tid'])

                    # Tratamento do valor para que fique padrão BR
                    if  len(str(dados_transacao['amount'])) > 3:
                        transicao['preco'] = str(dados_transacao['amount'])[:-2]+",00"
                    else:
                        transicao['preco'] = str(dados_transacao['amount'])+",00"

                    transicao['name'] = dados_transacao['customer']['name']
                    transicao['email'] = dados_transacao['customer']['email']
                    
                    if dados_transacao['payment_method'] == 'credit_card':
                        transicao['pagamento'] = 'Cartão de crédito'
                        transicao['parcelas'] = pagamento['installment']

                    lista_pagamentos.append(transicao)
    except:
        lista_pagamentos = []
        message = "L"

    total = 0
    for pagamento_preco in lista_pagamentos:
        total += int(pagamento_preco['preco'][:-3]+"00")

    # Tratamento do valor para que fique padrão BR
    total = str(total)[:-2]+",00"
    
    return render_template('index.html', lista_pagamentos = lista_pagamentos, valor_total=total, message=message)



@app.route('/pay', methods=['POST'])
def pagamento():
    dados_pagamento = {}

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
    dados_pagamento['amount'] = array_itemCompra[1]
    dados_pagamento['items'] = [{
            "id": "1",
            "title": array_itemCompra[0],
            "unit_price": array_itemCompra[1],
            "quantity": "1",
            "tangible": True
    }]

    try:
        if request.form['credito']:
            dados_pagamento['card_number'] = request.form['credito']
            dados_pagamento['card_cvv'] = request.form['credito_cvv']
            dados_pagamento['card_holder_name'] = request.form['credito_input_credito_titular']

            dados_pagamento['installments'] = request.form['credito_parcela']

            data_tratada = request.form['credito_data_expiracao'].split('-') 
            dados_pagamento['card_expiration_date'] = data_tratada[1]+""+data_tratada[0]


        pagamento = api_pagarme.realizar_transicao(dados_pagamento)
        
        if pagamento[1] == 400:
            message = "Falha em realizar pagamento || "+ pagamento[0].json()['errors'][0]['message']
        if pagamento[1] == 200:
            message = "Sucesso em realizar pagamento"
    except:
        message = "Não foi possível capturar dados do cartão"

    return redirect(url_for('index', message=message))


@app.route('/estorno', methods=['POST'])
def estorno():

    dados_estorno = {}

    try:
        dados_estorno['transaction_id'] = request.form['estorno_id']
        dados_estorno['amount'] = int(str(request.form['estorno_valor'])+"00")

        estorno = api_pagarme.realizar_estorno(dados_estorno)

        if estorno[1] == 400:
            message = "Falha em realizar o estorn || "+ pagamento[0].json()['errors'][0]['message']
        if estorno[1] == 200:
            message = "Sucesso em realizar o estorno"

    except:
        message = "Não foi possível realizar o processo de estorno"

    return redirect(url_for('index', message=message))


app.run('127.0.0.1', 8000)