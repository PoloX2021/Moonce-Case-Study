import unittest
from unittest.mock import patch, MagicMock
from bot.states import init_bot, update_reserves
from bot.connection import http_connection
from bot.arbitrage import arbitrage, log_arbitrages
from bot.myclasses import Token, Pool, Mybot

class TestBot(unittest.TestCase):


    def test_arbitrage(self):
        # Create mock pools
        uni_pool = Pool('0xUniPool', 'WETH-DAI', 'Uniswap', Token('0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'WETH', 18, 1000*10**18), Token('0xDai', 'DAI', 18, 2000))
        sushi_pool = Pool('0xSushiPool', 'WETH-DAI', 'Sushiswap', Token('0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'WETH', 18, 1000*10**18), Token('0xDai', 'DAI', 18, 2000))

        # Test arbitrage detection
        result = arbitrage(uni_pool, sushi_pool)
        self.assertIsNone(result)

        # Modify reserves to create arbitrage opportunity
        uni_pool.token0.reserves = 1200 *10**18
        result = arbitrage(uni_pool, sushi_pool)

        self.assertIsNotNone(result)


    @patch('bot.arbitrage.logging')
    def test_log_arbitrages(self, mock_logging):
        # Create mock bot with arbitrage opportunity
        bot = Mybot(12345)
        uni_pool = Pool('0xUniPool', 'WETH-DAI', 'Uniswap', Token('0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'WETH', 18, 1000*10**18), Token('0xDai', 'DAI', 18, 2000*10**6))
        sushi_pool = Pool('0xSushiPool', 'WETH-DAI', 'Sushiswap', Token('0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'WETH', 18, 2000*10**18), Token('0xDai', 'DAI', 18, 1800*10**6))
        bot.uni_pools = [uni_pool]
        bot.sushi_pools = [sushi_pool]

        log_arbitrages(bot)
        mock_logging.info.assert_called()

if __name__ == '__main__':
    unittest.main()
