"""FXT auto maker/taker."""
import ccxt
import configparser
import sys
import time


def make_exchange(config):
    """Make ccxt object."""
    exchange = ccxt.ftx()
    exchange.apiKey = config['apiKey']
    exchange.secret = config['secret']
    return exchange


def create_order(exchange, symbol, typus, side, amount, count=0):
    """Create Order."""
    if count >= 3:
        print (f'exit {typus} {side}')
        sys.exit(1)
    try:
        if typus == 'limit':
            book = exchange.fetch_order_book(symbol)
            price = (book['asks'][0][0] + book['bids'][0][0]) / 2.0
            exchange.create_order(
                symbol=symbol,
                type=typus,
                side=side,
                amount=amount,
                price=price
            )
        else:
            exchange.create_order(
                symbol=symbol,
                type=typus,
                side=side,
                amount=amount
            )
    except Exception as e:
        print (e)
        create_order(exchange, symbol, typus, side, amount, count + 1)


def main():
    """Main Fuction."""
    config = configparser.ConfigParser()
    config.read('config.ini')

    maker = make_exchange(config['maker'])
    taker = make_exchange(config['taker'])
    symbol = config['trade']['symbol']
    amount = float(config['trade']['amount'])
    repeat = int(config['trade']['repeat'])

    for i in range(repeat):
        # make position
        create_order(maker, symbol, 'limit', 'buy', amount)
        time.sleep(0.1)
        create_order(taker, symbol, 'market', 'sell', amount)
        time.sleep(1)
        # settle position
        create_order(maker, symbol, 'limit', 'sell', amount)
        time.sleep(0.1)
        create_order(taker, symbol, 'market', 'buy', amount)
        time.sleep(1)


if __name__ == '__main__':
    main()
