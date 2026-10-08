"""A fake broker for a zero-latency, limit-order backtest.

Reads the real SPY tick data used elsewhere in Module 7/8
(`data/20260812_spy.txt`) and turns each line into an incoming message: either
a quote update (a new best bid/ask) or a trade print. It also holds our own
resting limit orders and, on every trade print, checks whether that trade
would have crossed one of them -- if so it manufactures an OrderFilled message.

"Zero latency" here means our orders/cancels take effect the instant they're
sent, with no simulated wire delay -- not that we can see the future. Only
information from lines already read is ever used.
"""

import re
from dataclasses import dataclass
from datetime import datetime


@dataclass
class QuoteUpdate:
    time: datetime
    bid: float
    ask: float


@dataclass
class TradePrint:
    time: datetime
    price: float
    size: int


@dataclass
class OrderAccepted:
    order_id: int
    side: str


@dataclass
class OrderCanceled:
    order_id: int
    side: str


@dataclass
class OrderFilled:
    order_id: int
    side: str
    price: float
    size: int


def _parse_line(line):
    body = line.strip()
    body = body[len("MarketData(") : -1]
    parts = re.split(r", (?=\w+=)", body)
    fields = dict(part.split("=", 1) for part in parts)
    time = datetime.strptime(fields["local_time"], "%Y-%m-%d %H:%M:%S.%f")
    if "bid" in fields:
        return QuoteUpdate(time, float(fields["bid"]), float(fields["ask"]))
    return TradePrint(time, float(fields["last"]), int(fields["size"]))


class FakeBroker:
    """Plays back a ticker's quote/trade tape and matches our resting limit orders."""

    def __init__(self, data_path):
        self._file = open(data_path)
        self._resting = {}
        self._next_order_id = 1
        self._pending_broker_messages = []
        self.done = False

    def send_limit_order(self, side, price, size):
        """Place a resting limit order, replacing any existing order on that side."""
        order_id = self._next_order_id
        self._next_order_id += 1
        self._resting[side] = (order_id, price, size)
        self._pending_broker_messages.append(OrderAccepted(order_id, side))

    def cancel_order(self, side):
        """Cancel the resting order on `side`, if one exists."""
        resting = self._resting.pop(side, None)
        if resting is not None:
            self._pending_broker_messages.append(OrderCanceled(resting[0], side))

    def poll(self):
        """Read one tape line and return broker messages followed by its market event."""
        line = self._file.readline()
        if not line:
            self.done = True
            return []

        messages = self._pending_broker_messages
        self._pending_broker_messages = []

        event = _parse_line(line)
        messages.append(event)

        if isinstance(event, TradePrint):
            messages.extend(self._check_fill(event))

        return messages

    def _check_fill(self, trade):
        fills = []
        buy = self._resting.get("buy")
        if buy is not None and trade.price <= buy[1]:
            fills.append(OrderFilled(buy[0], "buy", buy[1], min(buy[2], trade.size)))
            del self._resting["buy"]
        sell = self._resting.get("sell")
        if sell is not None and trade.price >= sell[1]:
            fills.append(OrderFilled(sell[0], "sell", sell[1], min(sell[2], trade.size)))
            del self._resting["sell"]
        return fills

    def close(self):
        self._file.close()
