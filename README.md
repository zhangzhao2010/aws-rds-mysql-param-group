# aws-rds-mysql-param-group
create rds mysql param group with a file

# PrePrerequisites
https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html

# How to use
```
# create db param group
python3 src/create_db_parameter_group.py -n <name> -f <family> -d <desc>

# demo
python3 src/create_db_parameter_group.py -n my-param-group -f mysql5.7 -d "my param group"
```
```
# check aliyun param group
python3 src/check_aliyun_parameter_group.py -f <aliyun_param_file_name>

# demo
python3 src/check_aliyun_parameter_group.py -f rds_param.txt

```
```
# update db param group
python3 src/update_db_parameter_group.py -n <param_goup_name> -f <aliyun_param_file_name>

# demo
python3 src/update_db_parameter_group.py -n t1 -f rds_param_sub.txt
```