"""
Setup utilities for Premier Print app
"""
import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def create_fields():
    """Create all custom fields"""
    from premier_print.custom_fields import get_custom_fields
    
    custom_fields = get_custom_fields()
    create_custom_fields(custom_fields, update=True)
    
    frappe.db.commit()
    return "Custom fields created successfully!"

def hide_apply_tax_withholding():
    """Hide apply_tax_withholding_amount field"""
    try:
        # Check if it exists first
        existing = frappe.get_list('Property Setter', filters={
            'doc_type': 'Purchase Order',
            'field_name': 'apply_tax_withholding_amount',
            'property': 'hidden'
        })
        
        if not existing:
            ps = frappe.new_doc('Property Setter')
            ps.doctype_or_field = 'DocField'
            ps.doc_type = 'Purchase Order'
            ps.field_name = 'apply_tax_withholding_amount'
            ps.property = 'hidden'
            ps.value = '1'
            ps.insert()
            frappe.db.commit()
            return "Property Setter created!"
        else:
            return "Property Setter already exists!"
    except Exception as e:
        return f"Error: {str(e)}"

def setup_all():
    """Setup everything"""
    create_fields()
    hide_apply_tax_withholding()
    return "Premier Print customization complete!"

@frappe.whitelist()
def setup_purchase_order():
    """Whitelisted method to setup PO customization"""
    try:
        create_fields()
        hide_apply_tax_withholding()
        frappe.msgprint("Purchase Order customization applied successfully!")
        return {"success": True}
    except Exception as e:
        frappe.msgprint(f"Error: {str(e)}")
        return {"success": False, "error": str(e)}
