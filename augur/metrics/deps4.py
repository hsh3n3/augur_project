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
def deps4(self, repo_group_id):
    """
    Returns the name and count of every repo dependency ordered in descending order by count
    DataFrame has these columns:
	dep_name
    dep_count
    """

    contributorsSQL = s.sql.text("""
        SELECT dep_name, dep_count FROM repo_dependencies ORDER BY dep_count DESC;
    """)

    results = pd.read_sql(contributorsSQL, self.database, params={'repo_group_id': repo_group_id})
    return results