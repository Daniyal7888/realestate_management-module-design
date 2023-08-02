from odoo import fields, models, api


class EstateProperties(models.Model):

	_name = "estate.property.offer"

	_description = "Model for Real-Estate Properties"

	price = fields.Float('Price')
	status = fields.Selection(
		[('accepted', 'Accepted'), ('refused', 'Refused')],
		string='Status',
		copy=False
	)
	partner_id = fields.Many2one('res.partner', required=True)
	property_id = fields.Many2one('estate.property', required=True)
	validity = fields.Integer('Validity', default=7)
	date_deadline = fields.Date()

	def accept_offer(self):
		if self.property_id.state != 'offer_received':
			raise exceptions.UserError("Cannot accept offer. Property state must be 'Offer Received'.")
		self.property_id.state = 'offer_accepted'
		self.property_id.buyer = self.partner_id.name
		self.property_id.selling_price = self.price

	def refuse_offer(self):
		if self.property_id.state != 'offer_received':
			raise exceptions.UserError("Cannot refuse offer. Property state must be 'Offer Received'.")
		self.status = 'refused'

