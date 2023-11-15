import  os
from binance.cm_futures import CMFutures
import datetime
import time


api_key = "ZTVTuaxByK6uW35gw1XhPaRd7M7tPhfc7QvJeWq5JxY9O71jWHur40rmsZn5hB0f"
api_secret = "C3aBnjqFr41tIO4AXi32gTSXPra4cB4xRJ9ijI9M9IS9F2jAsIMUPuNavxNCO3Hf"

cm_futures_client = CMFutures()

cm_futures_client = CMFutures(key=api_key, secret=api_secret)

# print(cm_futures_client.account())

for item in dir(cm_futures_client):
    print(item)
