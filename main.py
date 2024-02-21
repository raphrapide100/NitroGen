from flask import Flask, jsonify
import requests
import random
import string

app = Flask(__name__)
if __name__ == "__main__":
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)


# Tes fonctions existantes
def generate_random_code(length=18):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def check_code(code):
    url = f"https://discord.com/api/v9/entitlements/gift-codes/{code}"
    response = requests.get(url)
    return response.status_code == 200

WEBHOOK_URL_VALID = 'https://discord.com/api/webhooks/TON_WEBHOOK_VALID'
WEBHOOK_URL_INVALID = 'https://discord.com/api/webhooks/TON_WEBHOOK_INVALID'

def send_to_webhook(code, is_valid=True):
    url = WEBHOOK_URL_VALID if is_valid else WEBHOOK_URL_INVALID
    content = f"{'Code valide trouvé: discord.gift/' if is_valid else 'Code invalide: '}{code}"
    data = {"content": content, "username": "Vérificateur de code"}
    response = requests.post(url, json=data)
    return response.status_code

# Route Flask pour générer et vérifier un code
@app.route('/generate_and_check_code')
def generate_and_check_code():
    code = generate_random_code()
    if check_code(code):
        send_to_webhook(code, is_valid=True)
        return jsonify({"message": "Code valide trouvé et envoyé.", "code": code}), 200
    else:
        send_to_webhook(code, is_valid=False)
        return jsonify({"message": "Code invalide généré et envoyé.", "code": code}), 200

# Lancer l'application Flask
if __name__ == "__main__":
    app.run(debug=True)
