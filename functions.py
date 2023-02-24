from tradingview_ta import TA_Handler, Interval
from time import sleep
import traceback

def get_tradingview_data(symbol, date_and_time=""):
    """
    The function accepts an asset ticker. 
    Through the tradingview_ta library, requests from TradingView the current price of the cryptocurrency, 
    its twenty-week SMA and four-hour RSI. 
    And returns a dictionary containing the ticker of the asset, 
    the ratio between the price and the twenty-week SMA, four-hour RSI.
    """

    try:
        one_week_handler = TA_Handler(
            symbol=symbol,
            screener="Crypto",
            exchange="Binance",
            interval=Interval.INTERVAL_1_WEEK
        )

        close_price = one_week_handler.get_analysis().indicators["close"]
        twenty_week_SMA = one_week_handler.get_analysis().indicators["SMA20"]

        # getting the ratio of the price to the twenty-week SMA
        price_difference_with_SMA = close_price / twenty_week_SMA

        sleep(5)

        four_hours_handler = TA_Handler(
            symbol=symbol,
            screener="Crypto",
            exchange="Binance",
            interval=Interval.INTERVAL_4_HOURS
        )

        four_hours_RSI = four_hours_handler.get_analysis().indicators["RSI"]

        symbol_data = {
            "symbol": symbol,
            "pDW_SMA": price_difference_with_SMA,
            "rSI_4H": four_hours_RSI
        }

    # the except block is designed to catch an error about unsuccessful access to the TradingView API, 
    #   through the tradingview_ta library
    except Exception:
        error = traceback.format_exc()
        with open("log.txt", "a") as log_file:
            # all errors are written to a log file
            print(f"{date_and_time}\n{error}\n", file=log_file)

        # in the case when access to the TradingView API fails, 
        #   the dictionary with the data of the ticker is assigned values 
        #   which can be used in further logical expressions in the message_for_bot function,
        #   but they will not affect the current state of the asset in any way
        symbol_data = {
            "symbol": symbol,
            "pDW_SMA": 1,
            "rSI_4H": 0
        }
    finally:
        sleep(5)
        return symbol_data


def message_for_bot(symbol_data):
    """
    The function takes a dictionary containing the ticker data obtained from get_tradingview_data 
    and returns a two-tuple. 
    The first element of the tuple is the received data 
    and additional keys, such as "-30% decline", fixing the current state of the market. 
    The second element is a message for the telegram bot or None if there is no such message.
    This function compares the current values of the indicators with their predefined levels to generate signals 
    about potential entry and exit points for transactions.
    """

    # the value representing the equality of the ticker price and its 20-week SMA 
    #   is the standard closing point for long positions opened from the lower boundary of the classic envelope
    EQUALITY_WITH_SMA = 1          # in the script it is used for close trades opened from levels -30% and -40% from SMA

    # the value representing the upper boundary of the envelope is the standard closing point for long positions 
    #   oriented to a strong upward movement from the lower boundary of the classic envelope
    N_TIMES_EXCESS = 1.5                     # in the script it is used for close trades opened from level -50% from SMA
    
    # standard border for the RSI indicator separating the impulse equilibrium zone from the overbought zone
    STANDARD_TOP_LINE_RSI = 70     # in the script it is used for close trades opened from levels -30% and -40% from SMA
    
    # checking whether the ticker has corrected relative to its previous fall, 
    #   if the ticker price previously descended to the 30% (40%) decline zone from the twenty-week SMA level, 
    #   and now returned to the current SMA level, or the four-hour RSI moved into the overbought zone, 
    #   then the asset is considered corrected
    if symbol_data.get("-30% decline") and not symbol_data.get("-50% decline") and (
            symbol_data["pDW_SMA"] > EQUALITY_WITH_SMA or symbol_data["rSI_4H"] > STANDARD_TOP_LINE_RSI
        ):

        # after a ticker correction, its keys are reset
        symbol_data["-30% decline"] = False
        symbol_data["-40% decline"] = False
        if not symbol_data["pDW_SMA"] > N_TIMES_EXCESS:
            message = f"{symbol_data['symbol']} corrected"
            return symbol_data, message
        
    # checking whether the ticker has corrected relative to its previous fall, 
    #   if the ticker price previously fell into the zone of 50% decline from the level of the twenty-week SMA, 
    #   and now exceeded the current SMA level by 50%, 
    #   then the asset is considered adjusted relative to the lowest border of the envelope
    if symbol_data.get("-50% decline") and symbol_data["pDW_SMA"] > N_TIMES_EXCESS:
        symbol_data["-30% decline"] = False
        symbol_data["-40% decline"] = False
        symbol_data["-50% decline"] = False
        message = f"{symbol_data['symbol']} corrected from the low point"
        return symbol_data, message

    # dictionary with keys - levels of the lower cutoffs for the envelope, indicated in percentages 
    #   and their values - price / twenty-week SMA ratios
    deviations = {
        "-30% decline": 0.7,
        "-40% decline": 0.6,
        "-50% decline": 0.5
    }

    # enumeration of the lower cutoffs of the envelope 
    #   and their comparison with the current price / twenty-week SMA ratio for the ticker
    for percent, portion in deviations.items():
        if not symbol_data.get(percent) and symbol_data["pDW_SMA"] < portion:
            # if the cutoff for the ticker is performed, 
            #   then a key is added to the dictionary with the ticker data that fixes the current state of the market
            symbol_data[percent] = True
            message = f"{symbol_data['symbol']} price is {percent} from twenty-week SMA"
            return symbol_data, message

    return symbol_data, None