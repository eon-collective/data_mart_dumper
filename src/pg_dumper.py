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
import argparse
import regex

# WRITE_LOCATION = os.getcwd()
# TXT_FILE_LOCATION = ''

# # Change this to where you want the files to be dumped, otherise they will be dumped in the current working directory
# WRITE_LOCATION = r''

# CREATE_TABLE_REGEX = ''
# FIND_TABLE_NAME_REGEX = ''


def process_pg_dump_file(input_file_location, output_file_location):
    """Process pg_dump file by using regex patterns of objects

    Keyword arguments:
    input_file_location -- pg_dump file location used as input file 
    output_file_location -- Output folder location
    """
    create_table_regex = regex.compile(
        r'CREATE (?!EXTERNAL|TEMP).*TABLE\s(IF NOT EXISTS)?(?:\w|\s|\.|\n|\(|,|(?<=\d)\)|-|\+|\[|\]|\"|(?<=\w)\))+\)'
    )

    with open(input_file_location, 'r') as file_content:
        buffer = ''
        for line in file_content:
            buffer += line
            while ';' in buffer:
                statement, buffer = buffer.split(';', 1)

                # Process the statement here
                table_ddl_search = regex.search(create_table_regex, statement)
                if table_ddl_search:
                    table_ddl = quote_swap(table_ddl_search.group())
                    schema_name, table_name = extract_table_header_from_statement(table_ddl)
                    print(schema_name, table_name, table_ddl)
                    write_ddl_to_file(output_file_location,schema_name, table_name, table_ddl)
                else:
                    continue


def extract_table_header_from_statement(ddl_statement: str) -> tuple:
    """extract_table_header_from_statement

    Keyword arguments:
    ddl_statement -- ddl string to be parsed
    """
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


def write_ddl_to_file(output_file_location: str, schema_name: str, table_name: str, ddl_statement: str):
    """
    Write extracted DDL to a file in the provided output location

    Keyword arguments:
    output_file_location -- ddl string to be parsed
    schema_name -- schema name of parsed DDL
    table_name -- table name of parsed DDL
    ddl_statement -- DDL statement to be parsed
    """
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
    # os.chdir(WRITE_LOCATION)
    os.chdir(output_file_location)
    file = open(file_name, 'w')
    file.write(file_body)
    file.close()
    print(f'Finished writing {file_name} \n')


def quote_swap(string: str, swap_out='double') -> str:
    """quote swap
    Swap single for doungle and vice versa

    Keyword arguments:
    string -- string to be transformed
    swap_out -- quote type to be swapped
    
    """
    if swap_out == 'double':
        return string.replace('"', "'")
    if swap_out == 'single':
        return string.replace("'", '"')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                    prog='Data Mart Dumper',
                    description='''This program takes in a pg_dump generated DDLs and generates crt_ models that can be placed
                                in the dbt project. The purpose of crt_ models is to simply create the tables in the warehouse so that they exist when
                                converting the Redshift stored procedures.''',
                    epilog='ADEPT utilities')
    parser.add_argument('--input_file_name',
                    default='/Users/james.kimani/Development/repositories/greenplum-oss-docker/usecase2/data/gp_ns_ddl_test-schema-eon-assessment.sql',
                    help='Input location for the pg_dump file')
    parser.add_argument('--output_location',
                        default='/Users/james.kimani/Development/repositories/data_mart_dumper/out',
                        help='Output location of generated files')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')

    args = parser.parse_args()
    print("Provided pg_dump file: " + args.input_file_name)
    print("Provided output location: " + args.output_location)
    ## call the process_pg_dump_file with input and put locations from args
    process_pg_dump_file(args.input_file_name, args.output_location)
