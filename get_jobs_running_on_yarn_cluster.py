import requests
import sys
list_of_running_applications=[]
list_of_running_application_ids=[]
list_of_tracking_url=[]
list_of_job_names=[]
dict_of_names_and_ids={}
RESOURCE_MANAGER_URL='<yarn resource manager URL>'

def get_job_id(response):
    running_jobs_list=response['jobs']
    for i in running_jobs_list:
        if i.get('status') in ('RUNNING'):
            return i.get('id')
def get_job_name(job_name_response):
    return job_name_response.get('name')
def get_dict_of_job_names_and_app_ids(list_of_running_application_ids,list_of_tracking_url):
    for i,v in zip(list_of_running_application_ids,list_of_tracking_url):
        b =requests.get(f'{v}/jobs/')
        job_id=get_job_id(b.json())
        job_name_response=requests.get(f'{v}/jobs/{job_id}')
        job_name=get_job_name(job_name_response.json())
        if i not in dict_of_names_and_ids.keys():
            dict_of_names_and_ids[i]=job_name
    return dict_of_names_and_ids
def main_function(job_name):
    r =requests.get(f'http://{RESOURCE_MANAGER_URL}/ws/v1/cluster/apps/')
    list_of_applications=(r.json())['apps']['app']
    for i,v in enumerate (list_of_applications):
        if list_of_applications[i]['id'] not in list_of_running_application_ids and list_of_applications[i]['state'] in ('RUNNING') :
            list_of_running_application_ids.append(list_of_applications[i]['id'])
            list_of_tracking_url.append(list_of_applications[i]['trackingUrl'])
    output_dict=get_dict_of_job_names_and_app_ids(list_of_running_application_ids,list_of_tracking_url)
    for key,value in output_dict.items():
        if value==job_name:
            return key

if __name__ == '__main__':
    try:
        output=main_function(sys.argv[1])
        if (output):
            sys.stdout.write(str(output))
    except:
        sys.exit('Error occured in script, Exiting')