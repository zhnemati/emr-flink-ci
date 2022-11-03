# EMR CI/CD for Flink Jobs
CI pipeline for flink on EMR. It can be integrated and triggered via jenkins and updates your .jar files and deploys application on EMR.
Assumption is that folder structure for Flink jobs is something like following : 
Root folder 
|
| - emr-flink-ci
| - data-projects
    | - flink-processors