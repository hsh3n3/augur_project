#SPDX-License-Identifier: MIT
"""
Metrics that provide data about with insight detection and reporting
"""
import datetime
import sqlalchemy as s
import pandas as pd
from augur.util import register_metric

@register_metric()
def deps1(self, repo_group_id, repo_id=None, begin_date=None, end_date=None, period='month'):
    """
    :param repo_id: The repository's id
    :param repo_group_id: The repository's group id
    :param period: To set the periodicity to 'day', 'week', 'month' or 'year', defaults to 'day'
    :param begin_date: Specifies the begin date, defaults to '1970-1-1 00:00:00'
    :param end_date: Specifies the end date, defaults to datetime.now()
    :return: DataFrame of persons/period
    """
    if not begin_date:
        begin_date = '1970-1-1 00:00:01'
    if not end_date:
        end_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    committersSQL = None

    if repo_id:
        committersSQL = s.sql.text(
            """
                SELECT DATE,
                    repo_name,
                    rg_name,
                    COUNT ( author_count ) 
                FROM
                    (
                    SELECT
                        date_trunc(:period, commits.cmt_author_date::date) as date,
                        repo_name,
                        rg_name,
                        cmt_author_name,
                        cmt_author_email,
                        COUNT ( cmt_author_name ) AS author_count 
                    FROM
                        commits, repo, repo_groups
                    WHERE
                        commits.repo_id = :repo_id AND commits.repo_id = repo.repo_id
                        AND repo.repo_group_id = repo_groups.repo_group_id
                        AND commits.cmt_author_date BETWEEN :begin_date and :end_date
                    GROUP BY date, repo_name, rg_name, cmt_author_name, cmt_author_email 
                    ORDER BY date DESC
                    ) C
                GROUP BY
                    C.DATE,
                    repo_name,
                    rg_name 
                ORDER BY C.DATE desc 
            """
        )
    else:
        committersSQL = s.sql.text(
            """
                SELECT DATE,
                    rg_name,
                    COUNT ( author_count ) 
                FROM
                    (
                    SELECT
                        date_trunc(:period, commits.cmt_author_date::date) as date,
                        rg_name,
                        cmt_author_name,
                        cmt_author_email,
                        COUNT ( cmt_author_name ) AS author_count 
                    FROM
                        commits, repo, repo_groups
                    WHERE
                        commits.repo_id = repo.repo_id
                        AND repo.repo_group_id = repo_groups.repo_group_id
                        AND commits.cmt_author_date BETWEEN :begin_date and :end_date
                        AND repo.repo_group_id = :repo_group_id
                    GROUP BY date, rg_name, cmt_author_name, cmt_author_email 
                    ORDER BY date DESC
                    ) C
                GROUP BY
                    C.DATE,
                    rg_name 
                ORDER BY C.DATE desc 
            """
        )

    results = pd.read_sql(committersSQL, self.database, params={'repo_id': repo_id, 
        'repo_group_id': repo_group_id,'begin_date': begin_date, 'end_date': end_date, 'period':period})

    return results
	# """
    # Returns a timeseries of all the contributions to a project.

    # DataFrame has these columns:
    # data_source
	# dep_name
	# dep_language
	# max

    # :param repo_id: The repository's id
    # :param repo_group_id: The repository's group id
    # :return: DataFrame of persons/period
    # """
	# deps1SQL = s.sql.text("""
	# 		SELECT dep_name FROM repo_dependencies
	# 	""")
	# results = pd.read_sql(deps1SQL, self.database)

	# return results


