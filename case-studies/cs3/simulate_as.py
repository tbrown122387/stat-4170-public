"""Avellaneda-Stoikov toy simulator from the Module 8 demonstration."""

import numpy as np


def simulate_as(
    rng,
    T=1.0,
    dt=0.001,
    sigma=2.0,
    gamma=0.1,
    k=1.5,
    A=140.0,
    s0=100.0,
    max_inv=15,
):
    """Simulate one synthetic price path and return time, mid, inventory, PnL."""
    N = int(T / dt)
    times = np.arange(N + 1) * dt
    mid, inv, cash, pnl = (np.zeros(N + 1) for _ in range(4))
    mid[0] = s0

    for n in range(N):
        tau = T - times[n]
        s, q = mid[n], inv[n]
        reservation = s - q * gamma * sigma**2 * tau
        delta = (1 / gamma) * np.log(1 + gamma / k) + 0.5 * gamma * sigma**2 * tau
        bid, ask = reservation - delta, reservation + delta

        p_bid = 1 - np.exp(-A * np.exp(-k * (s - bid)) * dt)
        p_ask = 1 - np.exp(-A * np.exp(-k * (ask - s)) * dt)

        inv[n + 1], cash[n + 1] = q, cash[n]
        if q < max_inv and rng.uniform() < p_bid:
            inv[n + 1] += 1
            cash[n + 1] -= bid
        if q > -max_inv and rng.uniform() < p_ask:
            inv[n + 1] -= 1
            cash[n + 1] += ask

        mid[n + 1] = s + sigma * rng.normal(0, np.sqrt(dt))
        pnl[n + 1] = cash[n + 1] + inv[n + 1] * mid[n + 1]

    return times, mid, inv, pnl
