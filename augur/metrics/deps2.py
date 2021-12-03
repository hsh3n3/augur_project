#SPDX-License-Identifier: MIT
"""
Metrics that provide data about with insight detection and reporting
"""
import datetime
import sqlalchemy as s
import pandas as pd
from augur.util import register_metric
from flask import request, Response, Flask

@register_metric()
def deps2(self):

    contributorsSQL = s.sql.text("""
        SELECT dep_name FROM repo_dependencies
    """)

    results = pd.read_sql(contributorsSQL, self.database, params={})
    return results