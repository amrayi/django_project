import requests

def send_sms(api_key, secret_key, phone_number, message):
    url = 'https://api.farapayamak.ir/v1/Message/SendSms'
    payload = {
        'username': api_key,
        'password': secret_key,
        'to': phone_number,
        'from': '09190027944',  # شماره ارسال کننده
        'text': message
    }
    response = requests.post(url, data=payload)
    return response.json()
