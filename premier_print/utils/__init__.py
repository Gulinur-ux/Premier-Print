# Utils package init
import frappe
import requests
from datetime import datetime, timedelta

@frappe.whitelist(allow_guest=True)
def get_usd_to_uzs_rate():
    """
    Get current USD to UZS exchange rate from CBU (Central Bank of Uzbekistan) API
    Returns the exchange rate or None if failed
    """
    try:
        # Check if we have a cached rate from today
        cache_key = f"usd_uzs_rate_{datetime.now().date()}"
        cached_rate = frappe.cache().get(cache_key)

        if cached_rate:
            return float(cached_rate)

        # Fetch from CBU API
        response = requests.get('https://cbu.uz/uz/arkhiv-kursov-valyut/json/', timeout=5)

        if response.status_code == 200:
            data = response.json()

            # Find USD in the response (Ccy: "USD")
            for currency in data:
                if currency.get('Ccy') == 'USD':
                    rate = float(currency.get('Rate'))

                    # Cache for 24 hours
                    frappe.cache().set(cache_key, rate, expires_in_sec=86400)

                    return rate

        # If API fails, return last known rate or default
        return get_fallback_rate()

    except Exception as e:
        frappe.log_error(f"Error fetching USD rate: {str(e)}", "USD Exchange Rate Error")
        return get_fallback_rate()


def get_fallback_rate():
    """
    Get fallback exchange rate from system settings or default value
    """
    try:
        # Try to get from Exchange Rate doctype (Frappe built-in)
        exchange_rate = frappe.db.get_value(
            'Currency Exchange',
            {
                'from_currency': 'USD',
                'to_currency': 'UZS',
            },
            'exchange_rate'
        )

        if exchange_rate:
            return float(exchange_rate)
    except:
        pass

    # Default fallback rate (approximate current rate)
    return 12700.0


@frappe.whitelist(allow_guest=True)
def calculate_usd_amount(uzs_amount, exchange_rate=None):
    """
    Calculate USD amount from UZS amount
    """
    if not exchange_rate:
        exchange_rate = get_usd_to_uzs_rate()

    if uzs_amount and exchange_rate:
        return float(uzs_amount) / float(exchange_rate)

    return 0
