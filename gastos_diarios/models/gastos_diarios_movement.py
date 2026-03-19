# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime

from openerp import models, fields, api, exceptions, _
from openerp.exceptions import except_orm, UserError, ValidationError


class GastosDiariosMovement(models.Model):
    _name = "gastos.diarios.movement"

    name = fields.Char(string='Descripción', required=False)
    date = fields.Datetime(string="Fecha", required=True)
    account_id = fields.Many2one('gastos.diarios.account', 'Cuenta', required=True)
    category_id = fields.Many2one('gastos.diarios.category', 'Categoria', required=True)
    amount = fields.Float('Monto', required=True)
    type = fields.Selection([('income', 'Ingresos'), ('expense', 'Gastos')], 'Tipo', required=True)
    month = fields.Selection([('01', 'Enero'),
    						  ('02', 'Febrero'),
    						  ('03', 'Marzo'),
    						  ('04', 'Abril'),
    						  ('05', 'Mayo'),
    						  ('06', 'Junio'),
    						  ('07', 'Julio'),
    						  ('08', 'Agosto'),
    						  ('09', 'Septiembre'),
    						  ('10', 'Octubre'),
    						  ('11', 'Noviembre'),
    						  ('12', 'Diciembre'),
    	                     ], 'Mes', required=True)
    year = fields.Char('Año', required=True)

