#!/usr/bin/python3
import argparse
import boto3
import os

def load_aws_rds_mysql_param_group():
    with open(os.path.dirname(__file__) + "/rds-mysql5.7-param-group.csv", 'r') as f:
        lines = f.readlines()
    dict_params = {}
    for line in lines:
        line = line.strip()
        if line:
            tmp_list = line.split(',')
            name = tmp_list[0]
            modifiable = tmp_list[1]
            data_type = tmp_list[2]
            dict_params[name] = {"modifiable": modifiable, "data_type": data_type}
    return dict_params

def read_file(file_name):
    dict_aws_params = load_aws_rds_mysql_param_group()

    with open(file_name, 'r') as f:
        lines = f.readlines()
    parameters = []
    for line in lines:
        line = line.strip()
        if line:
            try:
                key, value = line.split('=')
                if not key in dict_aws_params:
                    print(f"Ignoring line {line} because it is not exsit in aws params")
                    continue
                
                if dict_aws_params[key]["modifiable"] == "false":
                    print(f"Ignoring line {line} because it can't be changed")
                    continue
                
                if dict_aws_params[key]["data_type"] == "string":
                    continue

                if dict_aws_params[key]["data_type"] == "integer":
                    if not value.isnumeric():
                        print(f"Ignoring line {line} because it has invalid format")
                        continue
                elif dict_aws_params[key]["data_type"] == "boolean":
                    if value == "ON":
                        value = "1"
                    elif value == "OFF":
                        value = "0"
                    elif value != "1" and value != "0":
                        print(f"Ignoring line {line} because it has invalid format")
                        continue
                
                parameters.append({"ParameterName": key, "ParameterValue": value, "ApplyMethod": "pending-reboot"})
            except ValueError:
                print(f"Ignoring line {line} because it is not in the correct format")
    return parameters

def list_split(items, n):
    return [items[i:i+n] for i in range(0, len(items), n)]

def update_param_group(name, file_name):
    result = read_file(file_name)
    tmp_list = list_split(result, 20)

    rds = boto3.client('rds')
    for l in tmp_list:
        response = rds.modify_db_parameter_group(
            DBParameterGroupName=name,
            Parameters=l
        )
        print(response)
        
parser = argparse.ArgumentParser(description='need --name, --file_name')
parser.add_argument('--name', '-n', help='name')
parser.add_argument('--file_name', '-f', help='file_name')
args = parser.parse_args()

if __name__ == '__main__':
    print(f"name: {args.name}")
    print(f"file_name: {args.file_name}")
    print("------")
    update_param_group(args.name, args.file_name)
