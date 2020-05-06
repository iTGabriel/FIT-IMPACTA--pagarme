import requests

chave_api = "SUA CHAVE API PAGARME"


def realizar_transicao(dados):
  dados['api_key'] = chave_api
  r = requests.post('https://api.pagar.me/1/transactions', json=dados)
  r.headers['x-test'] = 'true'
  return [r, r.status_code]

def busca_todas_transacao():
  r = requests.get('https://api.pagar.me/1/payables', json = {"api_key": chave_api, "count": 50})
  return [r, r.status_code]

def busca_id_transacao(id):
  r = requests.get('https://api.pagar.me/1/transactions/'+str(id), json = {"api_key": chave_api})
  return [r, r.status_code]

def saldo(dados):
  r = requests.get('https://api.pagar.me/1/balance', json = {"api_key": chave_api})
  return [r, r.status_code]

def realizar_estorno(dados):
  dados['api_key'] = chave_api
  r = requests.post('https://api.pagar.me/1/transactions/'+dados['transaction_id']+'/refund', json=dados)
  r.headers['x-test'] = 'true'
  return [r, r.status_code]