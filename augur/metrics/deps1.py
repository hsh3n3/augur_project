#SPDX-License-Identifier: MIT
"""
Metrics that provide data about with insight detection and reporting
"""
import datetime
import sqlalchemy as s
import pandas as pd
from augur.util import register_metric
from flask import request, Response

@register_metric()
def deps0(self, repo_group_id, repo_id=None, period='day', begin_date=None, end_date=None):
    """
    Returns a timeseries of all the contributions to a project.

    DataFrame has these columns:
    date
    commits
    pull_requests
    issues
    commit_comments
    pull_request_comments
    issue_comments
    total

    :param repo_id: The repository's id
    :param repo_group_id: The repository's group id
    :param period: To set the periodicity to 'day', 'week', 'month' or 'year', defaults to 'day'
    :param begin_date: Specifies the begin date, defaults to '1970-1-1 00:00:00'
    :param end_date: Specifies the end date, defaults to datetime.now()
    :return: DataFrame of persons/period
    """

    # In this version, pull request, pr request comments,issue comments haven't be calculated
    if not begin_date:
        begin_date = '1970-1-1 00:00:01'
    if not end_date:
        end_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if repo_id:
        contributorsSQL = s.sql.text("""
           SELECT id                           AS user_id,
                SUM(commits)                 AS commits,
                SUM(issues)                  AS issues,
                SUM(commit_comments)         AS commit_comments,
                SUM(issue_comments)          AS issue_comments,
                SUM(pull_requests)           AS pull_requests,
                SUM(pull_request_comments)   AS pull_request_comments,
                SUM(a.commits + a.issues + a.commit_comments + a.issue_comments + a.pull_requests +
                    a.pull_request_comments) AS total,
                a.repo_id, repo.repo_name
            FROM (
                    (SELECT gh_user_id AS id,
                            0          AS commits,
                            COUNT(*)   AS issues,
                            0          AS commit_comments,
                            0          AS issue_comments,
                            0          AS pull_requests,
                            0          AS pull_request_comments,
                            repo_id
                    FROM issues
                    WHERE repo_id = :repo_id
                        AND created_at BETWEEN :begin_date AND :end_date
                        AND gh_user_id IS NOT NULL
                        AND pull_request IS NULL
                    GROUP BY gh_user_id, repo_id)
                    UNION ALL
                    (SELECT cmt_ght_author_id AS id,
                            COUNT(*)          AS commits,
                            0                 AS issues,
                            0                 AS commit_comments,
                            0                 AS issue_comments,
                            0                 AS pull_requests,
                            0                 AS pull_request_comments,
                            repo_id
                    FROM commits
                    WHERE repo_id = :repo_id
                        AND cmt_ght_author_id IS NOT NULL
                        AND cmt_committer_date BETWEEN :begin_date AND :end_date
                    GROUP BY cmt_ght_author_id, repo_id)
                    UNION ALL
                    (SELECT cntrb_id AS id,
                            0        AS commits,
                            0        AS issues,
                            COUNT(*) AS commit_comments,
                            0        AS issue_comments,
                            0        AS pull_requests,
                            0        AS pull_request_comments,
                            commits.repo_id as repo_id
                    FROM commit_comment_ref,
                        commits,
                        message
                    WHERE commit_comment_ref.cmt_id = commit_comment_ref.cmt_id
                        AND message.msg_id = commit_comment_ref.msg_id
                        AND commits.repo_id = :repo_id
                        AND created_at BETWEEN :begin_date AND :end_date
                    GROUP BY id, commits.repo_id)
                    UNION ALL
                    (
                        SELECT message.cntrb_id AS id,
                                0                AS commits,
                                0                AS issues,
                                0                AS commit_comments,
                                count(*)         AS issue_comments,
                                0                AS pull_requests,
                                0                AS pull_request_comments,
                            issues.repo_id as repo_id
                        FROM issues,
                            issue_message_ref,
                            message
                        WHERE issues.repo_id = :repo_id
                        AND gh_user_id IS NOT NULL
                        AND issues.issue_id = issue_message_ref.issue_id
                        AND issue_message_ref.msg_id = message.msg_id
                        AND issues.pull_request IS NULL
                        AND created_at BETWEEN :begin_date AND :end_date
                        GROUP BY id, issues.repo_id
                    )
                ) a, repo
            WHERE a.repo_id = repo.repo_id
            GROUP BY a.id, a.repo_id, repo_name
            ORDER BY total DESC
        """)

        results = pd.read_sql(contributorsSQL, self.database, params={'repo_id': repo_id, 'period': period,
                                                                'begin_date': begin_date, 'end_date': end_date})
    else:
        contributorsSQL = s.sql.text("""
           SELECT id                           AS user_id,
                SUM(commits)                 AS commits,
                SUM(issues)                  AS issues,
                SUM(commit_comments)         AS commit_comments,
                SUM(issue_comments)          AS issue_comments,
                SUM(pull_requests)           AS pull_requests,
                SUM(pull_request_comments)   AS pull_request_comments,
                SUM(a.commits + a.issues + a.commit_comments + a.issue_comments + a.pull_requests +
                    a.pull_request_comments) AS total, a.repo_id, repo_name
            FROM (
                    (SELECT gh_user_id AS id,
                            repo_id,
                            0          AS commits,
                            COUNT(*)   AS issues,
                            0          AS commit_comments,
                            0          AS issue_comments,
                            0          AS pull_requests,
                            0          AS pull_request_comments
                    FROM issues
                    WHERE repo_id in (SELECT repo_id FROM repo WHERE repo_group_id=:repo_group_id)
                        AND created_at BETWEEN :begin_date AND :end_date
                        AND gh_user_id IS NOT NULL
                        AND pull_request IS NULL
                    GROUP BY gh_user_id, issues.repo_id)
                    UNION ALL
                    (SELECT cmt_ght_author_id AS id,
                            repo_id,
                            COUNT(*)          AS commits,
                            0                 AS issues,
                            0                 AS commit_comments,
                            0                 AS issue_comments,
                            0                 AS pull_requests,
                            0                 AS pull_request_comments
                    FROM commits
                    WHERE repo_id in (SELECT repo_id FROM repo WHERE repo_group_id=:repo_group_id)
                        AND cmt_ght_author_id IS NOT NULL
                        AND cmt_committer_date BETWEEN :begin_date AND :end_date
                    GROUP BY cmt_ght_author_id, repo_id)
                    UNION ALL
                    (SELECT cntrb_id AS id,
                            commits.repo_id as repo_id,
                            0        AS commits,
                            0        AS issues,
                            COUNT(*) AS commit_comments,
                            0        AS issue_comments,
                            0        AS pull_requests,
                            0        AS pull_request_comments
                    FROM commit_comment_ref,
                        commits,
                        message
                    WHERE commit_comment_ref.cmt_id = commit_comment_ref.cmt_id
                        AND message.msg_id = commit_comment_ref.msg_id
                        AND commits.repo_id in (SELECT repo_id FROM repo WHERE repo_group_id=:repo_group_id)
                        AND created_at BETWEEN :begin_date AND :end_date
                    GROUP BY id, commits.repo_id)
                    UNION ALL
                    (
                        SELECT message.cntrb_id AS id,
                                issues.repo_id as repo_id,
                                0                AS commits,
                                0                AS issues,
                                0                AS commit_comments,
                                count(*)         AS issue_comments,
                                0                AS pull_requests,
                                0                AS pull_request_comments
                        FROM issues,
                            issue_message_ref,
                            message
                        WHERE issues.repo_id in (SELECT repo_id FROM repo WHERE repo_group_id=:repo_group_id)
                        AND gh_user_id IS NOT NULL
                        AND issues.issue_id = issue_message_ref.issue_id
                        AND issue_message_ref.msg_id = message.msg_id
                        AND issues.pull_request IS NULL
                        AND created_at BETWEEN :begin_date AND :end_date
                        GROUP BY id, issues.repo_id
                    )
                ) a, repo
            WHERE a.repo_id = repo.repo_id
            GROUP BY a.id, a.repo_id, repo_name
            ORDER BY total DESC
        """)

        results = pd.read_sql(contributorsSQL, self.database, params={'repo_group_id': repo_group_id, 'period': period,
                                                                'begin_date': begin_date, 'end_date': end_date})
    return results

@register_metric()
def deps1(self):

	return "<p>Feelsbadman</p>"

@register_metric()
def deps2(self):

	return "<h1>That wacky deps2 metric</h1>"

@app.route("/")
def deps3():

	return "<p>Sup Boiiiiiiiii!</p>"

@app.route("/")
def deps4():

	return "<h1>ThebigOl deps 4 route</h1>"





