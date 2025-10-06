import logging
from aster.rest_api import Client
from aster.lib.utils import config_logging
from aster.error import ClientError
import os
from dotenv import load_dotenv
import time
from datetime import datetime
load_dotenv()

config_logging(logging, logging.INFO)

key = os.getenv("ASTER_S0_KEY")
secret = os.getenv("ASTER_S0_SECRET")

client = Client(key, secret, base_url="https://fapi.asterdex.com")


def test_order_latency():
    now_timestamp = datetime.now().timestamp() * 1000
    create_order_response = client.new_order(symbol="BTCUSDT", side = "BUY", type= "LIMIT", quantity= 0.01, timeInForce="GTC", price= 115000)
    # logging.info(create_order_response)
    clientOrderId = create_order_response["clientOrderId"]

    create_order_latency = create_order_response["updateTime"] - now_timestamp

    now_timestamp = datetime.now().timestamp() * 1000
    cancel_order_response = client.cancel_order(symbol="BTCUSDT", orderId=int(create_order_response["orderId"]))
    # logging.info(cancel_order_response)

    cancel_order_latency = cancel_order_response["updateTime"] - now_timestamp

    logging.info(f"Create order latency: {create_order_latency}ms")
    logging.info(f"Cancel order latency: {cancel_order_latency}ms")


for i in range(10):
    test_order_latency()