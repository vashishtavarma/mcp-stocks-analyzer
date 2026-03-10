import yfinance as yf
import pandas as pd
from toon import encode
from src.errors import not_found, fetch_failed
import ta


def get_technical_indicators(symbol: str, period: str, interval: str) -> dict:
    """
    Compute technical indicators for a stock.

    Args:
        symbol: Yahoo Finance ticker (e.g., 'RELIANCE.NS', 'AAPL')
        period: Data lookback — '3mo', '6mo', '1y' (default '6mo')
        interval: Candle size — '1d', '1wk' (default '1d')

    Returns:
        dict with trend, momentum, volatility, volume, and signals
    """

    # --- 1. Fetch Data ---
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period, interval=interval)
    except Exception as e:
        return fetch_failed(symbol, e)

    if df.empty:
        return not_found(symbol, f"No price history for period='{period}', interval='{interval}'.")

    # Clean column names (yfinance sometimes returns multi-index)
    df.columns = [col if isinstance(col, str) else col[0] for col in df.columns]

    close = df["Close"]
    high = df["High"]
    low = df["Low"]
    volume = df["Volume"]
    latest = close.iloc[-1]

    # --- 2. Trend Indicators ---
    df["SMA_20"] = ta.trend.SMAIndicator(close, window=20).sma_indicator()
    df["SMA_50"] = ta.trend.SMAIndicator(close, window=50).sma_indicator()
    df["SMA_200"] = ta.trend.SMAIndicator(close, window=200).sma_indicator()
    df["EMA_12"] = ta.trend.EMAIndicator(close, window=12).ema_indicator()
    df["EMA_26"] = ta.trend.EMAIndicator(close, window=26).ema_indicator()

    # MACD
    macd_ind = ta.trend.MACD(close, window_slow=26, window_fast=12, window_sign=9)
    df["MACD"] = macd_ind.macd()
    df["MACD_signal"] = macd_ind.macd_signal()
    df["MACD_hist"] = macd_ind.macd_diff()

    # ADX
    adx_ind = ta.trend.ADXIndicator(high, low, close, window=14)
    df["ADX"] = adx_ind.adx()

    # --- 3. Momentum Indicators ---
    df["RSI_14"] = ta.momentum.RSIIndicator(close, window=14).rsi()

    # Stochastic
    stoch_ind = ta.momentum.StochasticOscillator(high, low, close, window=14, smooth_window=3)
    df["STOCH_K"] = stoch_ind.stoch()
    df["STOCH_D"] = stoch_ind.stoch_signal()

    # Williams %R
    df["WILLR_14"] = ta.momentum.WilliamsRIndicator(high, low, close, lbp=14).williams_r()

    # CCI
    df["CCI_20"] = ta.trend.CCIIndicator(high, low, close, window=20).cci()

    # --- 4. Volatility Indicators ---
    bb_ind = ta.volatility.BollingerBands(close, window=20, window_dev=2)
    df["BB_upper"] = bb_ind.bollinger_hband()
    df["BB_mid"] = bb_ind.bollinger_mavg()
    df["BB_lower"] = bb_ind.bollinger_lband()

    df["ATR_14"] = ta.volatility.AverageTrueRange(high, low, close, window=14).average_true_range()

    # --- 5. Volume Indicators ---
    df["OBV"] = ta.volume.OnBalanceVolumeIndicator(close, volume).on_balance_volume()
    df["VWAP"] = ta.volume.VolumeWeightedAveragePrice(high, low, close, volume).volume_weighted_average_price()
    df["VOL_SMA_20"] = ta.trend.SMAIndicator(volume.astype(float), window=20).sma_indicator()

    # --- 6. Build Response ---
    last = df.iloc[-1]
    prev = df.iloc[-2] if len(df) > 1 else last

    def safe(val):
        if val is None or pd.isna(val):
            return None
        return round(float(val), 2)

    # --- Signals ---
    signals = []

    # RSI
    rsi_val = safe(last.get("RSI_14"))
    if rsi_val is not None:
        if rsi_val > 70:
            signals.append({"indicator": "RSI", "signal": "OVERBOUGHT", "value": rsi_val})
        elif rsi_val < 30:
            signals.append({"indicator": "RSI", "signal": "OVERSOLD", "value": rsi_val})

    # MACD crossover
    macd_val = safe(last.get("MACD"))
    macd_sig = safe(last.get("MACD_signal"))
    macd_prev = safe(prev.get("MACD"))
    macd_sig_prev = safe(prev.get("MACD_signal"))
    if all(v is not None for v in [macd_val, macd_sig, macd_prev, macd_sig_prev]):
        if macd_prev < macd_sig_prev and macd_val > macd_sig:
            signals.append({"indicator": "MACD", "signal": "BULLISH_CROSSOVER", "value": macd_val})
        elif macd_prev > macd_sig_prev and macd_val < macd_sig:
            signals.append({"indicator": "MACD", "signal": "BEARISH_CROSSOVER", "value": macd_val})

    # Golden/Death Cross
    sma50 = safe(last.get("SMA_50"))
    sma200 = safe(last.get("SMA_200"))
    sma50_prev = safe(prev.get("SMA_50"))
    sma200_prev = safe(prev.get("SMA_200"))
    if all(v is not None for v in [sma50, sma200, sma50_prev, sma200_prev]):
        if sma50_prev < sma200_prev and sma50 > sma200:
            signals.append({"indicator": "SMA", "signal": "GOLDEN_CROSS", "value": f"50DMA({sma50}) > 200DMA({sma200})"})
        elif sma50_prev > sma200_prev and sma50 < sma200:
            signals.append({"indicator": "SMA", "signal": "DEATH_CROSS", "value": f"50DMA({sma50}) < 200DMA({sma200})"})

    # Bollinger Band breakout/squeeze
    bb_upper = safe(last.get("BB_upper"))
    bb_lower = safe(last.get("BB_lower"))
    bb_mid = safe(last.get("BB_mid"))
    if all(v is not None for v in [bb_upper, bb_lower, latest]):
        if latest > bb_upper:
            signals.append({"indicator": "BBANDS", "signal": "UPPER_BREAKOUT", "value": safe(latest)})
        elif latest < bb_lower:
            signals.append({"indicator": "BBANDS", "signal": "LOWER_BREAKOUT", "value": safe(latest)})
        if bb_mid:
            band_width = (bb_upper - bb_lower) / bb_mid
            if band_width < 0.05:
                signals.append({"indicator": "BBANDS", "signal": "SQUEEZE", "value": round(band_width, 4)})

    # Price vs MAs
    price_position = []
    for ma_name in ["SMA_20", "SMA_50", "SMA_200"]:
        ma_val = safe(last.get(ma_name))
        if ma_val is not None:
            price_position.append({
                "ma": ma_name,
                "value": ma_val,
                "price_position": "ABOVE" if latest > ma_val else "BELOW",
                "distance_pct": round(((latest - ma_val) / ma_val) * 100, 2)
            })

    # Relative volume
    vol_ratio = None
    vol_sma = safe(last.get("VOL_SMA_20"))
    if vol_sma and vol_sma > 0:
        vol_ratio = round(float(last["Volume"]) / vol_sma, 2)

    # Trend assessment
    adx_val = safe(last.get("ADX"))
    trend_strength = "WEAK"
    if adx_val:
        if adx_val > 40:
            trend_strength = "STRONG"
        elif adx_val > 25:
            trend_strength = "MODERATE"

    trend_direction = "NEUTRAL"
    if sma50 and sma200:
        if sma50 > sma200 and latest > sma50:
            trend_direction = "BULLISH"
        elif sma50 < sma200 and latest < sma50:
            trend_direction = "BEARISH"

    res = {
        "symbol": symbol,
        "last_price": safe(latest),
        "date": str(df.index[-1].date()) if hasattr(df.index[-1], "date") else str(df.index[-1]),

        "trend": {
            "direction": trend_direction,
            "strength": trend_strength,
            "adx": adx_val,
            "sma_20": safe(last.get("SMA_20")),
            "sma_50": sma50,
            "sma_200": sma200,
            "ema_12": safe(last.get("EMA_12")),
            "ema_26": safe(last.get("EMA_26")),
            "price_vs_ma": price_position,
            "macd": {
                "macd_line": macd_val,
                "signal_line": macd_sig,
                "histogram": safe(last.get("MACD_hist")),
            },
        },

        "momentum": {
            "rsi_14": rsi_val,
            "stoch_k": safe(last.get("STOCH_K")),
            "stoch_d": safe(last.get("STOCH_D")),
            "williams_r": safe(last.get("WILLR_14")),
            "cci_20": safe(last.get("CCI_20")),
        },

        "volatility": {
            "atr_14": safe(last.get("ATR_14")),
            "atr_pct": round(float(last["ATR_14"]) / latest * 100, 2) if not pd.isna(last.get("ATR_14", float("nan"))) else None,
            "bollinger": {
                "upper": bb_upper,
                "middle": bb_mid,
                "lower": bb_lower,
                "bandwidth": round((bb_upper - bb_lower) / bb_mid, 4) if all(v is not None for v in [bb_upper, bb_lower, bb_mid]) and bb_mid > 0 else None,
            },
        },

        "volume": {
            "current": int(last["Volume"]) if not pd.isna(last["Volume"]) else None,
            "avg_20": int(vol_sma) if vol_sma else None,
            "relative_volume": vol_ratio,
            "obv": safe(last.get("OBV")),
            "vwap": safe(last.get("VWAP")),
        },

        "signals": signals,
    }

    return encode(res)

if __name__ == "__main__":
    print(get_technical_indicators("RELIANCE.NS", period="6mo", interval="1d"))