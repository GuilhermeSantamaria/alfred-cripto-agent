def identify_cryptos_in_prompt(prompt_text):
    mapping = {
        'bitcoin': 'bitcoin', 'btc': 'bitcoin',
        'ethereum': 'ethereum', 'eth': 'ethereum',
        'ripple': 'ripple', 'xrp': 'ripple',
        'cardano': 'cardano', 'ada': 'cardano',
        'solana': 'solana', 'sol': 'solana',
        'dogecoin': 'dogecoin', 'doge': 'dogecoin',
        'binance coin': 'binancecoin', 'bnb': 'binancecoin',
        'litecoin': 'litecoin', 'ltc': 'litecoin',
        'chainlink': 'chainlink', 'link': 'chainlink',
        'polygon': 'polygon', 'matic': 'polygon'
    }
    prompt_text = prompt_text.lower()
    found = set()
    for key in mapping:
        if key in prompt_text:
            found.add(mapping[key])
    return list(found)