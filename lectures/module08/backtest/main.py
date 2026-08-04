"""Pedagogical limit-order backtest: rest behind the touch, skew by inventory.

Strategy: whenever the best bid/ask changes, cancel our resting orders and
re-quote just behind the touch -- bid a bit below the best bid, ask a bit
above the best ask -- shifted by a fixed amount per unit of inventory (buy
less eagerly the more we already own, and vice versa). This is the same
inventory-skew idea from the Avellaneda-Stoikov model in the Module 8 slides,
just without the reservation-price math. Resting behind the touch instead of
improving it is what lets the strategy actually earn the spread rather than
pay for fill priority.

We only rest quotes during regular trading hours, 9:30 to 4:00 -- outside
that window we cancel any resting orders and just watch the tape.

Run with the `quant-ts` conda environment active, pointing at a quote/trade
tape in the same format as `scripts/20260401.txt`:
    python main.py ../../../scripts/20260401.txt
    python main.py ../../../scripts/20260401.txt --plot
    python main.py ../../../scripts/20260401.txt --plot --max-messages 2000000
"""

import argparse
from datetime import time as clock_time

from fake_broker import FakeBroker, OrderFilled, QuoteUpdate, TradePrint

QUOTE_OFFSET = 0.01  # how far behind the touch we rest our quotes
ORDER_SIZE = 1
INVENTORY_SKEW = 0.01  # price shift per share of inventory
MAX_INVENTORY = 20
MAX_MESSAGES = 300_000  # cap the tape length so the demo finishes quickly
MARKET_OPEN = clock_time(9, 30)
MARKET_CLOSE = clock_time(16, 0)


def handle_next_tick(broker, book):
    """Read one tick's worth of incoming messages and react by (re-)quoting.

    This is the function the main loop calls once per iteration: it (a) reads
    every message the fake broker produced for this tick -- market data and
    broker acks/fills alike -- and (b) sends whatever orders/cancels follow.
    """
    for message in broker.poll():
        if isinstance(message, QuoteUpdate):
            book["time"] = message.time
            book["best_bid"], book["best_ask"] = message.bid, message.ask
        elif isinstance(message, TradePrint):
            book["time"] = message.time
            book["last_trade_price"] = message.price
        elif isinstance(message, OrderFilled):
            if message.side == "buy":
                book["inventory"] += message.size
                book["cash"] -= message.price * message.size
            else:
                book["inventory"] -= message.size
                book["cash"] += message.price * message.size

    if book["best_bid"] is None:
        return

    mark = book["last_trade_price"]
    if mark is None:
        mark = 0.5 * (book["best_bid"] + book["best_ask"])
    book["pnl_history"].append((book["time"], book["cash"] + book["inventory"] * mark))

    trading_hours = MARKET_OPEN <= book["time"].time() < MARKET_CLOSE
    if not trading_hours:
        broker.cancel_order("buy")
        broker.cancel_order("sell")
        return

    skew = book["inventory"] * INVENTORY_SKEW
    desired_bid = round(book["best_bid"] - QUOTE_OFFSET - skew, 2)
    desired_ask = round(book["best_ask"] + QUOTE_OFFSET - skew, 2)

    broker.cancel_order("buy")
    broker.cancel_order("sell")
    if book["inventory"] < MAX_INVENTORY:
        broker.send_limit_order("buy", desired_bid, ORDER_SIZE)
    if book["inventory"] > -MAX_INVENTORY:
        broker.send_limit_order("sell", desired_ask, ORDER_SIZE)


def plot_pnl(pnl_history):
    import matplotlib.pyplot as plt

    times, pnls = zip(*pnl_history)
    plt.figure(figsize=(10, 5))
    plt.plot(times, pnls)
    plt.axhline(0, color="grey", ls="--", lw=1)
    plt.xlabel("time")
    plt.ylabel("PnL ($)")
    plt.title("Mark-to-Market PnL Over the Trading Day")
    plt.tight_layout()
    plt.show()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "data_path",
        help="path to a quote/trade tape in the same format as scripts/20260401.txt",
    )
    parser.add_argument(
        "--plot",
        action="store_true",
        help="show a plot of mark-to-market PnL over time when the backtest finishes",
    )
    parser.add_argument(
        "--max-messages",
        type=int,
        default=MAX_MESSAGES,
        help=f"stop after this many tape lines, to keep the demo fast (default: {MAX_MESSAGES})",
    )
    args = parser.parse_args()

    broker = FakeBroker(args.data_path)
    book = {
        "time": None,
        "best_bid": None,
        "best_ask": None,
        "last_trade_price": None,
        "inventory": 0,
        "cash": 0.0,
        "pnl_history": [],
    }

    for _ in range(args.max_messages):
        if broker.done:
            break
        handle_next_tick(broker, book)

    broker.close()

    mark = book["last_trade_price"]
    pnl = book["cash"] + book["inventory"] * mark
    print(f"final inventory: {book['inventory']} shares")
    print(f"final cash:      {book['cash']:,.2f}")
    print(f"mark-to-market:  {mark:.2f}")
    print(f"total PnL:       {pnl:,.2f}")

    if args.plot:
        plot_pnl(book["pnl_history"])


if __name__ == "__main__":
    main()
