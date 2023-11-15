from odoo import api, fields, models, exceptions
from datetime import datetime, timedelta


class EstateProperties(models.Model):
    _name = "estate.property"
    _description = "Model for Real-Estate Properties"

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    highest_offer = fields.Float(string='Highest Offer', compute='_compute_highest_offer', store=True)
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string='Date Availability')
    expected_price = fields.Float(string='Expected Price', required=True, default=0.0)
    selling_price = fields.Float(string='Selling Price', readonly=True, copy=False)
    availability_date = fields.Date(string="Availability Date", copy=False,
                                    default=lambda self: fields.Date.today() + timedelta(days=90))
    bedrooms = fields.Integer(string='Bedrooms', default=2)
    living_area = fields.Float(string='Living Area (sqm)')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Float(string='Garden Area (sqm)')
    data_availability = fields.Date(string='Data Availability')
    property_type_id = fields.Many2one(
        "estate.property.type", string="Property Type", required=True
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    seller_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)

    state = fields.Selection([
        ('new', 'New'),
        ('draft', 'Draft'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled'),
    ], string="State", required=True, copy=False, default='new')
    best_price = fields.Float(string="Best Price")
    garden_orientation = fields.Selection(
        [('North', 'North'),
         ('South', 'South'),
         ('East', 'East'),
         ('West', 'West')
         ],
        string='Garden Orientation'
    )
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tags")

    total_area = fields.Float(string='Total Area', compute='_compute_total_area', store=True)

    # @api.model
    # def action_cancel(self):
    #     self.ensure_one()
    #     for record in self:
    #         if record.state == 'sold':
    #             raise exceptions.UserError("A sold property cannot be canceled.")
    #         record.state = 'canceled'
    #
    # @api.model
    # def action_set_sold(self):
    #     self.ensure_one()
    #     for record in self:
    #         if record.state == 'canceled':
    #             raise exceptions.UserError("A canceled property cannot be set as sold.")
    #         record.state = 'sold'

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_highest_offer(self):
        for record in self:
            if record.offer_ids:
                highest_offer = max(offer.price for offer in record.offer_ids)
                record.highest_offer = highest_offer
            else:
                record.highest_offer = 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            # Set default values when 'garden' is True
            self.garden_area = 10.0
            self.garden_orientation = 'North'
        else:
            # Clear fields when 'garden' is False
            self.garden_area = 0.0
            self.garden_orientation = False


