# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime

from openerp import models, fields, api, exceptions, _
from openerp.exceptions import except_orm, UserError, ValidationError


class GastosDiariosAccount(models.Model):
    _name = "gastos.diarios.account"

    name = fields.Char(string='Nombre', required=True)

