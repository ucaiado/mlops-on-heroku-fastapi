#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
'Infrastructure as Code'


@author: udacity, ucaiado

Created on 07/07/2020
"""

# import libraries
import argparse
import textwrap
import boto3
import json
import os
import glob
import tqdm
import configparser
import subprocess
import pathlib
import pandas as pd
from rich.console import Console
from rich.table import Column, Table
from rich.progress import track


'''
Begin help functions and variables
'''


def prettyEMRProps(props):
    l_data = [('Id', props['Id']),
              ('Name', props['Name']),
              ('State', props['Status']['State'])]

    console = Console()

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Key", style="dim", width=12)
    table.add_column("Value", justify="right")
    for row in l_data:
        table.add_row(
            *row
        )

    console.print(table)


def upload_files(s3, bucket_name, l_filepaths):
    # source: https://go.aws/3dvMlLb
    try:
        response = s3.list_buckets()
        l_buckets = [bucket['Name'] for bucket in response['Buckets']]
        if bucket_name not in l_buckets:
            d_bucket_conf = {'LocationConstraint': 'us-west-2'}
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration=d_bucket_conf)
            print(f'...create a new bucket with the name {bucket_name}')
        for s_filepath in track(l_filepaths):
            s_fname = s_filepath.split('/')[-1]
            s3.upload_file(s_filepath, bucket_name, s_fname)
    except Exception as e:
        print(e)
        return False
    return True


'''
End help functions and variables
'''


if __name__ == '__main__':
    s_txt = '''\
            Infrastructure as code
            --------------------------------
            Create Amazon IAM role in AWS to access S3
            '''
    # include and parse variables
    obj_formatter = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(
        formatter_class=obj_formatter, description=textwrap.dedent(s_txt))

    parser.add_argument(
        '-i',
        '--iam',
        action='store_true',
        help='Create IAM role'
    )

    parser.add_argument(
        '-b',
        '--bucket',
        action='store_true',
        help='Create a new bucket in S3'
    )

    parser.add_argument(
        '-d',
        '--dvc',
        action='store_true',
        help='Setup DVC to a bucket in S3'
    )

    parser.add_argument(
        '-hr',
        '--heroku',
        action='store_true',
        help='Setup AWS in Heroku'
    )

    # check what should do
    args = parser.parse_args()
    b_create_iam = args.iam
    b_create_bucket = args.bucket
    b_create_dvc = args.dvc
    b_create_heroku = args.heroku

    # check the step selected
    s_err = 'Please select one, and only one, option from -h menu'
    i_test_all = (b_create_iam*1 + b_create_bucket*1 + b_create_dvc*1 +
                  b_create_heroku*1)
    assert i_test_all == 1, s_err

    # define global variables
    s_path_conf = 'scripts/confs/project.cfg'
    config = configparser.ConfigParser()
    config.read_file(open(s_path_conf))

    KEY = config.get('AWS', 'ACCESS_KEY_ID')
    SECRET = config.get('AWS', 'SECRET_ACCESS_KEY')
    IAM_ROLE_ARN = config.get("IAM_ROLE",  "ARN")
    S3_IAM_ROLE_NAME = config.get("S3", "S3_IAM_ROLE_NAME")
    S3_BUCKET_NAME = config.get("S3", "S3_BUCKET_NAME")

    # create clients
    print('...create clients for S3 and IAM')
    s3 = boto3.client(
        's3',
        region_name='us-west-2',
        aws_access_key_id=KEY,
        aws_secret_access_key=SECRET)

    iam = boto3.client(
        'iam',
        region_name='us-west-2',
        aws_access_key_id=KEY,
        aws_secret_access_key=SECRET)

    if b_create_iam:
        # Create the IAM role
        try:
            dl_role = iam.create_role(
                Path='/',
                RoleName=S3_IAM_ROLE_NAME,
                Description=('Allow retrieving any object stored in the bucket'
                             'identified by the S3_BUCKET_NAME variable'),
                AssumeRolePolicyDocument=json.dumps(
                    {'Statement': [{
                        'Action': ['s3:GetObject'],
                        'Effect': 'Allow',
                        'Resource': f'arn:aws:s3:::{S3_BUCKET_NAME}/*',
                        'Principal': '*'}],
                     'Version': '2012-10-17'}
                ))
            print('...create a new IAM Role')
        except Exception as e:
            print(e)

        # Attaching Policy
        print('...attach AmazonS3FullAccess policy')
        iam.attach_role_policy(
            RoleName=S3_IAM_ROLE_NAME,
            PolicyArn="arn:aws:iam::aws:policy/AmazonS3FullAccess"
        )['ResponseMetadata']['HTTPStatusCode']

        # Get and print the IAM role ARN
        print('...get the IAM role ARN')
        role_arn = iam.get_role(RoleName=S3_IAM_ROLE_NAME)['Role']['Arn']
        print(f'   !! fill in the IAM_ROLE ARN field in {s_path_conf} file'
              ' with the following string:')
        print(role_arn)

    elif b_create_bucket:
        # Create a new bucket on S3
        try:
            s3_bucket = s3.create_bucket(
                Bucket=S3_BUCKET_NAME,
                CreateBucketConfiguration={
                    'LocationConstraint': 'us-west-2'
                    }
            )
            print(f'...create the bucket {S3_BUCKET_NAME} in S3')
        except Exception as e:
            print(e)

    elif b_create_dvc:
        # Create a new bucket on S3
        try:
            # create remotes
            s_cmd = f'dvc remote add -d s3remote s3://{S3_BUCKET_NAME}'
            subprocess.call(f'{s_cmd}', shell=True)
            subprocess.call(f'{s_cmd}/model', shell=True)
            subprocess.call(f'{s_cmd}/data', shell=True)
            # unset remote default so you always have to tell where to push
            subprocess.call(f'dvc remote default -u', shell=True)
            print(f'...setup DVC to {S3_BUCKET_NAME} S3 bucket')
        except Exception as e:
            print(e)


    elif b_create_heroku:
        # Set up Heroku to deploy a new App
        try:
            # setup aws credentials in heroku
            s_last_app = open('heroku_output.txt').read()
            s_last_app = s_last_app.split(' | ')[0]
            s_last_app = s_last_app.split('//')[1].split('.heroku')[0]
            s_cmd = f'heroku config:set AWS_ACCESS_KEY_ID={KEY} '
            s_cmd += f'AWS_SECRET_ACCESS_KEY={SECRET} --app={s_last_app}'
            subprocess.call(s_cmd, shell=True)
            print(f'...setup AWS creedentials in your Heroku account')

            # install buildpack in heroku
            s_cmd = f'heroku buildpacks:add --index 1 heroku-community/apt '
            s_cmd += f'--app={s_last_app};'
            subprocess.call(s_cmd, shell=True)
            print(f'...Install buildpack')

            # include new remote
            s_cmd = f'heroku git:remote -a {s_last_app}'
            subprocess.call(s_cmd, shell=True)
            print(f'...Include new remote')

        except Exception as e:
            print(e)
