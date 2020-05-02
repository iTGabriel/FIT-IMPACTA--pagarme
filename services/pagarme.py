import requests

chave_api = "ak_test_PwBsJZ7NAfJCXvwNFKkPjLw7H1Wrps"

params = {
    "api_key": chave_api,
		"amount": "25100",
    "card_number": "4111111111111111",
    "card_cvv": "123",
    "card_expiration_date": "0922",
    "card_holder_name": "Morpheus Fishburne",
    "customer": {
      "external_id": "1",
      "name": "Morpheus Fishburne",
      "type": "individual",
      "country": "br",
      "email": "mopheus@nabucodonozor.com",
      "documents": [
        {
          "type": "cpf",
          "number": "30621143049"
        }
      ],
      "phone_numbers": ["+5511999998888", "+5511888889999"],
      "birthday": "1965-01-01"
    },
    "billing": {
      "name": "Trinity Moss",
      "address": {
        "country": "br",
        "state": "sp",
        "city": "Cotia",
        "neighborhood": "Rio Cotia",
        "street": "Rua Matrix",
        "street_number": "9999",
        "zipcode": "06714360"
      }
    },
    "shipping": {
      "name": "Neo Reeves",
      "fee": "1000",
      "delivery_date": "2000-12-21",
      "expedited": True,
      "address": {
        "country": "br",
        "state": "sp",
        "city": "Cotia",
        "neighborhood": "Rio Cotia",
        "street": "Rua Matrix",
        "street_number": "9999",
        "zipcode": "06714360"
      }
    },
    "items": [
      {
        "id": "r123",
        "title": "Red pill",
        "unit_price": "10000",
        "quantity": "1",
        "tangible": True
      },
      {
        "id": "b123",
        "title": "Blue pill",
        "unit_price": "10000",
        "quantity": "1",
        "tangible": True
      }
    ]
}

def realizar_transicao(dados):
  dados['api_key'] = chave_api

  return dados
  # r = requests.post('https://api.pagar.me/1/transactions', json=dados)
  # return r

def busca_todas_transacao():
  r = requests.get('https://api.pagar.me/1/payables', json = {"api_key": chave_api})
  return r

def busca_id_transacao(id):
  r = requests.get('https://api.pagar.me/1/transactions/'+str(id), json = {"api_key": chave_api})
  return r

def saldo(dados):
  r = requests.get('https://api.pagar.me/1/balance', json = {"api_key": chave_api})
  return r

# print(realizar_transicao({"params": 1}))
# print(busca_todas_transacao().json())
# a = busca_todas_transacao().json()
# print(saldo(params).json())
