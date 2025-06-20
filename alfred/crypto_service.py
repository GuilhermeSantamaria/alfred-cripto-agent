from pycoingecko import CoinGeckoAPI

try:
    cg = CoinGeckoAPI()
except Exception as e:
    print(f"Erro ao conectar com CoinGecko: {e}")
    cg = None

def get_crypto_data(coin_ids=None, vs_currency='usd'):
    if not cg:
        return {}
    try:
        if coin_ids:
            data = cg.get_coins_markets(vs_currency=vs_currency, ids=','.join(coin_ids))
        else:
            data = cg.get_coins_markets(vs_currency=vs_currency, order='market_cap_desc', per_page=100, page=1)

        result = {}
        for item in data:
            result[item['id']] = {
                'name': item['name'],
                'symbol': item['symbol'].upper(),
                'price': item['current_price'],
                'change': item['price_change_percentage_24h'],
                'market_cap': item['market_cap'],
                'volume': item['total_volume']
            }
        return result
    except Exception as e:
        print(f"Erro ao buscar dados: {e}")
        return {}

