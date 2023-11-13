from odoo import fields, models

class ResUsersInherited(models.Model):
    _inherit = "res.users"

    # Add the One2many field to link properties to users
    property_ids = fields.One2many(
        'estate.property', 'seller_id',
        string='Linked Properties',
        domain="[('seller_id', '=', id)]",
    )
