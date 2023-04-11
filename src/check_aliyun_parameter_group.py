#!/usr/bin/python3
import json
import os
import argparse

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
            # name, modifiable, data_type, _ = line.split(',')
            dict_params[name] = {"modifiable": modifiable, "data_type": data_type}
    return dict_params

def check_param(file_name):
    # load aws default params
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
                    print(f"{line} : not exsit in aws params")
                    continue
                
                if dict_aws_params[key]["modifiable"] == "FALSE":
                    print(f"{line} : can't be modified")
                    continue
                
                if dict_aws_params[key]["data_type"] == "string":
                    continue

                if dict_aws_params[key]["data_type"] == "integer":
                    if not value.isnumeric():
                        print(f"{line} : has invalid format(should be integer)")
                        continue
                elif dict_aws_params[key]["data_type"] == "boolean":
                    if value in ["ON", "OFF", "1", "0"]:
                        continue
                    else:
                        print(f"{line} : has invalid formate(should be ON/OFF/1/0)")
            except ValueError:
                print(f"Ignoring line {line} because it is not in the correct format")

parser = argparse.ArgumentParser(description='--file_name')
parser.add_argument('--file_name', '-f', help='file_name')
args = parser.parse_args()

if __name__ == '__main__':
    print(f'file_name: {args.file_name}')
    print("------")
    file_name = args.file_name
    check_param(file_name)
