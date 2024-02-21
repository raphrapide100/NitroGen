import requests
import random
import string

# Génère un code aléatoire de 18 caractères (lettres et chiffres)
def generate_random_code(length=18):
    characters = string.ascii_letters + string.digits  # Lettres majuscules, minuscules et chiffres
    return ''.join(random.choice(characters) for _ in range(length))

# Fonction pour vérifier le code sur l'API Discord
def check_code(code):
    url = f"https://discord.com/api/v9/entitlements/gift-codes/{code}"
    response = requests.get(url)
    return response.status_code == 200

# Remplacez ces URL par les URL de vos webhooks Discord
WEBHOOK_URL_VALID = 'https://discord.com/api/webhooks/1209885252462579772/ffcDterrOviIjAxk3GrQ9G7L9vh-9rVCpNFTuEyMUVpt03aK81nh-tlQW-4WmBlvGTDl'
WEBHOOK_URL_INVALID = 'https://discord.com/api/webhooks/1209885309958103090/GKMOGqCSYxwH4TMC3ipmmnEWwjtbHpy_P4A5-PDidAhljl6zrqtN2A4UjkgttS3JgsCd'

# Fonction pour envoyer le code à votre webhook Discord
def send_to_webhook(code, is_valid=True):
    if is_valid:
        url = WEBHOOK_URL_VALID
        content = f"Code valide trouvé: discord.gift/{code}"
    else:
        url = WEBHOOK_URL_INVALID
        content = f"Code invalide: {code}"
    
    data = {
        "content": content,
        "username": "Vérificateur de code"
    }
    response = requests.post(url, json=data)
    return response.status_code

# Boucle principale
def main():
    while True:
        code = generate_random_code()
        print(f"Vérification du code: {code}")
        if check_code(code):
            print(f"Code valide trouvé: {code}")
            response_code = send_to_webhook(code, is_valid=True)
            if response_code == 204:
                print("Code valide envoyé au webhook avec succès.")
            else:
                print("Erreur lors de l'envoi au webhook valide.")
            break  # Optionnel : Sortir de la boucle après avoir trouvé un code valide
        else:
            print(f"Code invalide: {code}")
            response_code = send_to_webhook(code, is_valid=False)
            if response_code == 204:
                print("Code invalide envoyé au webhook avec succès.")
            else:
                print("Erreur lors de l'envoi au webhook invalide.")

if __name__ == "__main__":
    main()
