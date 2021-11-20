#SPDX-License-Identifier: MIT
"""
Metrics that provide data about with insight detection and reporting
"""
import datetime
import sqlalchemy as s
import pandas as pd
from augur.util import register_metric

@register_metric()
def deps1(self):
	"""
    Returns a timeseries of all the contributions to a project.

    DataFrame has these columns:
    data_source
	dep_name
	dep_language
	max

    :param repo_id: The repository's id
    :param repo_group_id: The repository's group id
    :return: DataFrame of persons/period
    """
	depsSQL = s.sql.text("""
			SELECT dep_name FROM repo_dependencies
		""")
	results = pd.read_sql(depsSQL, self.database, params={'repo_id'})

	return results
