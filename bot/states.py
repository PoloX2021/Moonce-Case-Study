from bot.myclasses import Mybot, Pool, Token
import os, json
from web3 import Web3


weth = Token('0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'WETH', 18)

tokens = {
    'DAI' : Token('0x6B175474E89094C44Da98b954EedeAC495271d0F', 'DAI', 18),
    'USDC' : Token('0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48', 'USDC', 6),
    'USDT' : Token('0xdAC17F958D2ee523a2206206994597C13D831ec7', 'USDT', 6),
    'WBTC' : Token('0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599', 'WBTC', 8),
}

def init_bot(w3):
    #Create a bot with the current state
    bot = Mybot(w3.eth.block_number)
    
    abi_path = os.path.join(os.path.dirname(__file__), "contracts", "factory_abi.json")
    with open(abi_path, "r") as f:
        factory_abi = json.load(f)

    uni_factory = w3.eth.contract(address = '0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f', abi = factory_abi)
    sushi_factory = w3.eth.contract(address = '0xC0AEe478e3658e2610c5F7A4A2E1777cE9e4f2Ac', abi = factory_abi)
    #Create pools:
    for token in tokens.values():
        symbol = "WETH-"+token.symbol

        address = uni_factory.functions.getPair(weth.address, token.address).call()
        bot.uni_pools.append(Pool(address, symbol, 'Uniswap', weth.copy(), token.copy()))

        address = sushi_factory.functions.getPair(weth.address, token.address).call()
        bot.sushi_pools.append(Pool(address, symbol, 'Sushiswap', weth.copy(), token.copy()))

    return bot

def update_reserves(bot, w3):
    abi_path = os.path.join(os.path.dirname(__file__), "contracts", "erc20_abi.json")
    with open(abi_path, "r") as f:
        erc20_abi = json.load(f)

    for pool in bot.uni_pools + bot.sushi_pools:
        token0_contract = w3.eth.contract(address=Web3.to_checksum_address(pool.token0.address), abi=erc20_abi)
        pool.token0.reserves = token0_contract.functions.balanceOf(Web3.to_checksum_address(pool.address)).call()
        token1_contract = w3.eth.contract(address=Web3.to_checksum_address(pool.token1.address), abi=erc20_abi)
        pool.token1.reserves = token1_contract.functions.balanceOf(Web3.to_checksum_address(pool.address)).call()
    return bot