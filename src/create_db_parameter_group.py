#!/usr/bin/python3
import boto3
import argparse

def create(db_parameter_group_name, db_parameter_group_family, description):
    rds = boto3.client('rds')
    response = rds.create_db_parameter_group(
        DBParameterGroupName=db_parameter_group_name,
        DBParameterGroupFamily=db_parameter_group_family,
        Description=description
    )
    return response


parser = argparse.ArgumentParser(description='need --name, --family, --desc')
parser.add_argument('--name', '-n', help='name')
parser.add_argument('--family', '-f', help='family')
parser.add_argument('--desc', '-d', help='desc')
args = parser.parse_args()

if __name__ == '__main__':
    print(f'name: {args.name}')
    print(f'file_name: {args.family}')
    print(f'desc: {args.desc}')
    print("------")
    response = create(args.name, args.family, args.desc)
    print(response)