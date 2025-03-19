from bot.myclasses import Token, Pool, Mybot
import logging


logging.basicConfig(level=logging.INFO)

#Calculate the arbitrage opportunities between two pools
def arbitrage(uni_pool, sushi_pool):
    weth = Token('0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'WETH', 18)

    amount_in = 1 * 10**weth.decimals

    #Start by trading ETH to Uniswap
    amount_out = sushi_pool.swapIn(sushi_pool.token1, uni_pool.swapIn(weth, amount_in))
    if amount_out > amount_in:
        return [uni_pool, sushi_pool, amount_in, uni_pool.swapIn(weth, amount_in), amount_out]
    
    #Then try trading first ETH to Sushiswap
    amount_out = uni_pool.swapIn(uni_pool.token1, sushi_pool.swapIn(weth, amount_in))
    if amount_out > amount_in:
        return [sushi_pool, uni_pool, amount_in, uni_pool.swapIn(weth, amount_in), amount_out]

    #No arbitrage opportunity
    return None
    
def log_arbitrages(bot):
    for i in range(len(bot.uni_pools)):
        arb = arbitrage(bot.uni_pools[i], bot.sushi_pools[i])

        ## Format the log
        if not(arb is None):
            arb[2] = arb[2] * 10**-arb[0].token0.decimals
            arb[3] = arb[3] * 10**-arb[0].token1.decimals
            arb[4] = arb[4] * 10**-arb[0].token0.decimals
            logging.info(f"""Arbitrage found at block {bot.block}. 
                Through {arb[0].type}, address: {arb[0].address} then {arb[1].type}, address: {arb[1].address}
                {arb[2]} {arb[0].token0.symbol} -> {arb[3]} {arb[0].token1.symbol} -> {arb[4]} {arb[0].token0.symbol}""")