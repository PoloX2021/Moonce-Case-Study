from bot.myclasses import Token, Pool, Mybot
import logging


def hop(pool0, pool1, token, amount):
    if pool0.token0.address != token.address and pool0.token1.address != token.address:
        raise Exception("Token is not in the pool0")
    if pool1.token0.address != token.address and pool1.token1.address != token.address:
        raise Exception("Token is not in the pool1")
    if pool0.token0.address != pool1.token0.address:
        raise Exception("Not the same first token")
    if pool0.token1.address != pool1.token1.address:
        raise Exception("Not the same second token")
    
    amount_hop = pool0.swapIn(token, amount)

    if pool0.token0.address == token.address:
        other_token = pool0.token1
    else:
        other_token = pool0.token0

    amount_out = pool1.swapIn(other_token, amount_hop)
    return amount_out

def arbitrage(uni_pool, sushi_pool):
    weth = Token('0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'WETH', 18)

    amount_in = 1 * 10**weth.decimals
    amount_out = hop(uni_pool, sushi_pool, weth, amount_in)
    if amount_out > amount_in:
        return [uni_pool, sushi_pool, amount_in, uni_pool.swapIn(weth, amount_in), amount_out]
    
    amount_in = 1 * 10**weth.decimals
    amount_out = hop(sushi_pool, uni_pool, weth, amount_in)
    if amount_out > amount_in:
        return [sushi_pool, uni_pool, amount_in, uni_pool.swapIn(weth, amount_in), amount_out]

    return None
    
def log_arbitrages(bot):
    for i in range(len(bot.uni_pools)):
        arb = arbitrage(bot.uni_pools[i], bot.sushi_pools[i])
        if arb:
            arb[2] = arb[2] * 10**-arb[0].token0.decimals
            arb[3] = arb[3] * 10**-arb[0].token1.decimals
            arb[4] = arb[4] * 10**-arb[0].token0.decimals
            #Don't show small arbitrages which are meaningless
            if arb[2] > 10**-8 and arb[4] > 10**-8:
                logging.info(f"""Arbitrage found at block {bot.block}. 
                            Through {arb[0].type}, address: {arb[0].address} then {arb[1].type}, address: {arb[1].address}
                            {arb[2]} {arb[0].token0.symbol} -> {arb[3]} {arb[0].token1.symbol} -> {arb[4]} {arb[0].token0.symbol}""")