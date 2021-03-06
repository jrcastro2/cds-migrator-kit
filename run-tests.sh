#!/usr/bin/env sh
# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
#
# cds-migrator-kit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

pydocstyle cds_migrator_kit tests docs && \
isort --check-only --diff && \
check-manifest --ignore ".travis-*" && \
sphinx-build -qnNW docs docs/_build/html && \
python setup.py test
