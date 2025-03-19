from bot.myclasses import Token, Pool, Mybot
from scipy.optimize import minimize
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

#The ouput of sending amount of token to pool0 then the result to pool1
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

def arbitrage_pair_directional(pool0, pool1):
    # Check if you can send weth to pool0 and get more weth from pool1
    #Always start with weth
    weth = Token('0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'WETH', 18)

    #We will minimize the opposite of the profit
    def neg_profit(amount):
        print(amount[0], hop(pool0, pool1, weth, amount[0]), amount[0] - hop(pool0, pool1, weth, amount[0]))
        return amount[0] - hop(pool0, pool1, weth, amount[0])
    
    constraint = {'type': 'ineq', 'fun': lambda x:x[0]}
    amount_max = minimize(neg_profit, x0 = [5*10**6], constraints = constraint).x[0]
    print(amount_max, neg_profit([amount_max]))
    if neg_profit([amount_max]) >= 0:
        return 0
    else:
        print("~"*10)
        return amount_max

def arbitrage(uni_pool, sushi_pool):
    #Try one direction
    amount = arbitrage_pair_directional(uni_pool, sushi_pool)
    weth = Token('0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'WETH', 18)
    amount_out = hop(uni_pool, sushi_pool, weth, amount)
    if amount - amount_out < 0:
        print([uni_pool, sushi_pool, amount, uni_pool.swapIn(weth, amount), amount_out])
        return [uni_pool, sushi_pool, amount, uni_pool.swapIn(weth, amount), amount_out]
    
    #Try the other direction
    amount = arbitrage_pair_directional(sushi_pool, uni_pool)
    amount_out = hop(uni_pool, sushi_pool, weth, amount)
    if amount - amount_out < 0:
        print([sushi_pool, uni_pool, amount, sushi_pool.swapIn(weth, amount), amount_out])
        return [sushi_pool, uni_pool, amount, sushi_pool.swapIn(weth, amount), amount_out]
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