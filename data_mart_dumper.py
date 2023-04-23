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

WRITE_LOCATION = os.getcwd()
TXT_FILE_LOCATION = ''

# Change this to where you want the files to be dumped, otherise they will be dumped in the current working directory
WRITE_LOCATION = r''

def main() -> None:
    """ Generates a collection of crt_<table_name>.sql files that can be executed in the dbt project"""

    # Read the contents of the file.
    with open(TXT_FILE_LOCATION, "r") as f:
        ddl_statements = f.read()
        assert ddl_statements, "File has no contents"

    print('formatting file contents...')
    # Format the contents of the file
    ddl_statements = re.sub(r'--.*', '', ddl_statements)    # Comment Remover
    ddl_statements = re.sub(r'ENCODE (lzo|az64|raw|bytedict|delta|delta32K|mostly8|mostly16|mostly32|runlength|text255|text32K|zstd)',
                            '', ddl_statements, flags=re.IGNORECASE)  # Redshift Encode Replacement
    ddl_statements = re.sub(r'DISTSTYLE (\w|\t|\n|\(|\)| |\.)*;', '', ddl_statements) # DISTTYLE Replacement
    ddl_statements = re.sub(r'ALTER TABLE (\w|\t|\n|\(|\)|\s|,|\.)*;', '', ddl_statements) # ALTER TABLE Replacement

    # Extract the CREATE TABLE IF NOT EXISTS <table_name> or CREATE TABLE <table_name>
    create_table_statements = re.findall(r"CREATE TABLE (?:\w|\d|\.| )*", ddl_statements)

    print('extracting table names and table definitions...')
    # Extract the compete CREATE TABLE [IF NOT EXISTS] <table_name> (<table definition>)
    complete_extract = re.findall(r'CREATE TABLE (?:\w|\s|\.|\n|\(|,|(?<=\d)\)|\"|(?<=\w)\))+\)', ddl_statements)
    complete_extract = [table_ddl.replace('"', '') for table_ddl in complete_extract]   # Remove quotes around column names
    complete_extract = [table_ddl.replace('CREATE TABLE', 'CREATE TABLE IF NOT EXISTS')
                        if 'IF NOT EXISTS' not in table_ddl else table_ddl
                        for table_ddl in complete_extract]  # All crt models should use CREATE TABLE IF NOT EXISTS

    identity_pattern = ('identity', re.compile(re.escape('default identity'), re.IGNORECASE))   # Swap default identity for identity
    getdate_pattern = ('current_date', re.compile(re.escape('getdate'), re.IGNORECASE))    # Swap getdate for current_date
    for replace_tuple in [identity_pattern, getdate_pattern]:
        complete_extract = [replace_tuple[1].sub(replace_tuple[0], table_ddl) for table_ddl in complete_extract]



    print('writing files...')
    # Extract the <table_name> without the source system prefix.
    table_group = [table.split('CREATE TABLE ') for table in create_table_statements]
    table_names = [table_name[1] for table_name in table_group]
    table_names = [table_name.replace('.', '__').replace('IF NOT EXISTS ', '') for table_name in table_names]
    assert len(complete_extract) == len(table_names), "Lists are not the same length"


    # Use the extracts to format the file contents and write to the file.
    for table_ddl, table_name in zip(complete_extract, table_names):
        file_body = '{{% set table_metadata = {{ \n\t ' \
                    '"table_definition":" \n\t\t' \
                    '{} \n\t' \
                    '"\n' \
                    '}}%}} \n\n' \
                    '{{{{ config(materialized = "ephemeral", tags = "crt_model") }}}}\n' \
                    '{{% do run_query(table_metadata.table_definition) %}}'.format(table_ddl)

        os.chdir(WRITE_LOCATION)
        file = open(f'crt_{table_name.strip()}.sql', 'w')
        file.write(file_body)
        file.close()

    return


if __name__ == '__main__':
    main()
    # CREATE\s+TABLE\s+(\w+)\s*\((?:\s*[^),]+(?:\([^)]+\))?)*\s*\);
