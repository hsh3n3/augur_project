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
def deps1(self):
    contributorsSQL = s.sql.text("""
           SELECT dep_name, dep_count FROM repo_dependencies ORDER BY dep_count DESC;
        """)

    results = pd.read_sql(contributorsSQL, self.database)

    return results