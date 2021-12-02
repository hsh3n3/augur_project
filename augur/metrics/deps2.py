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
def deps2(self, repo_group_id):
    """
    Returns all dependencies used in the most recent data collection for all repos or specific repos
    DataFrame has these columns:
    repo_id
	data_source
	dep_name
	dep_language
	date
    :param repo_id: The repository's id
    :param repo_group_id: The repository's group id
    :return: DataFrame of persons/period
    """

    contributorsSQL = s.sql.text("""
        SELECT dep_name FROM repo_dependencies
    """)

    results = pd.read_sql(contributorsSQL, self.database, params={'repo_group_id': repo_group_id})
    return results
