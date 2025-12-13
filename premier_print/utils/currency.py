"""
Global Currency Exchange Rate Utility
CBU dan real-time USD/UZS kurs olish
"""
import frappe
import requests
from datetime import datetime
from frappe.utils import cstr
import json

def get_cbu_exchange_rate():
    """
    CBU (Central Bank of Uzbekistan) dan real-time USD/UZS kursini oladi
    Cache'da 5 minut saqlaydi (keyin update qilinadi)
    """
    try:
        # Cache'dan birinchi olib ko'r
        cached_rate = frappe.cache().get_value('cbu_usd_uzs_rate')
        if cached_rate:
            rate = float(cached_rate)
            frappe.logger().info(f"Using cached rate: {rate}")
            return rate
        
        # CBU API endpoint
        url = "https://cbu.uz/uz/arkhiv-kursov-valyut/json/"
        
        frappe.logger().info(f"Fetching exchange rate from: {url}")
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        
        # USD ni topish (currency code: 840 = USD)
        for item in data:
            if item.get('Code') == '840' or item.get('Code') == 'USD':
                rate = float(item.get('Rate', 0))
                frappe.logger().info(f"CBU API rate: {rate}")
                
                # Cache'ga 5 minut uchun saqla
                frappe.cache().set_value('cbu_usd_uzs_rate', str(rate), expires_in_sec=300)
                return rate
        
        # Agar USD topilmasa, fallback rate qaytarish
        frappe.logger().warning("USD not found in CBU response")
        return get_fallback_rate()
        
    except requests.RequestException as e:
        frappe.logger().warning(f"CBU API request error: {str(e)}")
        return get_fallback_rate()
    except Exception as e:
        frappe.logger().warning(f"CBU API error: {str(e)}")
        return get_fallback_rate()

def get_fallback_rate():
    """
    Oldingi saqlangan kursni qaytaradi yoki default
    """
    try:
        # Database'dan last rate'ni olib ko'r
        rate_doc = frappe.db.get_value(
            "Currency Exchange Rate",
            filters={"from_currency": "USD", "to_currency": "UZS"},
            fieldname="exchange_rate",
            order_by="creation desc"
        )
        if rate_doc:
            fallback_rate = float(rate_doc)
            frappe.logger().info(f"Using fallback DB rate: {fallback_rate}")
            return fallback_rate
    except Exception as e:
        frappe.logger().warning(f"Error getting fallback rate: {str(e)}")
    
    # Default rate agar hech narsa topilmasa
    frappe.logger().warning("Using default rate: 12500")
    return 12500.0

@frappe.whitelist()
def get_exchange_rate():
    """
    Frontend dan chaqiriladigan whitelisted method
    Real-time kurs bilan timestamp'ni qaytaradi
    """
    try:
        rate = get_cbu_exchange_rate()
        result = {
            "rate": rate,
            "from_currency": "USD",
            "to_currency": "UZS",
            "timestamp": cstr(datetime.now()),
            "source": "CBU Real-Time"
        }
        frappe.logger().info(f"Exchange rate returned: {result}")
        return result
    except Exception as e:
        frappe.logger().error(f"Error in get_exchange_rate: {str(e)}")
        return {
            "rate": 12500.0,
            "from_currency": "USD",
            "to_currency": "UZS",
            "timestamp": cstr(datetime.now()),
            "source": "DEFAULT"
        }

def convert_currency(amount, from_currency="UZS", to_currency="USD"):
    """
    Bir valyutadan boshqasiga konvertirish
    """
    if from_currency == to_currency:
        return amount
    
    rate = get_cbu_exchange_rate()
    
    if from_currency == "UZS" and to_currency == "USD":
        return amount / rate
    elif from_currency == "USD" and to_currency == "UZS":
        return amount * rate
    
    return amount


