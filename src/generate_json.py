import json
import argparse
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
            # name, modifiable, data_type, _ = line.split(',')
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
            # print(line)
            try:
                key, value = line.split('=')
                if not key in dict_aws_params:
                    print(f"Ignoring line {line} because it is not exsit in aws params")
                    continue
                
                if dict_aws_params[key]["modifiable"] == "FALSE":
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
                
                parameters.append({"ParameterName": key, "ParameterValue": value, "ApplyMethod": "pending-reboot"})
            except ValueError:
                print(f"Ignoring line {line} because it is not in the correct format")
    return parameters

def generate_json(name, desc, file_name):
    parameters = read_file(file_name)
    data = {"Parameters": parameters}
    data["DBParameterGroupName"] = name
    # data["Description"] = desc
    output_file = f'{os.path.dirname(os.path.dirname(os.path.realpath(__file__)))}/output/{name}-{file_name}.json'
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)

parser = argparse.ArgumentParser(description='need --name, --desc, --file_name')
parser.add_argument('--name', '-n', help='name')
parser.add_argument('--desc', '-d', help='desc')
parser.add_argument('--file_name', '-f', help='file_name')
args = parser.parse_args()

if __name__ == '__main__':
    print(f'name: {args.name}')
    print(f'desc: {args.desc}')
    print(f'file_name: {args.file_name}')

    name = args.name
    desc = args.desc
    file_name = args.file_name
    generate_json(name, desc, file_name)
