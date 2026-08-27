"""
10771 E 28th Place, Denver 80238 -- buy vs. rent-and-invest.

Compares buying the house (live 2 years, let it for the rest) against renting
and holding the same capital in equities. The 2-year buy-and-sell case is out
of scope: it is not under consideration.

Every scenario starts with the same cash and pays all housing costs from it,
so the end balances are directly comparable.
"""

POT      = 623_000     # cash available in every scenario
PRICE    = 600_000     # assumed purchase price
CLOSING  = 3_000       # cash purchase: title, inspections, recording
SELLCOST = 0.07        # commissions, title, seller concession
RENT0    = 3_300 * 12  # like-for-like rent on this house
RENTG    = 0.03
CARRY    = 5_700 + 700 + 3_500 + 5_000   # tax, MCA, insurance, maintenance
PM, VAC, LEASEFEE = 0.08, 0.05, 1_650
DEPR     = PRICE * 0.80 / 27.5
LIVE_YRS = 2           # years occupied before returning to Taiwan


def invest(years, r):
    """Rent for LIVE_YRS, hold the capital in equities returning r."""
    bal = POT
    for y in range(years):
        bal *= 1 + r
        if y < LIVE_YRS:
            bal -= RENT0 * (1 + RENTG) ** y
    return bal


def buy(years, g):
    """Buy, occupy LIVE_YRS, then let it. g = annual house appreciation."""
    bal = POT - PRICE - CLOSING
    for y in range(years):
        bal *= 1 + 0.036                      # idle cash sits in T-bills
        if y < LIVE_YRS:
            bal -= CARRY
        else:
            gross = RENT0 * (1 + RENTG) ** y
            bal += gross * (1 - PM - VAC) - LEASEFEE - CARRY
    sale = PRICE * (1 + g) ** years * (1 - SELLCOST)
    recapture = DEPR * max(0, years - LIVE_YRS) * 0.25
    return bal + sale - recapture


def breakeven(years, r):
    """House appreciation needed to match an equity return of r."""
    lo, hi = -0.10, 0.40
    for _ in range(200):
        mid = (lo + hi) / 2
        if buy(years, mid) < invest(years, r):
            lo = mid
        else:
            hi = mid
    return mid


def house_total_return(years, g):
    """Annualised return on the whole buy scenario, for comparison with r."""
    lo, hi = -0.50, 0.50
    for _ in range(200):
        mid = (lo + hi) / 2
        if invest(years, mid) < buy(years, g):
            lo = mid
        else:
            hi = mid
    return mid


if __name__ == "__main__":
    EQUITY = [0.03, 0.04, 0.05, 0.065, 0.08, 0.10]
    for horizon in (5, 10):
        print(f"\n=== {horizon}-year horizon "
              f"({LIVE_YRS} occupied, {horizon - LIVE_YRS} let) ===")
        print(f"{'equity return':>14} {'house must appreciate':>23}")
        for r in EQUITY:
            print(f"{r:>13.1%} {breakeven(horizon, r):>22.2%}/yr")

        print(f"\n{'house appreciation':>19} {'equivalent equity return':>26}")
        for g in (0.00, 0.02, 0.03, 0.04, 0.07):
            print(f"{g:>18.1%} {house_total_return(horizon, g):>25.2%}/yr")
