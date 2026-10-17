"""Tool pages — currency converter and markets/assets watch."""
import json
import random

from django.shortcuts import render
from django.http import JsonResponse

# Fallback NGN rates (1 unit → NGN) used when the live API is unreachable.
FALLBACK_NGN_RATES = {
    "USD": 1450.0, "GBP": 1850.0, "EUR": 1580.0, "GHS": 95.0,
    "KES": 11.2, "ZAR": 80.0, "CAD": 1050.0, "AUD": 940.0,
    "JPY": 9.6, "INR": 17.2, "CNY": 200.0, "AED": 395.0,
    "NGN": 1.0,
}
CURRENCY_NAMES = {
    "USD": "US Dollar", "GBP": "British Pound", "EUR": "Euro",
    "GHS": "Ghanaian Cedi", "KES": "Kenyan Shilling", "ZAR": "South African Rand",
    "CAD": "Canadian Dollar", "AUD": "Australian Dollar", "JPY": "Japanese Yen",
    "INR": "Indian Rupee", "CNY": "Chinese Yuan", "AED": "UAE Dirham",
    "NGN": "Nigerian Naira",
}

# Watchlist seed data: symbol → (name, market, base price, day change %)
WATCHLIST = [
    ("DANGCEM", "Dangote Cement", "NGX", 415.00, 1.2),
    ("MTNN", "MTN Nigeria", "NGX", 268.50, -0.8),
    ("BUACEMENT", "BUA Cement", "NGX", 112.30, 0.4),
    ("GTCO", "Guaranty Trust", "NGX", 68.95, 2.1),
    ("ZENITHBANK", "Zenith Bank", "NGX", 48.20, -1.1),
    ("AIRTELAFRI", "Airtel Africa", "NGX", 2250.00, 0.9),
    ("SEPLAT", "Seplat Energy", "NGX", 5300.00, 1.8),
    ("NIBOR-91", "Treasury Bill 91d", "FIXED", 17.4, 0.0),
    ("BTC", "Bitcoin", "CRYPTO", 97250.0, 2.7),
    ("ETH", "Ethereum", "CRYPTO", 3420.0, 1.9),
    ("GOLD", "Gold (oz)", "COMMODITY", 2648.0, 0.3),
    ("BRENT", "Brent Crude", "COMMODITY", 74.2, -0.6),
]


def _series(base, change_pct, points=24):
    """Deterministic fake intraday series so charts look alive."""
    rng = random.Random(int(base * 100) + points)
    out, price = [], base * (1 - change_pct / 100)
    for _ in range(points):
        price += rng.uniform(-0.004, 0.0045) * base
        out.append(round(price, 2))
    out[-1] = round(base, 2)
    return out


def _get_ngn_rates():
    """Return NGN conversion rates, preferring the live provider."""
    rates = dict(FALLBACK_NGN_RATES)
    live = False
    try:
        import urllib.request

        with urllib.request.urlopen(
            "https://open.er-api.com/v6/latest/NGN", timeout=3
        ) as resp:
            data = json.loads(resp.read().decode())
            for code, rate in data.get("rates", {}).items():
                if rate:
                    rates[code] = round(1 / rate, 4)
            live = True
    except Exception:
        pass  # fall back to the embedded rates
    return rates, live


def currency_rates(request):
    """Small JSON endpoint used by the converter for live AJAX refreshes."""
    rates, live = _get_ngn_rates()
    return JsonResponse({"rates": rates, "live": live})


def currency_converter(request):
    rates, live = _get_ngn_rates()

    return render(
        request,
        "tools/currency_converter.html",
        {
            "nav_active": "tools",
            "rates_json": json.dumps(rates),
            "names_json": json.dumps(CURRENCY_NAMES),
            "currencies": sorted(CURRENCY_NAMES.items()),
            "live": live,
        },
    )


def markets(request):
    assets = _market_assets()
    return render(
        request,
        "tools/markets.html",
        {"nav_active": "tools", "assets_json": json.dumps(assets), "assets": assets},
    )


def _market_assets():
    return [
        {"symbol": symbol, "name": name, "market": market, "price": price,
         "change": change, "series": _series(price, change)}
        for symbol, name, market, price, change in WATCHLIST
    ]


def market_snapshot(request):
    """AJAX snapshot. Crypto values are refreshed from CoinGecko; other feeds fall back safely."""
    assets = _market_assets()
    live = False
    try:
        import urllib.parse
        import urllib.request

        query = urllib.parse.urlencode({
            "ids": "bitcoin,ethereum",
            "vs_currencies": "usd",
            "include_24hr_change": "true",
        })
        req = urllib.request.Request(
            f"https://api.coingecko.com/api/v3/simple/price?{query}",
            headers={"Accept": "application/json", "User-Agent": "TNE-Market-Snapshot/1.0"},
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            prices = json.loads(resp.read().decode())
        lookup = {"BTC": "bitcoin", "ETH": "ethereum"}
        for asset in assets:
            coin = lookup.get(asset["symbol"])
            if coin and coin in prices:
                asset["price"] = prices[coin].get("usd", asset["price"])
                asset["change"] = round(prices[coin].get("usd_24h_change", asset["change"]), 2)
        live = True
    except Exception:
        pass
    return JsonResponse({"assets": assets, "live": live})
