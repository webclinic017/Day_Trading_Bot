  
import config
import websocket, json

minute_candlesticks = []
min_counter = 1

def on_open(ws):
    print("opened")
    auth_data = {
        "action": "authenticate",
        "data": {"key_id": config.API_KEY, "secret_key": config.SECRET_KEY}
    }

    ws.send(json.dumps(auth_data))

    listen_message = {"action": "listen", "data": {"streams": ["AM.TSLA"]}}

    ws.send(json.dumps(listen_message))


def on_message(ws, message,min_counter):
    global current_minute_bar, min_counter
    current_minute_bar = json.loads(message)
    print("=====Received CandleStick======")
    minute_candlesticks.append({
        "minute": min_counter,
        "open": current_minute_bar.open,
        "high": current_minute_bar.high,
        "low": current_minute_bar.low,
        "close": current_minute_bar.close
    })

    print("==CandleSticks==")
    for candlestick in minute_candlesticks:
            print(candlestick)
    
    scan_ms()
  


    min_counter += 1

def scan_ms():
      ##detect morningstar from last 3 bars by checking to see if third star is red && the change is 
    if len(minute_candlesticks) >= 30:
        if (minute_candlesticks[-3].open * 100)/minute_candlesticks[-3].close


socket = "wss://data.alpaca.markets/stream"

ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message)
ws.run_forever()
