import copy

class Token:
    def __init__(self, _address, _symbol, _decimals, _reserve=0):
        self.address = _address
        self.symbol = _symbol
        self.reserves = _reserve
        self.decimals = _decimals

    # To show the right value
    def formatted_reserves(self) -> float:
        return self.reserves / (10 ** self.decimals)
    
    #String to visualize
    def __repr__(self):
        return f"Token(symbol={self.symbol}, address={self.address}, reserves={self.formatted_reserves()})"

    #Create a copy of the code
    def copy(self):
        return copy.deepcopy(self)

class Pool:
    #Fees for Uniswap and Sushiswap are 0.3%
    def __init__(self, _address, _symbol, _type, _token0, _token1, _fee = 0.003):
        self.address = _address
        self.symbol = _symbol
        self.type = _type
        self.token0 = _token0
        self.token1 = _token1
        self.fee = _fee
    
    #Visualize the pool state
    def __repr__(self):
        return f"Pool(name: {self.symbol}, address: {self.address}, type: {self.type})\n{str(self.token0)}\n{str(self.token1)}"

    def get_reserves(self):
        return {
            self.token0.symbol: self.token0.formatted_reserves(),
            self.token1.symbol: self.token1.formatted_reserves(),
        }
    
    #Simulate the swap of a token in the pool
    def swapIn(self, token, amount):
        K = self.token0.reserves * self.token1.reserves
        amount_after_fees = (1-self.fee) * amount
        if token.address == self.token0.address:
            return self.token1.reserves - K / (self.token0.reserves + amount_after_fees)
        else:
            return self.token0.reserves - K / (self.token1.reserves + amount_after_fees)
    
    def price(self, token):
        return self.token1.reserves / self.token0.reserves if token.address == self.token0.address else self.token0.reserves / self.token1.reserves
    
class Mybot:
    def __init__(self, _block, _uni_pools = [], _sushi_pools = []):
        self.block = _block
        self.uni_pools = _uni_pools
        self.sushi_pools = _sushi_pools