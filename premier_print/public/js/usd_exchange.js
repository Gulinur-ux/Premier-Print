// Universal USD Exchange Rate Management for Premier Print
// Works for Sales Order, Purchase Order, Sales Invoice, Purchase Invoice

window.premier_print = window.premier_print || {};

premier_print.fetch_usd_rate = function(frm, force_refresh = false) {
    frappe.call({
        method: 'premier_print.utils.get_usd_to_uzs_rate',
        callback: function(r) {
            if (r.message) {
                // Set exchange rate field based on doctype
                frm.set_value('usd_exchange_rate', r.message);

                if (force_refresh) {
                    frappe.show_alert({
                        message: __('USD Exchange Rate updated from CBU: 1 USD = {0} UZS', [r.message.toFixed(2)]),
                        indicator: 'green'
                    });
                }

                // Recalculate totals
                premier_print.calculate_totals(frm);
            }
        },
        error: function(r) {
            frappe.show_alert({
                message: __('Failed to fetch USD rate from CBU API. Using default rate: 12,700 UZS'),
                indicator: 'orange'
            });
        }
    });
};

premier_print.get_exchange_rate = function(frm) {
    return frm.doc.usd_exchange_rate || 12700;
};

premier_print.toggle_usd_fields = function(frm) {
    let is_uzs = frm.doc.currency === 'UZS';
    let is_usd = frm.doc.currency === 'USD';

    // Show exchange rate and calculated fields based on currency
    frm.toggle_display('usd_exchange_rate', is_uzs || is_usd);
    frm.toggle_display('grand_total_usd', is_uzs);
    frm.toggle_display('grand_total_uzs', is_usd);

    // For item-level fields (if they exist)
    if (frm.fields_dict.items && frm.fields_dict.items.grid) {
        frm.fields_dict.items.grid.update_docfield_property('rate_usd', 'hidden', !is_uzs);
        frm.fields_dict.items.grid.update_docfield_property('amount_usd', 'hidden', !is_uzs);
    }

    frm.refresh_field('items');
};

premier_print.hide_unnecessary_fields = function(frm) {
    // Hide unnecessary standard fields that aren't needed for Premier Print
    const fields_to_hide = [
        'price_list_rate',
        'discount_percentage',
        'discount_amount',
        'margin_type',
        'margin_rate_or_amount',
        'base_rate',
        'base_amount',
        'base_net_rate',
        'base_net_amount'
    ];

    // Hide fields from items table
    if (frm.fields_dict.items && frm.fields_dict.items.grid) {
        fields_to_hide.forEach(function(fieldname) {
            frm.fields_dict.items.grid.update_docfield_property(fieldname, 'hidden', 1);
            frm.fields_dict.items.grid.update_docfield_property(fieldname, 'in_list_view', 0);
        });
    }

    // Hide price list field from parent form
    setTimeout(() => {
        frm.set_df_property('selling_price_list', 'hidden', 1);
        frm.set_df_property('buying_price_list', 'hidden', 1);
        frm.set_df_property('price_list_currency', 'hidden', 1);
        frm.set_df_property('plc_conversion_rate', 'hidden', 1);
        frm.set_df_property('ignore_pricing_rule', 'hidden', 1);
    }, 100);
};

premier_print.calculate_totals = function(frm) {
    if (!frm.doc.grand_total || !frm.doc.usd_exchange_rate) {
        return;
    }

    let exchange_rate = frm.doc.usd_exchange_rate;

    // If currency is UZS, calculate USD equivalent
    if (frm.doc.currency === 'UZS') {
        let grand_total_usd = frm.doc.grand_total / exchange_rate;
        frm.set_value('grand_total_usd', grand_total_usd);
    }
    // If currency is USD, calculate UZS equivalent
    else if (frm.doc.currency === 'USD') {
        let grand_total_uzs = frm.doc.grand_total * exchange_rate;
        frm.set_value('grand_total_uzs', grand_total_uzs);
    }
};

premier_print.calculate_item_usd = function(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    let exchange_rate = premier_print.get_exchange_rate(frm);

    // Only calculate if currency is UZS
    if (frm.doc.currency !== 'UZS') {
        return;
    }

    if (row.rate && exchange_rate) {
        let rate_usd = row.rate / exchange_rate;
        frappe.model.set_value(cdt, cdn, 'rate_usd', rate_usd);
    }

    if (row.amount && exchange_rate) {
        let amount_usd = row.amount / exchange_rate;
        frappe.model.set_value(cdt, cdn, 'amount_usd', amount_usd);
    }
};

