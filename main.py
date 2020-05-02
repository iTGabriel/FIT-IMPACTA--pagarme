import flask
from flask import Flask, escape, render_template, request, redirect, session, flash, url_for
import services.pagarme as api_pagarme

app = Flask(__name__)

@app.route('/')
def index():
    historicos_pagamentos = []
    pagamentos = api_pagarme.busca_todas_transacao().json()
    
    for pagamento in pagamentos:
        historico_transacao = api_pagarme.busca_id_transacao(pagamento['transaction_id']).json()
        historicos_pagamentos.append(historico_transacao)
    
    return render_template('index.html', lista_pagamentos = historicos_pagamentos)




app.run('127.0.0.1', 8000 )