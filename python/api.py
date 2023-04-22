import requests
from io import BytesIO
from urllib3 import encode_multipart_formdata


REQUEST_FORM_DATA_BOUNDARY = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
FORM_DATA_STARTING_PAYLOAD = '{0}\r\nContent-Disposition: form-data; name="'.format(
    REQUEST_FORM_DATA_BOUNDARY)
FORM_DATA_MIDDLE_PAYLOAD = '\"\r\n\r\n'
FORM_DATA_ENDING_PAYLOAD = '{0}'.format(REQUEST_FORM_DATA_BOUNDARY)
headers = {
    'User-Agent': None,
    'Authorization': "Bearer 643d843b2c067643d843b2c069",
    'Content-Type': "multipart/form-data; boundary={}".format(REQUEST_FORM_DATA_BOUNDARY),
    'Accept-Encoding': 'gzip, deflate, br'
}
api_url = 'http://api.datsart.dats.team'


def generate_form_data_payload(kwargs):
    payload = ''
    for key, value in kwargs.items():
        payload += '\r\n{0}{1}{2}{3}\r\n'.format(
            FORM_DATA_STARTING_PAYLOAD, key, FORM_DATA_MIDDLE_PAYLOAD, value)
    payload += FORM_DATA_ENDING_PAYLOAD
    return payload


def get_info():
    return requests.post(api_url + '/art/stage/info', headers=headers).json()


def get_image_bytes(url: str):
    return BytesIO(requests.get(url).content)


def get_colors_info():
    return requests.post(api_url + '/art/colors/info', headers=headers).json()


def get_colors_amount(color: str):
    return requests.post(api_url + '/art/colors/amount', headers=headers, data={'color': color}).json()


def get_colors_list():
    return requests.post(api_url + '/art/colors/list', headers=headers).json()


def generate_colors():
    return requests.post(api_url + '/art/factory/generate', headers=headers).json()


def pick_color(num, tick):
    body, header = encode_multipart_formdata(
        {'num': num, 'tick': tick})
    headers['Content-Type'] = header

    r = requests.post(api_url + '/art/factory/pick', headers=headers,
                      data=body)

    return r.json()


def shoot(data):
    body, header = encode_multipart_formdata(data)
    headers['Content-Type'] = header
    # header['Authorization'] = headers['Authorization']
#     headers['Content-Type'] = 'multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW'

#     str = f'''----WebKitFormBoundary7MA4YWxkTrZu0gW
# Content-Disposition: form-data; name="angleHorizontal"

# {data['angleHorizontal']}
# ----WebKitFormBoundary7MA4YWxkTrZu0gW
# Content-Disposition: form-data; name="angleVertical"

# {data['angleVertical']}
# ----WebKitFormBoundary7MA4YWxkTrZu0gW
# Content-Disposition: form-data; name="power"

# {data['power']}
# ----WebKitFormBoundary7MA4YWxkTrZu0gW
# Content-Disposition: form-data; name="colors[{data['color']}]"

# 1
# ----WebKitFormBoundary7MA4YWxkTrZu0gW'''
#     print(str)

    r = requests.post(api_url + '/art/ballista/shoot',
                      headers=headers, data=body)

    return r.json()
