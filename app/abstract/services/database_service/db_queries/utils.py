"""Module containing utility functions for the db_queries package"""
from typing import Optional, List, re, Tuple

from app.abstract.services.database_service.db_queries.regex_constants import REGEX_FOR_WHERE, \
    REGEX_FOR_SQL_COMMANDS_AFTER_WHERE, LESS_RESTRICTIVE_REGEX_FOR_WHERE, REGEX_FOR_OPENING_BRACKET, \
    REGEX_FOR_CLOSING_BRACKET, REGEX_FOR_GROUP_BY


def _split_string_around_a_pattern(string: str, compiled_pattern: re.Pattern) -> List[str]:
    """Splits a given string around a given pattern returning string fragments"""
    return compiled_pattern.split(string)


def _is_a_subquery(sql_fragment: str) -> bool:
    """Returns true if the sql_fragment is part of a sub query"""
    closing_brackets = REGEX_FOR_CLOSING_BRACKET.findall(string=sql_fragment)
    opening_brackets = REGEX_FOR_OPENING_BRACKET.findall(string=sql_fragment)
    return len(closing_brackets) != len(opening_brackets)


def split_sql_statement_around_pattern(
        sql_statement: str, compiled_pattern: re.Pattern, replacement_clause: str = '') -> Tuple[str, str]:
    """Splits a given sql statement returning two fragments with appropriate replacements"""
    fragment_left_of_pattern = sql_statement
    fragment_right_of_pattern = ''

    fragments: List[str] = _split_string_around_a_pattern(
        compiled_pattern=compiled_pattern, string=sql_statement)

    if len(fragments) > 1:
        last_fragment = fragments[-1]
        other_fragments = fragments[:-1]

        if not _is_a_subquery(last_fragment):
            fragment_left_of_pattern = f' {replacement_clause} '.join(other_fragments)
            fragment_right_of_pattern = f' {replacement_clause} {last_fragment}'

    return fragment_left_of_pattern, fragment_right_of_pattern


def remove_where_statement_from_clause(where_clause: str) -> str:
    """In order to make putting 'WHERE' in the clause optional, we remove all traces of 'where'"""
    return LESS_RESTRICTIVE_REGEX_FOR_WHERE.sub(repl="", string=where_clause, count=1)


def insert_where_clause(sql_statement: str, where_clause: str) -> str:
    """Inserts a where clause into an sql statement and returns the new sql statement"""
    cleaned_where_clause = remove_where_statement_from_clause(where_clause=where_clause)

    sql_statement_split_around_common_commands = _split_string_around_a_pattern(
        string=sql_statement, compiled_pattern=REGEX_FOR_SQL_COMMANDS_AFTER_WHERE)

    first_fragment = sql_statement_split_around_common_commands[0].strip()

    word_for_merging = 'WHERE' if first_fragment == '' else 'AND'
    merged_first_fragment = f'{first_fragment} {word_for_merging} {cleaned_where_clause}'

    modified_sql_statement = sql_statement.replace(first_fragment, merged_first_fragment)

    return modified_sql_statement


def append_where_clause(sql_statement: str, where_clause: Optional[str]) -> str:
    """Adds the WHERE clause to the sql_statement in an appropriate position"""
    if where_clause is None:
        return sql_statement

    fragment_left_of_group_by_clause, fragment_right_of_group_by_clause = split_sql_statement_around_pattern(
        sql_statement=sql_statement,
        compiled_pattern=REGEX_FOR_GROUP_BY,
        replacement_clause='GROUP BY'
    )

    fragment_left_of_where_clause, fragment_right_of_where_clause = split_sql_statement_around_pattern(
        sql_statement=fragment_left_of_group_by_clause,
        compiled_pattern=REGEX_FOR_WHERE,
        replacement_clause='WHERE')

    fragment_right_of_where_clause = insert_where_clause(sql_statement=fragment_right_of_where_clause,
                                                         where_clause=where_clause)

    return f'{fragment_left_of_where_clause} {fragment_right_of_where_clause} {fragment_right_of_group_by_clause}'


def append_pagination_clause(sql_statement: str, limit: Optional[int] = None, offset: Optional[int] = None) -> str:
    """Appends the pagination clause to the sql statement"""
    sql = sql_statement

    if isinstance(offset, int):
        sql = f"{sql} OFFSET {offset}"
    if isinstance(limit, int):
        sql = f"{sql} LIMIT {limit}"

    return sql


def extract_sql_param_from_http_param(separator: str, http_param: str):
    """
    Extracts sql params from an http param with given separator,
    returning tuple of db_query_label and query_name
    """
    try:
        db_query_label, query_name = http_param.split(separator)
    except ValueError:
        raise Exception(
            f"""Query parameter: {http_param} should be of pattern 
            <DbQuery.label>{separator}<query_name>
            like da_ndf{separator}q""")

    return db_query_label, query_name
