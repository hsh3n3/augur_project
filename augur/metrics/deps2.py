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
def deps2(self, repo_group_id, period='day', begin_date=None, end_date=None):

    if not begin_date:
        begin_date = '1970-1-1 00:00:01'
    if not end_date:
        end_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
    contributorsSQL = s.sql.text("""
        SELECT a.repo_id, a.NAME, PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY a.LIBYEAR) as median
        FROM (
            SELECT repo_id, NAME, data_collection_date, libyear
            FROM repo_deps_libyear
            WHERE data_collection_date BETWEEN :begin_date AND :end_date
            ) AS a
        GROUP BY a.repo_id, a.NAME;
    """)

    results = pd.read_sql(contributorsSQL, self.database, params={'repo_group_id': repo_group_id, 'period': period,
                                                            'begin_date': begin_date, 'end_date': end_date})
    return results
