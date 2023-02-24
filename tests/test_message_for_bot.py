from cryptocurrency_trading_telebot.functions import message_for_bot
import unittest


class TestMessageForBot(unittest.TestCase):
    def test_get_30_decline(self):
        self.assertEqual(
            message_for_bot(dict(symbol="BTCUSDT", pDW_SMA=0.69, rSI_4H=0)), 
            (
                {"symbol": "BTCUSDT", "pDW_SMA": 0.69, "rSI_4H": 0, "-30% decline": True},
                "BTCUSDT price is -30% decline from twenty-week SMA"
            )
        )

    def test_get_40_decline(self):
        btc_data, message = message_for_bot(dict(symbol="BTCUSDT", pDW_SMA=0.59, rSI_4H=0))
        self.assertEqual(
            (btc_data, message),
            (
                {"symbol": "BTCUSDT", "pDW_SMA": 0.59, "rSI_4H": 0, "-30% decline": True},
                "BTCUSDT price is -30% decline from twenty-week SMA"
            )
        )

        btc_data, message = message_for_bot(btc_data)
        self.assertEqual(
            (btc_data, message),
            (
                {"symbol": "BTCUSDT", "pDW_SMA": 0.59, "rSI_4H": 0, "-30% decline": True, 
                                                                    "-40% decline": True},
                "BTCUSDT price is -40% decline from twenty-week SMA"
            )
        )

    def test_get_50_decline(self):
        btc_data, message = message_for_bot(dict(symbol="BTCUSDT", pDW_SMA=0.49, rSI_4H=0))
        self.assertEqual(
            (btc_data, message),
            (
                {"symbol": "BTCUSDT", "pDW_SMA": 0.49, "rSI_4H": 0, "-30% decline": True},
                "BTCUSDT price is -30% decline from twenty-week SMA"
            )
        )

        btc_data, message = message_for_bot(btc_data)
        self.assertEqual(
            (btc_data, message),
            (
                {"symbol": "BTCUSDT", "pDW_SMA": 0.49, "rSI_4H": 0, "-30% decline": True, 
                                                                    "-40% decline": True},
                "BTCUSDT price is -40% decline from twenty-week SMA"
            )
        )

        btc_data, message = message_for_bot(btc_data)
        self.assertEqual(
            (btc_data, message),
            (
                {"symbol": "BTCUSDT", "pDW_SMA": 0.49, "rSI_4H": 0, "-30% decline": True, 
                                                                    "-40% decline": True, 
                                                                    "-50% decline": True},
                "BTCUSDT price is -50% decline from twenty-week SMA"
            )
        )

    def test_get_SMA_corrected(self):
        self.assertEqual(
            message_for_bot({"symbol": "BTCUSDT", "pDW_SMA": 1.01, "rSI_4H": 0, "-30% decline": True}),
            (
                {"symbol": "BTCUSDT", "pDW_SMA": 1.01, "rSI_4H": 0, "-30% decline": False, 
                                                                    "-40% decline": False},
                "BTCUSDT corrected"
            )
        )

    def test_get_SMA_without_corrected(self):
        self.assertEqual(
            message_for_bot({"symbol": "BTCUSDT", "pDW_SMA": 1.01, "rSI_4H": 0, "-30% decline": True,
                                                                                "-40% decline": True,
                                                                                "-50% decline": True}),
            (
                {"symbol": "BTCUSDT", "pDW_SMA": 1.01, "rSI_4H": 0, "-30% decline": True,
                                                                    "-40% decline": True,
                                                                    "-50% decline": True},
                None
            )
        )

    def test_get_RSI_corrected(self):
        self.assertEqual(
            message_for_bot({"symbol": "BTCUSDT", "pDW_SMA": 0.71, "rSI_4H": 71, "-30% decline": True}),
            (
                {"symbol": "BTCUSDT", "pDW_SMA": 0.71, "rSI_4H": 71, "-30% decline": False, 
                                                                    "-40% decline": False},
                "BTCUSDT corrected"
            )
        )

    def test_get_SMA_without_corrected(self):
        self.assertEqual(
            message_for_bot({"symbol": "BTCUSDT", "pDW_SMA": 0.71, "rSI_4H": 71, "-30% decline": True,
                                                                                "-40% decline": True,
                                                                                "-50% decline": True}),
            (
                {"symbol": "BTCUSDT", "pDW_SMA": 0.71, "rSI_4H": 71, "-30% decline": True,
                                                                    "-40% decline": True,
                                                                    "-50% decline": True},
                None
            )
        )

    def test_get_corrected_from_low(self):
        self.assertEqual(
            message_for_bot({"symbol": "BTCUSDT", "pDW_SMA": 1.51, "rSI_4H": 0, "-30% decline": True,
                                                                                "-40% decline": True,
                                                                                "-50% decline": True}),
            (
                {"symbol": "BTCUSDT", "pDW_SMA": 1.51, "rSI_4H": 0, "-30% decline": False, 
                                                                    "-40% decline": False,
                                                                    "-50% decline": False},
                "BTCUSDT corrected from the low point"
            )
        )


if __name__ == "__main__":
    unittest.main()