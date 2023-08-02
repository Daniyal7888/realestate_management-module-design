from odoo import fields, models, api
# from dateutil.relativedelta import relativedelta

class EstateProperties(models.Model):

	_name = "estate.property"

	_description = "Model for Real-Estate Properties"


	name = fields.Char('Name',default='Unknown', required=True)
	title = fields.Char('Title ')
	description=fields.Text('Description')
	postcode=fields.Char('Postcode')
	date_availability=fields.Date('Date', copy=False, )
	expected_price=fields.Float('Expected Price', required=True)
	selling_price=fields.Float('Selling Price', copy=False)
	bedrooms=fields.Integer(string='Bedrooms', default=2)
	living_area=fields.Integer('Living Area(sqm)')
	facades=fields.Integer('Facecades')
	garage=fields.Boolean('Garage')
	garden=fields.Boolean('Garden')
	garden_area=fields.Integer('Garden Area')
	garden_orientation = fields.Selection(
		string='Garden Orientation',
		selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
		help="Choose the orientation of the garden (North, South, East, or West)"
	)

	_sql_constraints = [
		('positive_expected_price', 'CHECK(expected_price > 0)', 'Expected price must be strictly positive!'),
		('positive_selling_price', 'CHECK(selling_price >= 0)', 'Selling price must be positive!')
	]

	state = fields.Selection(selection=[(('new'),('New')),('offer_received', 'Offer Received'),('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),('canceled', 'Canceled')],string='State',copy=False,default='new')
	last_seen = fields.Datetime("Last Seen", default=lambda self: fields.Datetime.now())
	property_type_id=fields.Many2one('estate.property.type')
	user_id = fields.Many2one('res.users', string='Salesperson', index=True, tracking=True,
							  default=lambda self: self.env.user)



	@api.model
	def _default_name(self):
		return self.env.user.name if self.env.user else 'Unknown'
	salesperson=fields.Char('Sales_Person', default=_default_name, required=True)

	tag_ids=fields.Many2many('estate.property.tag')

	offer_if=fields.Char('estate.property.offer')
	total_area=fields.Float('Total Area')
	best_price=fields.Float('Best price')


	price = fields.Float('Price')
	status = fields.Selection(
		[('accepted', 'Accepted'), ('refused', 'Refused')],
		string='Status',
		copy=False
	)
	partner = fields.Char("Partner")

	@api.depends('debit', 'credit')
	def _compute_balance(self):
		for line in self:
			total_area = living_area+garden_area

	partner_id = fields.Many2one("res.partner", string="Partner")
	salesman=fields.Char('Salesman' )
	buyer = fields.Char('Buyer', copy=False)

	@api.onchange("partner_id")
	def _onchange_partner_id(self):
		self.name = "Document for %s" % (self.partner_id.name)
		self.description = "Default description for %s" % (self.partner_id.name)

		# Check if the garden field is set to True
		if self.garden:
			# Set default values for garden_area and garden_orientation
			self.garden_area = 10
			self.garden_orientation = 'north'
		else:
			# Clear the fields when garden is unset
			self.garden_area = False
			self.garden_orientation = False


		def action_cancel_property(self):
			if self.state == 'sold':
				raise exceptions.UserError("Cannot cancel a sold property.")
			self.state = 'canceled'

		def action_set_property_sold(self):
			if self.state == 'canceled':
				raise exceptions.UserError("Cannot set a canceled property as sold.")
			self.state = 'sold'

		@api.constrains('expected_price', 'selling_price')
		def _check_selling_price(self):
			for record in self:
				if not float_is_zero(record.expected_price, precision_digits=2):
					if float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2) == -1:
						raise exceptions.ValidationError(
							"Selling price cannot be lower than 90% of the expected price!")
