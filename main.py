import json

def load_aws_rds_mysql_param_group():
    with open("rds-mysql5.7-param-group.csv", 'r') as f:
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
                
                parameters.append({"ParameterName": key, "ParameterValue": value, "ApplyMethod": "immediate"})
            except ValueError:
                print(f"Ignoring line {line} because it is not in the correct format")
    return parameters

def generate_json(name, desc, file_name):
    parameters = read_file(file_name)
    data = {"Parameters": parameters}
    data["Name"] = name
    data["Description"] = desc
    with open('output.json', 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == '__main__':
    name = "example"
    desc = "This is an example"
    file_name = "rds_param.txt"
    generate_json(name, desc, file_name)
