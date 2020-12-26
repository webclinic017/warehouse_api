"""Module containing some REGEX constants important for this package"""

import re

REGEX_FOR_WHERE: re.Pattern = re.compile(r'\sWHERE\s', flags=re.DOTALL | re.IGNORECASE)
LESS_RESTRICTIVE_REGEX_FOR_WHERE: re.Pattern = re.compile(r'WHERE\s+', flags=re.DOTALL | re.IGNORECASE)
REGEX_FOR_ORDER: re.Pattern = re.compile(r'\sORDER\s+BY\s', flags=re.DOTALL | re.IGNORECASE)
REGEX_FOR_GROUP_BY: re.Pattern = re.compile(r'\sGROUP\s+BY\s', flags=re.DOTALL | re.IGNORECASE)
REGEX_FOR_CLOSING_BRACKET: re.Pattern = re.compile(r'\)', flags=re.DOTALL | re.IGNORECASE)
REGEX_FOR_OPENING_BRACKET: re.Pattern = re.compile(r'\(', flags=re.DOTALL | re.IGNORECASE)
REGEX_FOR_SQL_COMMANDS_AFTER_WHERE: re.Pattern = re.compile(
    r'\sGROUP\s+BY\s(?!.*\))|\sORDER\s+BY\s(?!.*\))', flags=re.DOTALL | re.IGNORECASE)
