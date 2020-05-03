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




app.run('127.0.0.1', 8000 )