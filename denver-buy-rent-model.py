POT      = 623_000     # same starting cash in every scenario
PRICE    = 600_000
CLOSING  = 3_000
SGOV     = 0.0360
SELLCOST = 0.07
RENT0    = 3_300 * 12  # like-for-like rent on THIS house
RENTG    = 0.03
CARRY    = 5_700 + 700 + 3_500 + 5_000   # tax, MCA, insurance, maintenance
PM       = 0.08
VAC      = 0.05
LEASEFEE = 1_650
DEPR     = PRICE * 0.80 / 27.5

def rent_scenario(years):
    bal = POT
    for y in range(years):
        bal *= (1 + SGOV)
        if y < 2:                       # only pays US rent while living there
            bal -= RENT0 * (1 + RENTG) ** y
    return bal

def buy_scenario(years, g):
    bal = POT - PRICE - CLOSING
    for y in range(years):
        bal *= (1 + SGOV)
        if y < 2:
            bal -= CARRY
        else:
            gross = RENT0 * (1 + RENTG) ** y
            bal += gross - gross * PM - gross * VAC - LEASEFEE - CARRY
    sale = PRICE * (1 + g) ** years * (1 - SELLCOST)
    rec  = DEPR * max(0, years - 2) * 0.25
    return bal + sale - rec

for horizon in (2, 5):
    print(f"\n=== {horizon}-year horizon ===")
    print(f"rent baseline: ${rent_scenario(horizon):,.0f}")
    for g in (0, .01, .02, .03, .04, .05):
        d = buy_scenario(horizon, g) - rent_scenario(horizon)
        print(f"  {g:.0%}/yr  buy-minus-rent: {d:+,.0f}")
    lo, hi = -0.02, 0.12
    for _ in range(80):
        mid = (lo + hi) / 2
        if buy_scenario(horizon, mid) - rent_scenario(horizon) < 0: lo = mid
        else: hi = mid
    print(f"  break-even appreciation: {mid:.2%}/yr")

print("\n=== rental-phase net income (yrs 3-5) ===")
for y in (2, 3, 4):
    gross = RENT0 * (1 + RENTG) ** y
    print(f"  yr{y+1}: gross ${gross:,.0f}  net ${gross - gross*PM - gross*VAC - LEASEFEE - CARRY:,.0f}")
print(f"\nannual owning cost incl. opportunity: ${CARRY + (PRICE+CLOSING)*SGOV:,.0f}  vs rent ${RENT0:,.0f}")

# Variant sweep: which unconfirmed inputs actually move the break-even.
# See variants table in denver-central-park-house.html
