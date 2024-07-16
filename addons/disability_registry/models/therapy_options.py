from odoo import models, fields

class TherapyOption(models.Model):
    _name = 'therapy.option'
    _description = 'Therapy Options'

    name = fields.Char(string='Therapy Option')