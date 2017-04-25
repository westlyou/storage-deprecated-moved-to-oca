# -*- coding: utf-8 -*-
# Copyright 2017 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models
import logging

_logger = logging.getLogger(__name__)


class StorageFile(models.Model):
    _name = 'storage.file'
    _description = 'Storage File'
    _inherit = 'ir.attachment'

    # redefinition du field
    url = fields.Char(help="HTTP accessible path for odoo backend to the file")
    private_path = fields.Char(help='Location for backend, may be relative')
    public_url = fields.Char(
        compute='_compute_url',
        help='Public url like CDN')  # ou path utile ?
    backend_id = fields.Many2one(
        'storage.backend',
        'Storage',
        required=True)

    # forward compliency to v9 and v10
    checksum = fields.Char("Checksum/SHA1", size=40, select=True, readonly=True)
    mimetype = fields.Char('Mime Type', readonly=True)
    index_content = fields.Char('Indexed Content', readonly=True)
    public = fields.Boolean('Is public document')

    the_file = fields.Binary(
        help="The file",
        inverse='_inverse_set_file',
        compute='_compute_get_file',
        store=False)

    def _inverse_set_file(self):
        _logger.warning('comupte set file [parent]')
        import pdb
        pdb.set_trace()

    def _compute_get_file(self):
        _logger.warning('comupte get file [parent]')
        return True

    def _compute_url(self):
        _logger.info('compute_url du parent')
        return self.backend_id.get_public_url(self)

    def get_base64(self):
        _logger.info('file.get_base64')
        return self.backend_id.get_base64(self)