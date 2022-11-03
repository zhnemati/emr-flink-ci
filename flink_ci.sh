#!/bin/bash
set -euxo pipefail
git checkout develop
git pull origin develop
declare modifiedfiles=$(git diff --name-only HEAD^1) 
script_output=$(python3 get_job_names.py "$modifiedfiles" 2>&1)
if [ -z "${script_output}" ];
then
echo "No file existing in the flink processors repository has been modified. Exiting"
exit 0
else 
IFS=',' read -r -a array_of_project_names <<< "$script_output"
length_of_project_list=${#array_of_project_names[@]}
echo "$length_of_project_list"
for (( i=0; i<$length_of_project_list; i++ )); 
do 
    cd "${array_of_project_names[$i]}"
    mvn clean package
    rc=$?
    if [ $rc -ne 0 ] ; then
    echo "Maven compilation failed"
    cd ..
    exit $rc
    else
    cd "${array_of_project_names[$i]}-jars"
    aws s3 cp ${array_of_project_names[$i]}.jar s3://flink-jars-emr/${array_of_project_names[$i]}/${array_of_project_names[$i]}.jar
    application_id=$(python3 get_running_jobs_on_yarn_cluster.py "$array_of_project_names[$i]" 2>&1)
    aws emr add-steps --cluster-id j-XXXXXXXXX --steps Type=CUSTOM_JAR,Name="$array_of_project_names[$i]",Jar=command-runner.jar,Args="bash","-c"," yarn application -kill "$application_id" && sudo aws s3 cp s3://flink-jars-emr/${array_of_project_names[$i]}/${array_of_project_names[$i]}.jar  /flink-jars/ --region me-south-1 && /usr/lib/flink/bin/flink run-application -t yarn-application /flink-jars/${array_of_project_names[$i]}.jar"
    cd ../..
    fi
done
fi