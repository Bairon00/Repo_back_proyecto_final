from dotenv import load_dotenv
from flask import Flask, jsonify, request
import mercadopago
import os

load_dotenv()

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['ENV'] = 'development'

ACCESS_TOKEN = os.getenv('TEST-8126dae5-3936-4bf6-bef6-7d911eb2f79b')
sdk = mercadopago.SDK(ACCESS_TOKEN)


@app.route('api/preference', methods=['POST'])
def generate_preference():

    name = request.json.get('name')
    quantity = request.json.get('quantity', 1)
    valor = request.json.get('valor')

    preference_data = {
        "items": [
            {
                "name": name,
                "quantity": 1,
                "valor": float(valor)
            }
        ]
    }

    preference_response = sdk.preference().create(preference_data)
    preference = preference_response["response"]

    return jsonify(preference), 200
