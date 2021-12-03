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
def deps3(self, repo_group_id):
    """
    Returns the name of every dependency of all loaded repos
    DataFrame has these columns:
	dep_name
    """

    contributorsSQL = s.sql.text("""
        SELECT dep_name FROM repo_dependencies
    """)

    results = pd.read_sql(contributorsSQL, self.database, params={'repo_group_id': repo_group_id})
    return results