from coinmarketcapapi import CoinMarketCapAPI, CoinMarketCapAPIError
import dotenv, os

dotenv.load_dotenv()
API_KEY = os.getenv("CMC_API_KEY")
cmc = CoinMarketCapAPI(API_KEY)

# Returns USD quote of asset specified by symbol
def get_price(base, quote="USD", amount=1):
    quote = quote.upper()
    price_info = cmc.tools_priceconversion(convert=quote, amount=amount, symbol=base)
    return price_info._Response__payload["data"]["quote"][quote]["price"]
