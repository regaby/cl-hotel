#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import csv
from tempfile import TemporaryFile
from tempfile import mkstemp
import os
from openerp import models, fields, api, exceptions, _
#import xlwt, xlrd, xlutils
import xlrd
import time
# from datetime import date
# from datetime import datetime
# from datetime import timedelta
import datetime


class GastosDiariosImportMovement(models.TransientModel):
    """ Language Import """

    _name = "gastos.diarios.import.movement"
    _description = "gastos.diarios.import.movement"

    # _columns = {
    #     'data': fields.binary('Archivo Asistencias', required=True),
    #     'info': fields.text('Info'),
    #     'device': fields.selection([('reloj_1','Reloj Principal'),('reloj_2', 'Reloj Secundario')], 'Dispositivo', required=True),
    #     'state': fields.selection( ( ('choose','choose'), ('done','done') ) ),
    # }

    # _defaults = {
    #              'state': lambda *a: 'choose',
    #              'device': lambda *a: 'reloj_1',
    #             }
    data = fields.Binary('Archivo', required=True)
    state = fields.Selection([('choose','choose'), ('done','done')], default='choose')
    info = fields.Text('Info')

    @api.multi
    def import_movements(self):
        # employee_obj = self.pool.get('hr.employee')
        # atend_obj = self.pool.get('hr.attendance')
        info = ""
        cuenta_obj = self.env['gastos.diarios.account']
        categoria_obj = self.env['gastos.diarios.category']
        movement_obj = self.env['gastos.diarios.movement']

        # import_data = self.browse(cr, uid, ids)[0]
        import_data = self
        fd, temp_path = mkstemp()
        os.system('some_commande --output %s' % temp_path)
        file = open(temp_path, 'w+')
        file.write(base64.decodestring(import_data.data))
        file.close()

        try:
            book = xlrd.open_workbook(temp_path)
            sh = book.sheet_by_index(0)
        except:
            raise osv.except_osv(_('Error !'),_('No se pudo procesar el archivo seleccionado. \nPruebe exportar el archivo como Excel (8.0) e intente nuevamente.'))
            info+="No se pudo procesar el archivo seleccionado.\n"
            return self.write({'state':'done', 'info':info,})
        for rx in range(5,sh.nrows):
            fecha = sh.cell_value(rowx=rx, colx=1)
            if fecha == '':
                continue
            cuenta = sh.cell_value(rowx=rx, colx=3)
            categoria = sh.cell_value(rowx=rx, colx=4)
            ingreso = sh.cell_value(rowx=rx, colx=5)
            gasto = sh.cell_value(rowx=rx, colx=6)
            descripcion = sh.cell_value(rowx=rx, colx=7)

            # temp = datetime.datetime(1900, 1, 1)
            temp = datetime.datetime(1899, 12, 30)
            delta = datetime.timedelta(days=fecha)
            fecha_new = temp+delta

            cuenta_id = cuenta_obj.search([('name','=',cuenta)])
            if not cuenta_id:
                cuenta_id = cuenta_obj.create({'name': cuenta})
            categoria_id = categoria_obj.search([('name','=',categoria)])
            if not categoria_id:
                categoria_id = categoria_obj.create({'name': categoria})
            monto = 0
            type = ''
            if ingreso > 0:
                monto = ingreso
                type = 'income'
            else:
                monto = gasto * -1
                type = 'expense'
            vals = {
                'account_id': cuenta_id.id,
                'category_id': categoria_id.id,
                'amount': monto,
                'name': descripcion,
                'date': fecha_new,
                'type': type,
                'month': str(fecha_new.month).zfill(2),
                'year': str(fecha_new.year),
            }
            movement_obj.create(vals)


        os.close(fd)
        os.remove(temp_path)

        if info=="":
            info="(Registros procesados sin errores)"

        self.write({'state':'done', 'info':info,})
        view_id = self.env['ir.ui.view'].search([('model','=','gastos.diarios.import.movement')])
        print self.ids
        print view_id
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'gastos.diarios.import.movement',
            'name': _('Importar movimientos'),
            'res_id': self.id,
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': view_id.id,
            'target': 'new',
             'nodestroy': True,
             'context': self.env.context
                }


GastosDiariosImportMovement()

