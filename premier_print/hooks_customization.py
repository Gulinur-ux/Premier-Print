"""
Purchase Order va Sales Order uchun server-side hooks
"""
import frappe

def hide_apply_tax_withholding():
    """
    "Apply Tax Withholding Amount" fieldni hidden qilish
    """
    property_setters = [
        {
            'doc_type': 'Purchase Order',
            'field_name': 'apply_tax_withholding_amount',
        },
        {
            'doc_type': 'Sales Order',
            'field_name': 'apply_tax_withholding_amount',
        },
        {
            'doc_type': 'Sales Invoice',
            'field_name': 'apply_tax_withholding_amount',
        },
        {
            'doc_type': 'Purchase Invoice',
            'field_name': 'apply_tax_withholding_amount',
        }
    ]
    
    for ps_dict in property_setters:
        try:
            existing = frappe.db.exists('Property Setter', {
                'doc_type': ps_dict['doc_type'],
                'field_name': ps_dict['field_name'],
                'property': 'hidden'
            })
            
            if not existing:
                ps = frappe.new_doc('Property Setter')
                ps.doctype_or_field = 'DocField'
                ps.doc_type = ps_dict['doc_type']
                ps.field_name = ps_dict['field_name']
                ps.property = 'hidden'
                ps.value = '1'
                ps.insert(ignore_permissions=True)
                frappe.logger().info(f"Hidden: {ps_dict['doc_type']}.{ps_dict['field_name']}")
        except Exception as e:
            frappe.logger().warning(f"Error hiding field: {str(e)}")
    
    frappe.db.commit()

@frappe.whitelist()
def apply_tax_withholding_customization():
    """
    Whitelisted method to apply customization from UI
    """
    try:
        hide_apply_tax_withholding()
        return {"success": True, "message": "Customization applied successfully"}
    except Exception as e:
        return {"success": False, "error": str(e)}
