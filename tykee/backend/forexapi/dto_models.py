from typing import Iterable, Dict, Union

import pandas as pd
from peakdetect import peakdetect


def calculate_backtest_stats(positions: Iterable) -> Dict[str, Union[float, int]]:
    """
    Calculates the backtest statistics based on the given positions.

    Parameters
    ----------
    positions
        Iterable of positions.

    Returns
    -------
    BacktestStats
        Statistics of the backtest.
    """
    positions = pd.DataFrame(positions)
    start_balance = positions['balance'].iloc[0] + positions['net_profit'].iloc[0]
    profit = round((positions.balance.iloc[-1] / start_balance - 1) * 100, 2)
    profit_factor = round(
        positions[positions.net_profit > 0].net_profit.sum()
        / abs(positions[positions.net_profit < 0].net_profit.sum()),
        2
    )
    dd = max_drawdown(positions.balance)
    total_trades = len(positions)
    wr = round(len(positions[positions.gross_profit > 0]) / total_trades * 100, 2)

    return {'profit': profit, 'profit_factor': profit_factor, 'drawdown': dd, 'total_trades': total_trades,
            'win_rate': wr}


def max_drawdown(balances: pd.Series):
    """
    Calculates the maximum drawdown of a given series of balances.
    Maximum drawdown is defined as the largest **relative** drop
    from a peak to a valley of the balance curve.

    Parameters
    ----------
    balances:
        pd.Series of balances.
    Returns
    -------
    max_dd, max_dd_percent:
        Maximum absolute drawdown and it's relative value.
    """
    max_balances, min_balances = max_min_peaks(balances)

    max_dd = 0
    max_dd_percent = 0
    # Find the max drawdown based on drawdown`s percentage, not the absolute value
    for max_b, min_b in zip(max_balances, min_balances):
        # Percentage is calculated based on the max balance
        drawdown = round((max_b[1] / min_b[1] - 1) * 100 * -1, 2)
        if drawdown < max_dd_percent:
            max_dd_percent = drawdown
            max_dd = round(min_b[1] - max_b[1], 2)

    return max_dd_percent


def max_min_peaks(values: pd.Series, lookahead: int = 3):
    """
    Finds the maximum and minimum peaks and troughs of a given series of values.
    Parameters
    ----------
    values
        pd.Series of values.
    lookahead
        Number of steps to look ahead to find a peak.
    Returns
    -------
    """
    org_max_peaks, min_peaks = peakdetect(values, lookahead=lookahead)
    org_max_peaks = org_max_peaks[:-1]
    min_peaks = min_peaks[1:]

    # peakdetect tends to find the peak after the actual peak, if the lookahead is too narrow
    # we need to check if the previous balance is higher than the peak
    max_peaks = []
    for peak in org_max_peaks:
        peak_idx = peak[0]
        peak_val = peak[1]
        if values[peak_idx - 1] > peak_val:
            peak = [peak_idx - 1, values[peak_idx - 1]]
        max_peaks.append(peak)

    return max_peaks, min_peaks
