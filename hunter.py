import requests

API_KEY = '0b28615fdfd964d1fc7e63503d382ae150caecea'


def email_verifier(email):
    response = requests.get(f'https://api.hunter.io/v2/email-verifier?email={email}&api_key={API_KEY}')
    if response.status_code == 200 and response.json()['data']['status'] == 'valid':
        return True
    return False
