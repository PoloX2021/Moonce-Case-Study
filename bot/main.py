from bot.states import init_bot, update_reserves
from bot.connection import http_connection
import time
from bot.arbitrage import log_arbitrages
from bot.myclasses import Token

def main():
    #Initialize the pools
    w3 = http_connection()
    bot = init_bot(w3)
    bot = update_reserves(bot, w3)

    while True:
        time.sleep(2)
        block = w3.eth.block_number
        #When there is a new block
        if block > bot.block:
            bot.block = block
            bot = update_reserves(bot, w3)
            weth = Token('0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'WETH', 18)

            #Check for arbitrage opportunities
            log_arbitrages(bot)
        

if __name__ == "__main__":
    main()