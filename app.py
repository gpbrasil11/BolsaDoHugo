import yfinance as yf
import telegram
from flask import Flask, render_template

app = Flask(
    __name__, template_folder='E:/OneDrive/Desktop/visual bot bolsa/templates')

token = '6207875880:AAFsioEMXMnus2r5Id6yxs6cE4YKCzSdw4Q'
chat_id = '-804551456'


def send_message(token, chat_id, text):
    bot = telegram.Bot(token=token)
    bot.send_message(chat_id=chat_id, text=text)


def candlestick(df):
    # Renomeia as colunas
    df = df.rename(columns={'Open': 'open', 'High': 'high', 'Low': 'low',
                            'Close': 'close', 'Adj Close': 'adj_close', 'Volume': 'volume'})

    # Calcula os candlesticks

    df['body'] = df['close'] - df['open']
    df['upper_wick'] = df['high'] - df[['open', 'close']].max(axis=1)
    df['lower_wick'] = df[['open', 'close']].min(axis=1) - df['low']

    df['open_15'] = df['open'].shift(-15)
    df['close_15'] = df['close'].shift(-15)
    df['high_15'] = df['high'].shift(-15)
    df['low_15'] = df['low'].shift(-15)

    df['body_15'] = df['close_15'] - df['open']
    df['upper_wick_15'] = df['high_15'] - df[['open', 'close_15']].max(axis=1)
    df['lower_wick_15'] = df[['open', 'close_15']].min(axis=1) - df['low_15']

    df['candle_type'] = ''
    df = df.tz_localize(None)

    df.loc[(df['body'] > 0) & (df['upper_wick'] == 0) & (
        df['lower_wick'] == 0), 'candle_type'] = 'Marubozu de alta +'
    df.loc[(df['body'] < 0) & (df['upper_wick'] == 0) & (
        df['lower_wick'] == 0), 'candle_type'] = 'Marubozu de baixa -'

    df.loc[(df['body'] > 0) & (df['upper_wick'] == 0) & (
        df['lower_wick'] > 0), 'candle_type'] = 'Padrão de martelo +'
    df.loc[(df['body'] < 0) & (df['upper_wick'] > 0) & (
        df['lower_wick'] == 0), 'candle_type'] = 'Padrão de shooting star -'

    df.loc[(df['body'] > 0) & (df['upper_wick'] > 0) & (
        df['lower_wick'] == 0), 'candle_type'] = 'Padrão de martelo invertido +'
    df.loc[(df['body'] < 0) & (df['upper_wick'] == 0) & (
        df['lower_wick'] > 0), 'candle_type'] = 'Padrão de homem pendurado -'

    df.loc[(df['body'] == 0) & (df['upper_wick'] == 0) & (
        df['lower_wick'] > 0), 'candle_type'] = 'Padrão de Dragonfly Doji 0'
    df.loc[(df['body'] == 0) & (df['upper_wick'] > 0) & (
        df['lower_wick'] == 0), 'candle_type'] = 'Padrão de Gravestone Doji 0'

    df.loc[(df['body'] > 0) & (df['upper_wick'] > 0) & (
        df['lower_wick'] > 0), 'candle_type'] = 'Padrão de alta +'
    df.loc[(df['body'] < 0) & (df['upper_wick'] > 0) & (
        df['lower_wick'] > 0), 'candle_type'] = 'Padrão de baixa -'

    df.loc[(df['body'] == 0) & (df['upper_wick'] > 0) & (
        df['lower_wick'] > 0), 'candle_type'] = 'Spinning Top 0'
    df.loc[(df['body'] == 0) & (df['upper_wick'] == 0) & (
        df['lower_wick'] == 0), 'candle_type'] = 'Spinning Top Zerado 0'

    df.loc[(df['body_15'] > 0) & (df['upper_wick_15'] == 0) & (
        df['lower_wick_15'] == 0), 'candle_type_15'] = 'Marubozu de alta +'
    df.loc[(df['body_15'] < 0) & (df['upper_wick_15'] == 0) & (
        df['lower_wick_15'] == 0), 'candle_type_15'] = 'Marubozu de baixa -'

    df.loc[(df['body_15'] > 0) & (df['upper_wick_15'] == 0) & (
        df['lower_wick_15'] > 0), 'candle_type_15'] = 'Padrão de martelo +'
    df.loc[(df['body_15'] < 0) & (df['upper_wick_15'] > 0) & (
        df['lower_wick_15'] == 0), 'candle_type_15'] = 'Padrão de shooting star -'

    df.loc[(df['body_15'] > 0) & (df['upper_wick_15'] > 0) & (
        df['lower_wick_15'] == 0), 'candle_type_15'] = 'Padrão de martelo invertido +'
    df.loc[(df['body_15'] < 0) & (df['upper_wick_15'] == 0) & (
        df['lower_wick_15'] > 0), 'candle_type_15'] = 'Padrão de homem pendurado -'

    df.loc[(df['body_15'] == 0) & (df['upper_wick_15'] == 0) & (
        df['lower_wick_15'] > 0), 'candle_type_15'] = 'Padrão de Dragonfly Doji 0'
    df.loc[(df['body_15'] == 0) & (df['upper_wick_15'] > 0) & (
        df['lower_wick_15'] == 0), 'candle_type_15'] = 'Padrão de Gravestone Doji 0'

    df.loc[(df['body_15'] > 0) & (df['upper_wick_15'] > 0) & (
        df['lower_wick_15'] > 0), 'candle_type_15'] = 'Padrão de alta +'
    df.loc[(df['body_15'] < 0) & (df['upper_wick_15'] > 0) & (
        df['lower_wick_15'] > 0), 'candle_type_15'] = 'Padrão de baixa -'

    df.loc[(df['body_15'] == 0) & (df['upper_wick_15'] > 0) & (
        df['lower_wick_15'] > 0), 'candle_type_15'] = 'Spinning Top 0'
    df.loc[(df['body_15'] == 0) & (df['upper_wick_15'] == 0) & (
        df['lower_wick_15'] == 0), 'candle_type_15'] = 'Spinning Top Zerado 0'

    return df


@app.route('/')
def index():
    # Coleta os dados de ações em tempo real
    data = yf.download("VALE3.SA", period="1d", interval="15m")
    # Seleciona apenas as colunas relevantes
    data = data[['Open', 'High', 'Low', 'Close', 'Volume']]
    data = candlestick(data)
    # Formata os dados para 4 casas decimais
    data = data.round(4)
    data = data[-5:]
    # Renderiza o template HTML com os dados
    # verifica se todas as linhas são iguais a "Marubozu de alta +"
    if all(data['candle_type'] == 'Marubozu de alta +'):
        print('Alerta! Todas as linhas são iguais a "Marubozu de alta +"')
        send_message(
            token, chat_id, 'Alerta! Todas as linhas são iguais a "Marubozu de alta +"')
    return render_template('index.html', data=data)


if __name__ == '__main__':
    app.run()
