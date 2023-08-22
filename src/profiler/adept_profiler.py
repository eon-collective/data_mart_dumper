import os
import argparse
import uuid
import re
import pandas
from ydata_profiling import ProfileReport
from pathlib import Path
import hashlib
from datetime import datetime

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
            # .stem is method for pathlib objects to get the input_file w/o the extension
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
            # .stem is method for pathlib objects to get the input_file w/o the extension
            # data['profiled_file_name'] = f.stem
            # dfs.append(data)
            print(f.stem)
            profile_adept_from_file(dir_input_path+"/"+f.stem+".csv", args.output_dir, args.job_name, f.stem+".html", args.delimiter)
    except:
        print ("something went wrong in profile_adept_results during profile for a folder")
        raise

def generate_adept_graph_data(input_file, output_dir, job_name, df):
    file_name =  Path(input_file).name
    file_extension = file_name.split(".")[1]

    # check if graph data directory for nodes exists, if not create it
    gd_nodes_directory=output_dir+'/'+job_name+'/graph_data/nodes'
    gd_nodes_directory_isExist = os.path.exists(gd_nodes_directory)
    if not gd_nodes_directory_isExist:
        # Create a new directory because it does not exist for /graph_data/nodes
        os.makedirs(gd_nodes_directory+"/")
        print("The new directory is created! "+ gd_nodes_directory)

    # check if graph data directory for nodes exists, if not create it
    gd_relationships_directory=output_dir+'/'+job_name+'/graph_data/relationships'
    gd_relationships_directory_isExist = os.path.exists(gd_relationships_directory)
    if not gd_relationships_directory_isExist:
        # Create a new directory because it does not exist for /graph_data/relationships
        os.makedirs(gd_relationships_directory+"/")
        print("The new directory is created! "+ gd_relationships_directory)

    file_node_path = gd_nodes_directory+"/profile_file.csv"
    is_NodeFile_Existing = os.path.exists(file_node_path) 
    if is_NodeFile_Existing == False:
            BaseNodeFile = open(file_node_path, "a")
            # Schema => Entity_ID:ID,:Label,HashKey,name, Technical Data Type,
            file_column_header_line = ["Entity_ID:ID,:Label,HashKey,name,Path,Extension,Size,Last_Modified_Time,Creation_Time\n"]
            BaseNodeFile.writelines(file_column_header_line)
            file_column_line = ["%s,%s,%s,%s,%s,%s,%s bytes,%s,%s\n"%(hashlib.md5((input_file).encode()).hexdigest(),"File",hashlib.md5((input_file).encode()).hexdigest(),file_name,input_file,file_extension,os.path.getsize(input_file),os.path.getctime(input_file),os.path.getmtime(input_file))]
            BaseNodeFile.writelines(file_column_line)
            BaseNodeFile.close()
    else:
        BaseNodeFile = open(file_node_path, "a")
        # Schema => Entity_ID:ID,:Label,HashKey,name,Path,Extension,Size,Creation_Time,Last_Modified_Time
        file_column_line = ["%s,%s,%s,%s,%s,%s,%s bytes,%s,%s\n"%(hashlib.md5((input_file).encode()).hexdigest(),"File",hashlib.md5((input_file).encode()).hexdigest(),file_name,input_file,file_extension,os.path.getsize(input_file),os.path.getctime(input_file),os.path.getmtime(input_file))]
        BaseNodeFile.writelines(file_column_line)
        BaseNodeFile.close()
            
    filecolumn_node_path = gd_nodes_directory+"/profile_file_columns.csv"
    is_NodeFile_Existing = os.path.exists(filecolumn_node_path) 
    if is_NodeFile_Existing == False:
        BaseNodeFile = open(filecolumn_node_path, "a")
        # Schema => Entity_ID:ID,:Label,HashKey,name, Technical Data Type,
        file_column_line = ["Entity_ID:ID,:Label,HashKey,name,Technical_Data_Type,Source_Name\n"]
        BaseNodeFile.writelines(file_column_line)
        BaseNodeFile.close()       
    
    file_relationship_path = gd_relationships_directory + "/profile_relationships.csv"
    is_RelationshipFile_Existing = os.path.exists(file_relationship_path)
    if is_RelationshipFile_Existing == False:
        BaseRelationshipFile = open(file_relationship_path, "a")
        # Schema => Entity_ID:ID,:Label,HashKey,name, Technical Data Type,
        file_column_relationship_line = [":START_ID,:END_ID,:TYPE,timestamp,Version\n"]
        BaseRelationshipFile.writelines(file_column_relationship_line)
        BaseRelationshipFile.close()     

    for colname, coltype in df.infer_objects().dtypes.items():       
        print(colname, coltype)
        NodeFileColumn = open(filecolumn_node_path, "a")
        # Schema => Entity_ID:ID,:Label,HashKey,name, Technical Data Type,
        Entity_ID = hashlib.md5((input_file+"~"+str(colname)).encode()).hexdigest()
        Label = "Column"
        HashKey = Entity_ID
        name = str(colname)
        Technical_Data_Type = str(coltype)
        Source = input_file
        file_column_line = [Entity_ID + "," + Label + "," + HashKey + "," + name + "," + Technical_Data_Type + "," + Source + "\n"]
        NodeFileColumn.writelines(file_column_line)
        NodeFileColumn.close()
            
        RelationshipFile = open(file_relationship_path, "a")
        # Schema => :START_ID,:END_ID,:TYPE,timestamp,Version
        START_ID = hashlib.md5((input_file).encode()).hexdigest()
        END_ID = hashlib.md5((input_file+"~"+str(colname)).encode()).hexdigest()
        TYPE = "contains_columns"
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        Version = "1"
        file_column_relationship_line = [START_ID + "," + END_ID + "," + TYPE + "," + timestamp + "," + Version + "\n"]
        RelationshipFile.writelines(file_column_relationship_line)
        RelationshipFile.close()


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
        file_name =  Path(input_file).name  
        df['profiled_file_name'] = file_name
        prof = ProfileReport(df,
            config_file=conf_file)
        object_directory_isExist = os.path.exists(output_dir+'/'+job_name+'/reports')
        if not object_directory_isExist:
            # Create a new directory because it does not exist
            os.makedirs(output_dir+'/'+job_name+'/reports/')
            print("The new directory is created! "+ output_dir+'/'+job_name+'/reports/')
        prof.to_file(output_file=output_dir+'/'+job_name+'/reports/'+report_name)
        print ("Writing profile report to "+ output_dir+'/'+job_name+'/reports/'+report_name)
        #  generate graph_data for ADEPT
        generate_adept_graph_data(input_file, output_dir, job_name, df)

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
    parser.add_argument('--version', action='version', version='%(prog)s 2.01')
    parser.add_argument("-i", "--input-file", required=False, help="input txt", default="")
    parser.add_argument("-f", "--input-dir", required=False, help="input dir", default="")
    parser.add_argument("-d", "--delimiter", required=False, help="delimiter for input file", type=ascii)
    parser.add_argument("-o", "--output-dir", required=False, help="job baseoutput directory", default="")
    parser.add_argument("-c", "--conf-file", required=False, help="Profiling configuration file", default="profiling.yml")
    parser.add_argument("-r", "--report-name", required=False, help="profiling report name", default="adept_report.html")
    parser.add_argument("-m", "--mode", required=False, help="choose mode to run this jobs as: can be file or folder", choices=['file','folder', 'mixedfolder', 'FILE', 'FOLDER', 'MIXEDFOLDER'], default="FILE")
    parser.add_argument("-j", "--job-name", required=False, help="adept job name", default="adept_profiler")
    main(parser)
