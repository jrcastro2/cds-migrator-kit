# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
#
# cds-migrator-kit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""CDS Migrator Records views."""

from __future__ import absolute_import, print_function

import logging

from flask import Blueprint, current_app, render_template, send_from_directory

from cds_migrator_kit.config import CDS_MIGRATOR_KIT_LOGS_PATH

from .log import JsonLogger

cli_logger = logging.getLogger('migrator')


blueprint = Blueprint(
    'cds_migrator_kit_records',
    __name__,
    template_folder='templates',
    static_folder='static',
)


@blueprint.route("/")
def index():
    """Render a basic view."""
    return render_template(
        "cds_migrator_kit_records/welcome.html",
    )


@blueprint.route("/results")
def results():
    """Render a basic view."""
    all_stats = JsonLogger().render_stats()
    return render_template(
        "cds_migrator_kit_records/index.html",
        results=all_stats)


@blueprint.route('/record/<rectype>/<recid>')
def send_json(rectype, recid):
    """Serves static json preview output files."""
    cli_logger.warning('View reached')
    cli_logger.warning(CDS_MIGRATOR_KIT_LOGS_PATH)
    cli_logger.warning('{0}_{1}.json'.format(rectype, recid))
    return send_from_directory(
        current_app.config['CDS_MIGRATOR_KIT_LOGS_PATH'],
        '{0}_{1}.json'.format(rectype, recid))
