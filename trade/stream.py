  
import config
import websocket, json

minute_candlesticks = []
min_counter = 1
stopLoss = None

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
    isRed = None
    change = None
    
    print("=====Received CandleStick======")

    if current_minute_bar['open'] <= current_minute_bar['close']:
        isRed = False
    else:
        isRed = True
    
    if isRed == False:
        change = (100*current_minute_bar['open'])/current_minute_bar['close']
    else:
        change = -(100*current_minute_bar['close'])/current_minute_bar['open']

    minute_candlesticks.append({
        "minute": min_counter,
        "open": current_minute_bar['open'],
        "high": current_minute_bar['high'],
        "low": current_minute_bar['low'],
        "close": current_minute_bar['close'],
        "change": change
    })

    print("==CandleSticks==")
    for candlestick in minute_candlesticks:
            print(candlestick)
    
    scan_ms()

    min_counter += 1

def scan_ms():
    bar_1 = False
    bar_2 = False
    bar_3 = False
    gap_1 = False
    gap_2 = False
    global stopLoss

    if len(minute_candlesticks) >= 30:
        if minute_candlesticks[-3]['change'] < 0 & minute_candlesticks[-3]['change'] >= .40:  #bar -3 evaluation
            bar_3 = True
        
        if minute_candlesticks[-2]['change'] < 0:           #gap -2 evaluation
            if minute_candlesticks[-2]['open'] < minute_candlesticks[-3]['close']:
                gap_2 = True
        else:
            if minute_candlesticks[-2]['close'] < minute_candlesticks[-3]['close']:
                gap_2 = True
        
        if abs(minute_candlesticks[-2]['change']) <= .04:           #bar -2 evaluation
            bar_2 = True
        
        if minute_candlesticks[-2]['change'] < 0:             #gap -1 evaluation
            if minute_candlesticks[-2]['open'] < minute_candlesticks[-1]['open']:
                gap_1 = True
        else:
            if minute_candlesticks[-2]['close'] < minute_candlesticks[-1]['open']:
                gap_1 = True
        
        if minute_candlesticks[-1]['change'] > 0 & minute_candlesticks[-1]['change'] >= .40 & minute_candlesticks[-1]['close'] < minute_candlesticks[-3]['open']:   #bar -1 evaluation
            bar_1 = True

        if bar_3 & gap_2 & bar_2 & gap_1 & bar_1:
            print("Morning star found!!!")
            placeOrder(minute_candlesticks[-1]['close'])
            stopLoss = minute_candlesticks[-2]['low']
            print("Order placed at " + minute_candlesticks[-1]['close'] + ", taking profit at " + minute_candlesticks[-1]['close']*1.01 + " and stop loss set at " + stopLoss)


def placeOrder(price):
    #TODO place order using API
    pass


socket = "wss://data.alpaca.markets/stream"

ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message)
ws.run_forever()
