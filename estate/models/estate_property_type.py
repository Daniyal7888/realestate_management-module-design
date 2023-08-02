from odoo import fields, models, api


class EstateProperties(models.Model):

	_name = "estate.property.type"

	_description = "Model for Real-Estate Properties"


	name = fields.Char('Name', required=True)
