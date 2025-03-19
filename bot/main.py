from bot.states import init_bot, update_reserves
from bot.connection import http_connection
import time
from bot.arbitrage import log_arbitrages
from bot.myclasses import Token

def main():
    w3 = http_connection()
    bot = init_bot(w3)
    bot = update_reserves(bot, w3)
    while True:
        time.sleep(2)
        block = w3.eth.block_number
        if block > bot.block:
            bot.block = block
            print(f"Scanning at block: {bot.block}")
            bot = update_reserves(bot, w3)
            weth = Token('0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'WETH', 18)
            log_arbitrages(bot)
            for i in range(len(bot.uni_pools)):
                uni_pool = bot.uni_pools[i]
                print(str(uni_pool))
                sushi_pool = bot.sushi_pools[i]
                print(str(sushi_pool))
                print(uni_pool.swapIn(weth, 10**weth.decimals), sushi_pool.swapIn(sushi_pool.token1, uni_pool.swapIn(weth, 10**weth.decimals)))
                print(sushi_pool.swapIn(weth, 10**weth.decimals), uni_pool.swapIn(uni_pool.token1, sushi_pool.swapIn(weth, 10**weth.decimals)))
            print("~"*10)
        

if __name__ == "__main__":
    main()