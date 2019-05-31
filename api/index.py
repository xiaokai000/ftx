from flask import Flask, request, jsonify
from ..ftx.conn import Mongodb


col = Mongodb().db['old_ftx']

app = Flask(__name__)


@app.route('/', methods=['post'])
def index():
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    province = request.form.get('province')
    city = request.form.get('city')

    if start_date > end_date:
        return 'error'

    data = col.find_one({'date':{'$gte': start_date,'$lte': end_date}, 'province': province, 'city': city})

    if not data:
        return 'None'

    return jsonify({'data': data['new_house_price_list']})