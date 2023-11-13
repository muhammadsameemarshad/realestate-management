from odoo import api, models, fields, exceptions
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"

    validity = fields.Integer(default=7)
    name = fields.Char(string='Name', required=True, default='New Offer')
    price = fields.Float(string="Price", required=True)
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")],
        string="Status",
        required=True,
    )
    partner_id = fields.Many2one(
        "res.partner", string="Partner", required=True, ondelete="restrict"
    )
    property_id = fields.Many2one(
        "estate.property",
        string="Property",
        required=True,
        ondelete="cascade",
        domain="[('state', 'in', ('new', 'offer_received'))]",
    )
    date_deadline = fields.Date(string="Validity Date", compute='_compute_date_deadline',
                                inverse='_inverse_date_deadline', store=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], default='draft', string='Offer State')

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = offer.create_date + timedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.create_date and offer.date_deadline:
                create_date = offer.create_date.date()  # Convert to datetime.date
                offer.validity = (offer.date_deadline - create_date).days

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            # Set default values when the 'garden' field is checked
            self.garden_area = 10.0
            self.orientation = "north"
        else:
            # Clear the values when the 'garden' field is unchecked
            self.garden_area = 0.0
            self.orientation = False

    _sql_constraints = [
        ('check_expected_price_positive', 'CHECK(expected_price >= 0)', 'Expected price must be strictly positive.'),
        ('check_selling_price_positive', 'CHECK(selling_price >= 0)', 'Selling price must be positive.'),
    ]

    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price < 0:
                raise ValidationError("Selling price must be positive.")
            if record.selling_price > 0 and record.expected_price > 0 and \
                    record.selling_price < 0.9 * record.expected_price:
                raise ValidationError("Selling price cannot be lower than 90% of the expected price.")

    # @api.model
    # #
    # def action_accept(self):
    #     self.ensure_one()
    #     for record in self:
    #         if record.property_id.state == 'sold':
    #             raise exceptions.UserError("A sold property cannot accept offers.")
    #         record.property_id.buyer_id = record.buyer_id
    #         record.property_id.selling_price = record.price
    #         record.state = 'accepted'
    #
    # def action_refuse(self):
    #     self.ensure_one()
    #     for record in self:
    #         record.state = 'refused'

