import axios from 'axios';
import FormData from 'form-data';

const data = {
    'angleHorizontal': '0.016745',
    'angleVertical': 45,
    'colors[15943455]': 1,
    'power': '2.461236'
};

const fd = new FormData();

Object.entries(data).forEach(([key, val]) => fd.append(key, val));

axios.post('http://api.datsart.dats.team/art/factory/pick', fd, {
    headers: {
        'Authorization': "Bearer 643d843b2c067643d843b2c069",
        'Content-Type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW"
    }
}).then(res => console.debug(res.data)).catch(err => console.error(err));