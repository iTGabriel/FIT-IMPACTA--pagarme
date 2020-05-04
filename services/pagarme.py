import requests

chave_api = "SUA CHAVE API PAGARME"



def realizar_transicao(dados):
  dados['api_key'] = chave_api
  r = requests.post('https://api.pagar.me/1/transactions', json=dados)
  r.headers['x-test'] = 'true'
  print("\n\n", r.json())
  return r

def busca_todas_transacao():
  r = requests.get('https://api.pagar.me/1/payables', json = {"api_key": chave_api})
  return r

def busca_id_transacao(id):
  r = requests.get('https://api.pagar.me/1/transactions/'+str(id), json = {"api_key": chave_api})
  return r

def saldo(dados):
  r = requests.get('https://api.pagar.me/1/balance', json = {"api_key": chave_api})
  return r