import json
import os
import sys
FLINK_PROCESSORS='flink-processors'
LEVEL_1_LENGTH=1

def print_name(modifiedfiles):
    '''
    Gets the names of the modified files from bash
    '''
    delimited_file_paths=modifiedfiles.split('\n')
    return delimited_file_paths
def parse_map():
    '''
    Parses the json map
    '''
    here = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(here, 'processor_map.json')
    with open(filename) as filereader:
        data=json.load(filereader)
    return data
def compare_files(files):
    '''
    Maps the file names obtained from bash to ecr tags
    '''
    json_map=parse_map()
    list_of_file_names=[]
    for file_name in files:
        file_name_parts=file_name.split('/')
        if file_name_parts[0] == FLINK_PROCESSORS and len(file_name_parts)>LEVEL_1_LENGTH:
            if file_name_parts[LEVEL_1_LENGTH] in json_map.keys() and file_name_parts[LEVEL_1_LENGTH] not in list_of_file_names:
                list_of_file_names.append(file_name_parts[LEVEL_1_LENGTH])

    project_files = ",".join(list_of_file_names)
    if list_of_file_names:
        sys.stdout.write(project_files)


if __name__ == '__main__':
    try:
        file_list=print_name(sys.argv[1])
        compare_files(file_list)
    except:
        sys.exit('Error occured in script, Exiting')