import os
import argparse
import uuid
import re
import pandas
from ydata_profiling import ProfileReport

# delimiter = '-- Name: '

output_path=''

def split_file_from_pg_dump(args):
    counter = 1
    output_filename = 'part-'+str(counter)
    section = 'audit'

    """
    split_file_from_pg_dump - Split File From pg_dump File
    
    """
    try:
        stats_output_dir = os.path.join(args.output_dir, 'audit')
        stats_output_path = os.path.join(stats_output_dir, 'catalog.csv')
        ## check if file exists
        catalogFile_isExist = os.path.exists(stats_output_path)
        if not catalogFile_isExist:
            os.makedirs(stats_output_dir)
            print("The new directory is created for audit stats! ")
            with open(stats_output_path, 'a') as stats_output_file:
                stats_output_file.write("{0};{1};{2};{3}\n".format("Name", "Type", "Schema", "Owner"))

        with open(args.input_file, 'r') as input_file:
            for line in input_file.read().split('\n'):
                if args.split_delimiter in line:
                    counter = counter+1
                    # -- Name: TABLE ada_phone_agg_touch_fct; Type: ACL; Schema: mkt_rdl; Owner: sys_object_owner
                    file_parts = line.removeprefix('-- ').split('; ')
                    object_name_preClean = file_parts[0].removeprefix('Name: ').split('(')[0]
                    object_name = re.sub(r'\W+', '___', object_name_preClean)
                    object_type = file_parts[1].removeprefix('Type: ')
                    section = object_type
                    object_schema = file_parts[2].removeprefix('Schema: ')
                    object_owner= file_parts[3].removeprefix('Owner: ')

                    # output_filename = 'gp-part-'+str(counter)
                    output_filename = object_schema+"-"+object_name+"-"+object_owner
                    output_path = os.path.join(args.output_dir+section, output_filename+'.sql')
                    object_directory_isExist = os.path.exists(args.output_dir+section)
                    if not object_directory_isExist:
                        # Create a new directory because it does not exist
                        os.makedirs(args.output_dir+section)
                        print("The new directory is created! "+ args.output_dir+section)
                    with open(output_path, 'a') as output_file:
                        output_file.write("{0}\n".format(line))

                    stats_output_path = os.path.join(args.output_dir, 'catalog.csv')
                    with open(stats_output_path, 'a') as stats_output_file:
                        cleanLine = line.replace("-- Name: ","").replace(" Type: ","").replace(" Schema: ","").replace(" Owner: ","").replace("; Tablespace: ","")
                        stats_output_file.write("{0}\n".format(cleanLine))
                    print(section + ' Section '+str(counter)+' started and write to file '+ output_filename)
                else:
                    #skips empty lines (change the condition if you want empty lines too)
                    if line.strip() :
                        output_path = os.path.join(args.output_dir+section, output_filename+'.sql')
                        isExist = os.path.exists(args.output_dir+section)
                        if not isExist:
                            # Create a new directory because it does not exist
                            os.makedirs(args.output_dir+section)
                            print("The new directory is created! "+ args.output_dir+section)
                        with open(output_path, 'a') as output_file:
                            output_file.write("{0}\n".format(line))
    except:
        print ("something went wrong in split_file_from_pg_dump")
        raise

def profile_adept_results(args):
    """
    profile_adept_results

    """
    try:
        stats_output_path = args.output_dir +'/catalog.csv'
        print (stats_output_path)
        df = pandas.read_csv(stats_output_path,
                                sep = ';',
                                engine='python')
        prof = ProfileReport(df,
            config_file=args.conf_file)
        prof.to_file(output_file=args.output_dir+'/report.html')
    except:
        print ("something went wrong in profile_adept_results")
        raise

def main(parser):
    """
    main - Driver program
    
    """
    try:
        args = parser.parse_args()
        split_file_from_pg_dump(args)
        profile_adept_results(args)
    except:
        print ("something went wrong in calling main driver for the program")
        raise

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
    prog='pg_dump Splitter',
    description='''This program takes in a pg_dump generated DDLs and generates individual 
            .sql files partitioned by object type: TABLES, VIEWS etc.''',
    epilog='ADEPT utilities')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    parser.add_argument("-i", "--input-file", required=False, help="input txt", default="/Users/james.kimani/Development/repositories/greenplum-oss-docker/usecase2/data/gp_ns_ddl_test-schema-eon-assessment.sql")
    parser.add_argument("-o", "--output-dir", required=False, help="output directory", default="/Users/james.kimani/Development/repositories/greenplum-oss-docker/usecase2/data/splits/")
    parser.add_argument("-c", "--conf-file", required=False, help="Profiling configuration file", default="profiling.yml")
    parser.add_argument("-s", "--split-delimiter", required=False, help="pg_dump file split delimiter", default="-- Name: ")
    main(parser)
