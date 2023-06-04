def calculate_vwap(data, closeCol='close', volumeCol='volume'):
    """
    the Volume-Weighted Average Price (VWAP) is a trading indicator that calculates the average price a
    stock has traded at throughout the day, weighted by the trading volume at each price level.

    Parameters
    ----------
    data
    closeCol
    volumeCol


    Returns
    -------

    """

    cumulative_volume_price = (data[volumeCol] * data[closeCol]).cumsum()
    cumulative_volume = data[volumeCol].cumsum()
    vwap = cumulative_volume_price / cumulative_volume
    return vwap


def calculate_stochastic_oscillator(data, period=14, smoothing=3):
    """
     Traders often use the crossing of the %K and %D lines or the position of these lines in relation to
     overbought (typically above 80) and oversold (typically below 20) levels as potential buy or sell signals.

    Parameters
    ----------
    data
    period
    smoothing


    Returns
    -------

    """

    # Calculate the lowest low and highest high over the specified period
    lowest_low = data.rolling(window=period).min()
    highest_high = data.rolling(window=period).max()

    # Calculate the %K
    k_percent = 100 * ((data - lowest_low) / (highest_high - lowest_low))

    # Calculate the %D (smoothing)
    d_percent = k_percent.rolling(window=smoothing).mean()

    return k_percent, d_percent


def calculate_rsi(data, period=14):
    """
    Relative Strength Index (RSI): RSI measures the speed and change of price movements to determine
    overbought or oversold conditions. It is often used to identify potential reversal points in the market.

    provides insights into whether a stock is overbought or oversold and can indicate potential trend reversals

    RSI value above 70 is considered overbought, suggesting that the stock may be due for a pullback.
    Conversely, an RSI value below 30 is considered oversold,
    Parameters
    ----------
    data
    period


    Returns
    -------

    """

    # Calculate price changes
    delta = data.diff().dropna()

    # Separate gains and losses
    gains = delta.where(delta > 0, 0)
    losses = -delta.where(delta < 0, 0)

    # Calculate average gains and losses
    avg_gain = gains.rolling(window=period).mean()
    avg_loss = losses.rolling(window=period).mean()

    # Calculate relative strength (RS)
    rs = avg_gain / avg_loss

    # Calculate RSI
    rsi = 100 - (100 / (1 + rs))

    return rsi


def calculate_technical_indicators(data, indicators, closeColumn="close", volumeCol='volume'):
    """
    WARNING: when calculating RSI and S0, the first n values will be NaN, where n is the period of the indicator

    Parameters
    ----------
    data
    indicators
    closeColumn
    volumeCol

    Returns
    -------

    """

    try:
        for indicator in indicators:
            if "RSI" in indicator:
                arguments = indicator.split("_")
                data["RSI_" + arguments[1]] = calculate_rsi(data[closeColumn], int(arguments[1]))
            elif "SO" in indicator:
                arguments = indicator.split("_")
                data["SOk_" + arguments[1]], data["SOd_" + arguments[1]] = calculate_stochastic_oscillator(
                    data[closeColumn], int(arguments[1]))
            elif "VWAP" in indicator:
                VW = calculate_vwap(data, closeColumn, volumeCol)
                data["VWAP"] = VW
            elif "PCTC" in indicator:
                arguments = indicator.split("_")
                data["PCTC_" + arguments[1]] = data[closeColumn].pct_change(int(arguments[1]))

    except ValueError as e:
        print("WARNING:", e)
    except Exception as e:
        print("WARNING:", e)
    return data
