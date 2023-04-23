""" Data Mart Dumper

This program takes in a formatted EON extract of SBD's Redshift Table DDLs and generates crt_ models that can be placed
in the dbt project. The purpose of crt_ models is to simply create the tables in the warehouse so that they exist when
converting the Redshift stored procedures.

Note: Any table that already exists won't be create and any table that is created by a dbt model will be overwritten.
Note: Convert the .sql file to a .txt file by changing the extension before running the script.

Future Updates:
    - Handle quote formatting (possibly , followed by "")
    - Handle IDENTITY data types
    - Create Constraint formatting
"""

import re
import os
import regex
import argparse

WRITE_LOCATION = os.getcwd()
TXT_FILE_LOCATION = ''

# Change this to where you want the files to be dumped, otherise they will be dumped in the current working directory
WRITE_LOCATION = r''

# CREATE_TABLE_REGEX = ''
# FIND_TABLE_NAME_REGEX = ''


def main():
    create_table_regex = regex.compile(
        r'CREATE (?!EXTERNAL).*TABLE\s(IF NOT EXISTS)?(?:\w|\s|\.|\n|\(|,|(?<=\d)\)|-|\+|\[|\]|\"|(?<=\w)\))+\)'
    )

    with open(TXT_FILE_LOCATION, 'r') as f:
        buffer = ''
        for line in f:
            buffer += line
            while ';' in buffer:
                statement, buffer = buffer.split(';', 1)

                # Process the statement here
                table_ddl_search = regex.search(create_table_regex, statement)
                if table_ddl_search:
                    table_ddl = quote_swap(table_ddl_search.group())
                    schema_name, table_name = extract_table_header_from_statement(table_ddl)
                    print(schema_name, table_name, table_ddl)
                    write_ddl_to_file(schema_name, table_name, table_ddl)
                else:
                    continue


def extract_table_header_from_statement(ddl_statement: str) -> tuple:
    find_table_name_regex = regex.compile(r'(?<=CREATE.*TABLE\s(IF NOT EXISTS)?).*(\.)?.*(?=\(\s?)', re.IGNORECASE)
    schema_table_name_search = regex.search(find_table_name_regex, ddl_statement)

    if schema_table_name_search:
        schema_table_name = schema_table_name_search.group()
        schema_table_name_split = schema_table_name.split('.')
        try:
            schema_name = schema_table_name_split[0]
            table_name = schema_table_name_split[1]
            return schema_name, table_name
        except IndexError:
            table_name = schema_table_name_split[0]
            return None, table_name
    else:
        return None, None


def write_ddl_to_file(schema_name: str, table_name: str, ddl_statement: str):
    file_body = '{{% set table_metadata = {{ \n\t ' \
                '"table_definition":" \n\t\t' \
                '{} \n\t' \
                '"\n' \
                '}}%}} \n\n' \
                '{{{{ config(materialized = "ephemeral", tags = "crt_model") }}}}\n' \
                '{{% do run_query(table_metadata.table_definition) %}}'.format(ddl_statement)

    if schema_name:
        file_name = f'crt__{schema_name}__{table_name.strip()}.sql'
    else:
        file_name = f'crt__{table_name.strip()}.sql'

    print(f'Writing {file_name}')
    os.chdir(WRITE_LOCATION)
    file = open(file_name, 'w')
    file.write(file_body)
    file.close()
    print(f'Finished writing {file_name} \n')


def quote_swap(string: str, swap_out='double') -> str:
    if swap_out == 'double':
        return string.replace('"', "'")
    elif swap_out == 'single':
        return string.replace("'", '"')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                    prog='Data Mart Dumper',
                    description='''This program takes in a formatted EON extract of SBD\'s Redshift Table DDLs and generates crt_ models that can be placed
                                in the dbt project. The purpose of crt_ models is to simply create the tables in the warehouse so that they exist when
                                converting the Redshift stored procedures.''',
                    epilog='ADEPT utilities')
    main()
