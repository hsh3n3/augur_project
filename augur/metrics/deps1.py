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
def deps1(self, repo_group_id, period='day', begin_date=None, end_date=None):
    
    contributorsSQL = s.sql.text("""
        SELECT repo_dependencies.repo_id, data_source, dep_name, dep_language, max(data_collection_date)
        FROM repo_dependencies, (select repo_id, max(data_collection_date) as thedate from repo_dependencies group by repo_id) a 
        WHERE a.repo_id = repo_dependencies.repo_id and a.thedate=repo_dependencies.data_collection_date
        GROUP BY repo_dependencies.repo_id, data_source, dep_name, dep_language
        ORDER BY repo_id, dep_language, dep_name;
    """)

    results = pd.read_sql(contributorsSQL, self.database, params={'repo_group_id': repo_group_id, 'period': period,
                                                            'begin_date': begin_date, 'end_date': end_date})

    return results
