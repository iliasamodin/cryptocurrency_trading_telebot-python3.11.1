# Envelope+
This program is designed for spot medium-term trading against the trend 
and long-term spot trading from potential trend reversal points.

## How it works
The trading strategy embedded in the program is based on the use of the classic Envelope tool on the weekly timeframe. 
The classic Envelope is modified with additional levels 
with a smaller deviation from the moving average (-30%, -40% of the SMA).
The principle of operation of the trading strategy and program:
the strategy has a moving average (in this case, a twenty-week SMA). 
Three levels are built on its basis: -30% below the SMA, -40% below, -50% below. 
The first two levels (-30%, -40% of the SMA) serve as potential entry points for a mid-term countertrend trade. 
The third level (-50% of the SMA) serves as a potential entry point for a long-term trade 
oriented to reversal from a downtrend into an uptrend.

Possible closing points for medium-term long positions may be 
the return of prices to the current level of the twenty-week SMA 
or the increase in the level of the second indicator - the four-hour RSI to its upper cut-off in the area above 70%.
A possible point of closing or reducing a long-term long position may be 
an increase in the value of the asset to the upper boundary of the Envelope -
a level exceeding by 50% the current value of the twenty-week SMA.

## Sources
The trading strategy is based on the Envelope indicator, the principle of which is described in detail in the book "Come Into My Trading Room: A Complete Guide to Trading" | Elder Alexander.

All values for the Envelope and RSI indicators are calculated based on observations of the movement patterns 
and volatility of the BTCUSDT and ETHUSDT tickers over the past twelve and seven years, respectively.
The strategy is only for Bitcoin and Ethereum. 
Other cryptocurrencies with a smaller capitalization may show significantly more volatility or turn out to be a scam.

## Recommendations
The strategy does not offer stop levels, but recommends using them.
The author of the strategy recommends following the rules of risk management -
no more than 2% of the total trading portfolio per trade,
especially for medium-term countertrend positions, 
for such trades the amount can be limited to 0.5-1% of the entire trading account.

## P.S.
The author of the repository is not responsible for any changes on your trading account when trading with this strategy. 
Trade smart!