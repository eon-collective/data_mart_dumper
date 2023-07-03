import os
import argparse
import uuid
import re
import pandas
from ydata_profiling import ProfileReport
from pathlib import Path

def profile_adept_from_folder(args):
    """
    profile_adept_results from a folder
    """
    #os.system('pwd')
    #os.system('ls -l')
    try:
        dir_input_path = args.input_dir
        ddl_files = Path(dir_input_path).glob('*.csv')
        dfs = list()
        for f in ddl_files:
            # print("Checking out "+ str(f))
            data = pandas.read_csv(f,
                                sep = ',', 
                                engine='python')
            # data = pandas.read_fwf(f)
            # .stem is method for pathlib objects to get the filename w/o the extension
            data['file'] = f.stem
            dfs.append(data)

        print (args.output_dir)
        df = pandas.concat(dfs, ignore_index=True)
        prof = ProfileReport(df,
            config_file=args.conf_file)
        prof.to_file(output_file=args.output_dir+'/'+args.report_name)
    except:
        print ("something went wrong in profile_adept_results")
        raise

def profile_adept_from_file(args):
    """
    profile_adept_results from a single file

    """
    try:
        stats_input_path = args.input_file
        print (stats_input_path)
        df = pandas.read_csv(stats_input_path,
                                sep = args.delimiter,
                                engine='python')
            
        prof = ProfileReport(df,
            config_file=args.conf_file)
        prof.to_file(output_file=args.output_dir+'/'+args.report_name)
        print ("Writing profile report to "+ args.output_dir+'/'+args.report_name)
    except:
        print ("something went wrong in profile_adept_results")
        raise

def main(parser):
    """
    main - Driver program
    
    """
    try:
        args = parser.parse_args()
        if args.mode.upper() == "FILE":
            profile_adept_from_file(args)
        elif args.mode.upper() == "FOLDER":
            profile_adept_from_folder(args)
    except:
        print ("something went wrong in calling main driver for the program")
        raise

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
    prog='adept_profiler',
    description='''This program takes in a pg_dump generated DDLs and generates individual 
            .sql files partitioned by object type: TABLES, VIEWS etc.''',
    epilog='ADEPT utilities')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    parser.add_argument("-i", "--input-file", required=False, help="input txt", default="")
    parser.add_argument("-f", "--input-dir", required=False, help="input dir", default="")
    parser.add_argument("-d", "--delimiter", required=False, help="delimiter for input file", type=ascii)
    parser.add_argument("-o", "--output-dir", required=False, help="output directory", default="")
    parser.add_argument("-c", "--conf-file", required=False, help="Profiling configuration file", default="profiling.yml")
    parser.add_argument("-r", "--report-name", required=False, help="profiling report name", default="report.html")
    parser.add_argument("-m", "--mode", required=False, help="choose mode to run this jobs as: can be file or folder", choices=['file','folder', 'FILE', 'FOLDER'], default="FILE")

    main(parser)
