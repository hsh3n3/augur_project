#SPDX-License-Identifier: MIT
"""
Metrics that provide data about with insight detection and reporting
"""

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
	# if repo_id:
	# 	depsSQL = s.sql.text("""
	# 		SELECT repo_dependencies.repo_id, data_source, dep_name, dep_language, max(data_collection_date)
	# 		FROM repo_dependencies, (select repo_id, max(data_collection_date) as thedate from repo_dependencies group by repo_id) a 
	# 		where a.repo_id = repo_dependencies.repo_id and a.thedate=repo_dependencies.data_collection_date
	# 		group by repo_dependencies.repo_id, data_source, dep_name, dep_language
	# 		ORDER BY repo_id, dep_language, dep_name;
	# 	""")
	# 	results = pd.read_sql(depsSQL, self.database, params={'repo_id'})

	# else:
	# 	depsSQL = s.sql.text("""
	# 		SELECT repo_dependencies.repo_id, data_source, dep_name, dep_language, max(data_collection_date)
	# 		FROM repo_dependencies, (select repo_id, max(data_collection_date) as thedate from repo_dependencies group by repo_id) a 
	# 		where a.repo_id = repo_dependencies.repo_id and a.thedate=repo_dependencies.data_collection_date
	# 		group by repo_dependencies.repo_id, data_source, dep_name, dep_language
	# 		ORDER BY repo_id, dep_language, dep_name;
	# 	""")
	# 	results = pd.read_sql(depsSQL, self.database)

	# return results

	print("Hello World")
