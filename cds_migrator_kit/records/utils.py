# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
#
# cds-migrator-kit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""CDS Migrator Records utils."""
import copy
import json
import os
import re

from flask import current_app
from fuzzywuzzy import fuzz


def process_fireroles(fireroles):
    """Extract firerole definitions."""
    rigths = set()
    for firerole in fireroles:
        for (allow, not_, field, expressions_list) in firerole[1]:
            if not allow:
                current_app.logger.warning(
                    'Not possible to migrate deny rules: {0}.'.format(
                        expressions_list))
                continue
            if not_:
                current_app.logger.warning(
                    'Not possible to migrate not rules: {0}.'.format(
                        expressions_list))
                continue
            if field in ('remote_ip', 'until', 'from'):
                current_app.logger.warning(
                    'Not possible to migrate {0} rule: {1}.'.format(
                        field, expressions_list))
                continue
            # We only deal with allow group rules
            for reg, expr in expressions_list:
                if reg:
                    current_app.logger.warning(
                        'Not possible to migrate groups based on regular'
                        ' expressions: {0}.'.format(expr))
                    continue
                clean_name = expr[
                    :-len(' [CERN]')].lower().strip().replace(' ', '-')
                rigths.add('{0}@cern.ch'.format(clean_name))
    return rigths


def update_access(data, *access):
    """Merge access rights information.

    :params data: current JSON structure with metadata and potentially an
        `_access` key.
    :param *access: List of dictionaries to merge to the original data, each of
        them in the form `action: []`.
    """
    current_rules = data.get('_access', {})
    for a in access:
        for k, v in a.items():
            current_x_rules = set(current_rules.get(k, []))
            current_x_rules.update(v)
            current_rules[k] = list(current_x_rules)

    data['_access'] = current_rules


def same_issn(obj1, obj2):
    """Check if two objects have the same ISSN."""
    return obj1['issn'] is not None and obj2['issn'] is not None and \
        obj1['issn'] == obj2['issn']


def compare_titles(title1, title2):
    """Return the ratio of the fuzzy comparison between two titles."""
    return fuzz.ratio(title1, title2)


def clean_exception_message(message):
    """Cleanup exception message."""
    match = re.match(r'^(\[[^\]]*\])?(.*)$', message)
    if match:
        return match.group(2).strip().capitalize()
    return message
