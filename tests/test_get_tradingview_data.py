from cryptocurrency_trading_telebot.functions import get_tradingview_data
import unittest


class TestGetTradingViewData(unittest.TestCase):
    def test_get_pDW_SMA(self):
        # this test is carried out with the ticker BUSDUSDT, 
        #   because the ratio of its "price" to the twenty-week SMA 
        #   in 99.99% of cases is in the range of 0.95-1.05 (95%-105%)
        self.assertIn(round(get_tradingview_data("BUSDUSDT")["pDW_SMA"], 1) * 100, range(95, 105))


if __name__ == "__main__":
    unittest.main()