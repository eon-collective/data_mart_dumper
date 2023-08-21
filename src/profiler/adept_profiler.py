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
            data['profiled_file_name'] = f.stem
            dfs.append(data)

        print (args.output_dir)
        df = pandas.concat(dfs, ignore_index=True)
        prof = ProfileReport(df,
            config_file=args.conf_file)
        object_directory_isExist = os.path.exists(args.output_dir+'/'+args.job_name+'/reports')
        if not object_directory_isExist:
            # Create a new directory because it does not exist
            os.makedirs(args.output_dir+'/'+args.job_name+'/reports/')
            print("The new directory is created! "+ args.output_dir+'/'+args.job_name+'/reports/')
        prof.to_file(output_file=args.output_dir+'/'+args.job_name+'/reports/'+args.report_name)
    except:
        print ("something went wrong in profile_adept_results during profile for a folder")
        raise

def profile_adept_from_mixedfolder(args):
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
            # data = pandas.read_csv(f,
            #                     sep = ',', 
            #                     engine='python')
            # data = pandas.read_fwf(f)
            # .stem is method for pathlib objects to get the filename w/o the extension
            # data['profiled_file_name'] = f.stem
            # dfs.append(data)
            print(f.stem)
            profile_adept_from_file(dir_input_path+"/"+f.stem+".csv", args.output_dir, args.job_name, f.stem+".html", args.delimiter)
    except:
        print ("something went wrong in profile_adept_results during profile for a folder")
        raise

def profile_adept_from_file(input_file, output_dir, job_name, report_name, conf_file, delimiter=','):
    """
    profile_adept_results from a single file

    """
    try:
        stats_input_path = input_file
        print ("profiling " + stats_input_path)
        df = pandas.read_csv(stats_input_path,
                                sep = delimiter,
                                engine='python')
            
        df['profiled_file_name'] = Path(input_file).name
        prof = ProfileReport(df,
            config_file=conf_file)
        object_directory_isExist = os.path.exists(output_dir+'/'+job_name+'/reports')
        if not object_directory_isExist:
            # Create a new directory because it does not exist
            os.makedirs(output_dir+'/'+job_name+'/reports/')
            print("The new directory is created! "+ output_dir+'/'+job_name+'/reports/')
        prof.to_file(output_file=output_dir+'/'+job_name+'/reports/'+report_name)
        print ("Writing profile report to "+ output_dir+'/'+job_name+'/reports/'+report_name)
    except:
        print ("something went wrong in profile_adept_results during profiling of a file")
        raise

def main(parser):
    """
    main - Driver program
    
    """
    try:
        args = parser.parse_args()
        if args.mode.upper() == "FILE":
            profile_adept_from_file(args.input_file, args.output_dir, args.job_name, args.report_name, args.conf_file, args.delimiter)
        elif args.mode.upper() == "FOLDER":
            profile_adept_from_folder(args)
        elif args.mode.upper() == "MIXEDFOLDER":
            profile_adept_from_mixedfolder(args)
    except:
        print ("something went wrong in calling main driver for the program")
        raise

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
    prog='adept_profiler',
    description='''This program is used to profile a file or folder and provide a .html report''',
    epilog='ADEPT utilities')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    parser.add_argument("-i", "--input-file", required=False, help="input txt", default="")
    parser.add_argument("-f", "--input-dir", required=False, help="input dir", default="")
    parser.add_argument("-d", "--delimiter", required=False, help="delimiter for input file", type=ascii)
    parser.add_argument("-o", "--output-dir", required=False, help="job baseoutput directory", default="")
    parser.add_argument("-c", "--conf-file", required=False, help="Profiling configuration file", default="profiling.yml")
    parser.add_argument("-r", "--report-name", required=False, help="profiling report name", default="adept_report.html")
    parser.add_argument("-m", "--mode", required=False, help="choose mode to run this jobs as: can be file or folder", choices=['file','folder', 'mixedfolder', 'FILE', 'FOLDER', 'MIXEDFOLDER'], default="FILE")
    parser.add_argument("-j", "--job-name", required=False, help="adept job name", default="adept_profiler")
    main(parser)
