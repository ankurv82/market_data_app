from json2html import *
from flask import Flask, request, render_template
import json
import logging.config
from clients import market_data_client

logger = logging.getLogger("app_endpoint")

DEFAULT_ORDER_DEPTH = '5'


def run_app(my_host, my_port, my_client_config):
    app = Flask(__name__, template_folder='../templates')
    my_client = market_data_client.BinanceMarketDataClient(my_client_config)

    @app.route('/api/v1/currencies/quotes', methods=['GET'])
    def api_get():
        logger.debug("api_get called")
        if 'symbol' in request.args and request.args['symbol']:
            symbol = request.args['symbol']
        else:
            error = {
                'Exception': "Error: Symbol Not Provided",
            }
            logger.error(str(error))
            return json.dumps(error)

        if 'limit' in request.args and request.args['limit']:
            limit = request.args['limit']
        else:
            limit = DEFAULT_ORDER_DEPTH

        data_processed = my_client.get_data(symbol, limit)
        return json2html.convert(json=data_processed)

    @app.errorhandler(404)
    def page_not_found(e):
        return "<h1>404</h1><p>The resource could not be found.</p>", 404

    @app.route("/")
    def index():
        return render_template("index.html")

    app.run(host=my_host, port=my_port)
