"""
Custom fields for forms - faqat zaruri fields
"""

def get_custom_fields():
    return {
        'Purchase Order': [
            {
                'fieldname': 'grand_total_uzs',
                'label': 'Grand Total (UZS)',
                'fieldtype': 'Currency',
                'read_only': 1,
                'insert_after': 'grand_total',
                'precision': 2
            },
            {
                'fieldname': 'grand_total_usd',
                'label': 'Grand Total (USD)',
                'fieldtype': 'Currency',
                'read_only': 1,
                'insert_after': 'grand_total_uzs',
                'precision': 2
            },
            {
                'fieldname': 'grand_total_display_html',
                'label': 'Grand Total (Dual Currency)',
                'fieldtype': 'HTML',
                'insert_after': 'grand_total_usd'
            }
        ],
        'Sales Order': [
            {
                'fieldname': 'grand_total_uzs',
                'label': 'Grand Total (UZS)',
                'fieldtype': 'Currency',
                'read_only': 1,
                'insert_after': 'grand_total',
                'precision': 2
            },
            {
                'fieldname': 'grand_total_usd',
                'label': 'Grand Total (USD)',
                'fieldtype': 'Currency',
                'read_only': 1,
                'insert_after': 'grand_total_uzs',
                'precision': 2
            },
            {
                'fieldname': 'grand_total_display_html',
                'label': 'Grand Total (Dual Currency)',
                'fieldtype': 'HTML',
                'insert_after': 'grand_total_usd'
            }
        ],
        'Sales Invoice': [
            {
                'fieldname': 'grand_total_uzs',
                'label': 'Grand Total (UZS)',
                'fieldtype': 'Currency',
                'read_only': 1,
                'insert_after': 'grand_total',
                'precision': 2
            },
            {
                'fieldname': 'grand_total_usd',
                'label': 'Grand Total (USD)',
                'fieldtype': 'Currency',
                'read_only': 1,
                'insert_after': 'grand_total_uzs',
                'precision': 2
            },
            {
                'fieldname': 'grand_total_display_html',
                'label': 'Grand Total (Dual Currency)',
                'fieldtype': 'HTML',
                'insert_after': 'grand_total_usd'
            }
        ],
        'Purchase Invoice': [
            {
                'fieldname': 'grand_total_uzs',
                'label': 'Grand Total (UZS)',
                'fieldtype': 'Currency',
                'read_only': 1,
                'insert_after': 'grand_total',
                'precision': 2
            },
            {
                'fieldname': 'grand_total_usd',
                'label': 'Grand Total (USD)',
                'fieldtype': 'Currency',
                'read_only': 1,
                'insert_after': 'grand_total_uzs',
                'precision': 2
            },
            {
                'fieldname': 'grand_total_display_html',
                'label': 'Grand Total (Dual Currency)',
                'fieldtype': 'HTML',
                'insert_after': 'grand_total_usd'
            }
        ]
        # item_name field already exists in standard Frappe, no need to create it
    }



