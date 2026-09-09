from kavenegar import *




def send_otp_code(phone_number,code):
    try:
        api = KavenegarAPI('373139********************************593D')
        params = {'sender': '2000660110', 'receptor': phone_number, 'message': f"your code:{code}"}
        response = api.sms_send(params)
    except Exception as e:
        print(e)

