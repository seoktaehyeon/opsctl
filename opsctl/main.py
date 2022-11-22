#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: v.stone@163.com
import json
from getopt import getopt, GetoptError
import sys
import os
from urllib.parse import urlparse

import yaml

from opsctl.render import Render as opsctlRender
from opsctl.bambooClient import Bamboo


def print_help_tool():
    print('\n'.join([
        '\nopsctl',
        '\t'.join([
            '  tmpl2art',
            'Render templates to articles'
        ]),
        '\t'.join([
            '  env2json',
            'Get environ variables to Json file'
        ]),
        '\t'.join([
            '  env2yaml',
            'Get environ variables to YAML file'
        ]),
        '\t'.join([
            '  bamboo',
            'Bamboo CLI'
        ]),
        '\t'.join([
            '  version',
            'Show opsctl version'
        ]),
    ]))
    exit(1)


def print_help_cmd_tmpl2art():
    print('\n'.join([
        '\nopsctl tmpl2art',
        '\t'.join([
            '  --config',
            'Key-Value config file path, file type is YAML'
        ]),
        '\t'.join([
            '  --tmpl',
            'Template dir path or template file path'
        ]),
        '\t'.join([
            '  --output',
            'Articles output path'
        ]),
    ]))
    exit(1)


def check_cmd_tmpl2art_opts(cmd_tmpl2art_opts):
    """
    config, template, output is required
    :param cmd_tmpl2art_opts:
    :return:
    """
    _items = dict()
    for k, v in cmd_tmpl2art_opts:
        _items['OPSCTL_%s' % k.replace('--', '').upper()] = v
    if len(_items) == 0:
        print_help_cmd_tmpl2art()
    if not _items.get('OPSCTL_CONFIG'):
        print('--config is required')
        print_help_cmd_tmpl2art()
    if not _items.get('OPSCTL_TMPL'):
        print('--tmpl is required')
        print_help_cmd_tmpl2art()
    if not _items.get('OPSCTL_OUTPUT'):
        print('--output is required')
        print_help_cmd_tmpl2art()
    if not os.path.isfile(_items['OPSCTL_CONFIG']):
        print('%s is not a valid file' % _items['OPSCTL_CONFIG'])
        print_help_cmd_tmpl2art()
    if os.path.isdir(_items['OPSCTL_TMPL']):
        if not os.path.isdir(_items['OPSCTL_OUTPUT']):
            print('%s is not a valid path' % _items['OPSCTL_OUTPUT'])
            print_help_cmd_tmpl2art()
    elif os.path.isfile(_items['OPSCTL_TMPL']):
        if os.path.isfile(_items['OPSCTL_OUTPUT']):
            print('%s is existing' % _items['OPSCTL_OUTPUT'])
            print_help_cmd_tmpl2art()
        elif os.path.isdir(_items['OPSCTL_OUTPUT']):
            _items['OPSCTL_OUTPUT'] = os.path.join(_items['OPSCTL_OUTPUT'], os.path.basename(_items['OPSCTL_TMPL']))
    else:
        print('%s is not a valid path' % _items['OPSCTL_TMPL'])
        print_help_cmd_tmpl2art()

    return _items


def print_help_cmd_env2json():
    print('\n'.join([
        '\nopsctl env2json',
        '\t'.join([
            '  --output',
            'Output Json file path'
        ]),
        '\t'.join([
            '  --input',
            'Optional. Ensure your input file format that is must be same with output of command "env".'
        ]),
        '\t'.join([
            '         ',
            'Get current os environ variables if let this option empty.'
        ]),
    ]))
    exit(1)


def check_cmd_env2json_opts(cmd_env2json_opts):
    """
    output is required
    :param cmd_env2json_opts:
    :return:
    """
    _items = dict()
    for k, v in cmd_env2json_opts:
        _items['OPSCTL_%s' % k.replace('--', '').upper()] = v
    if len(_items) == 0:
        print_help_cmd_env2json()
    if not _items.get('OPSCTL_OUTPUT'):
        print('--output is required')
        print_help_cmd_env2json()
    if os.path.dirname(_items['OPSCTL_OUTPUT']) and not os.path.exists(os.path.dirname(_items['OPSCTL_OUTPUT'])):
        print('%s is not a valid path' % _items['OPSCTL_OUTPUT'])
        print_help_cmd_env2json()
    if _items.get('OPSCTL_INPUT') and not os.path.isfile(_items['OPSCTL_INPUT']):
        print('%s is not a valid path' % _items['OPSCTL_INPUT'])
        print_help_cmd_env2json()
    return _items


def print_help_cmd_env2yaml():
    print('\n'.join([
        '\nopsctl env2yaml',
        '\t'.join([
            '  --output',
            'Output YAML file path'
        ]),
        '\t'.join([
            '  --input',
            'Optional. Ensure your input file format that is must be same with output of command "env".'
        ]),
        '\t'.join([
            '         ',
            'Get current os environ variables if let this option empty.'
        ]),
    ]))
    exit(1)


def check_cmd_env2yaml_opts(cmd_env2yaml_opts):
    """
    output is required
    :param cmd_env2yaml_opts:
    :return:
    """
    _items = dict()
    for k, v in cmd_env2yaml_opts:
        _items['OPSCTL_%s' % k.replace('--', '').upper()] = v
    if len(_items) == 0:
        print_help_cmd_env2yaml()
    if not _items.get('OPSCTL_OUTPUT'):
        print('--output is required')
        print_help_cmd_env2yaml()
    if os.path.dirname(_items['OPSCTL_OUTPUT']) and not os.path.exists(os.path.dirname(_items['OPSCTL_OUTPUT'])):
        print('%s is not a valid path' % _items['OPSCTL_OUTPUT'])
        print_help_cmd_env2yaml()
    if _items.get('OPSCTL_INPUT') and not os.path.isfile(_items['OPSCTL_INPUT']):
        print('%s is not a valid path' % _items['OPSCTL_INPUT'])
        print_help_cmd_env2yaml()
    return _items


def print_help_cmd_bamboo():
    print('\n'.join([
        '\nopsctl bamboo',
        '\t'.join([
            '  --host',
            'Bamboo server host base url'
        ]),
        '\t'.join([
            '  --token',
            'Bamboo server access token'
        ]),
        '\t'.join([
            '  --deploy',
            'Trigger Bamboo deployment project running. Format is deploymentProjectName:environmentName'
        ]),
        '\t'.join([
            '  --param',
            'Optional. Update target variables paramKey:paramValue'
        ]),
    ]))
    exit(1)


def check_cmd_bamboo_opts(cmd_bamboo_opts):
    """
    host, token, deploy/build is required
    :param cmd_bamboo_opts:
    :return:
    """
    _items = dict()
    for k, v in cmd_bamboo_opts:
        _items['OPSCTL_%s' % k.replace('--', '').upper()] = v
    if len(_items) == 0:
        print_help_cmd_bamboo()
    if not _items.get('OPSCTL_HOST'):
        if os.getenv("bamboo_resultsUrl"):
            parse_result = urlparse(os.getenv("bamboo_resultsUrl"))
            _items['OPSCTL_HOST'] = "%s://%s" % (parse_result.scheme, parse_result.netloc)
        else:
            print('--host is required')
            print_help_cmd_bamboo()
    if not _items.get('OPSCTL_TOKEN'):
        print('--token is required')
        print_help_cmd_bamboo()
    if not _items.get('OPSCTL_DEPLOY'):
        print('--deploy is required')
        print_help_cmd_bamboo()
    _items['OPSCTL_DEPLOY_PROJECT'], _items['OPSCTL_DEPLOY_ENVIRONMENT'] = _items.get('OPSCTL_DEPLOY').split(":")
    if not _items.get('OPSCTL_DEPLOY_PROJECT') or not _items.get('OPSCTL_DEPLOY_ENVIRONMENT'):
        print('--deploy is required')
        print_help_cmd_bamboo()
    if _items.get('OPSCTL_PARAM'):
        opsctl_params = _items.get('OPSCTL_PARAM').split(",")
        _items['OPSCTL_PARAM'] = {}
        for param_item in opsctl_params:
            param_k, param_v = param_item.split(":")
            _items['OPSCTL_PARAM'][param_k] = param_v
    else:
        _items['OPSCTL_PARAM'] = {}
    return _items


def output_env(output_type, output_path, input_path):
    output_content = ""
    if input_path:
        with open(input_path, 'r', encoding='utf-8') as f:
            input_file_content = f.read()
        input_content = dict()
        for input_file_line in input_file_content.split('\n'):
            if input_file_line:
                key, value = input_file_line.replace('=', ': ', 1).split(': ')
                input_content[key] = value
    else:
        input_content = dict(os.environ)
    if output_type == "json":
        output_content = json.dumps(input_content)
    elif output_type == "yaml":
        output_content = yaml.safe_dump(input_content)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output_content)
    print('\tSucceed to generate %s' % output_path)
    return True


def run_bamboo(bamboo_host, bamboo_token, run_info):
    bamboo = Bamboo(bamboo_host, bamboo_token)
    execution_rsp = bamboo.trigger_deployment_environment_setup(
        deploy_project=run_info["deploy_project"],
        deploy_environment=run_info["deploy_environment"],
        trigger_param=run_info["trigger_param"]
    )
    print('\tSucceed to run bamboo [%s](%s)' % (
        execution_rsp.get("deploymentResultId"),
        execution_rsp["link"]["href"]
    ))
    return True


def main():
    try:
        tool_cmd = sys.argv[1]
    except IndexError:
        tool_cmd = ''
        print_help_tool()
    cmd_args = sys.argv[2:]
    cmd_args_items = dict()
    if tool_cmd == 'tmpl2art':
        try:
            opts, args = getopt(
                args=cmd_args,
                shortopts='',
                longopts=[
                    'config=',
                    'tmpl=',
                    'output=',
                ]
            )
            cmd_args_items = check_cmd_tmpl2art_opts(opts)
        except GetoptError:
            print_help_cmd_tmpl2art()
        opsctl_render = opsctlRender(
            config_file=cmd_args_items['OPSCTL_CONFIG'],
            template_path=cmd_args_items['OPSCTL_TMPL'],
            output_path=cmd_args_items['OPSCTL_OUTPUT']
        )
        if os.path.isfile(cmd_args_items['OPSCTL_TMPL']):
            opsctl_render.render_file()
        else:
            opsctl_render.render_all()
    elif tool_cmd == 'env2json':
        try:
            opts, args = getopt(
                args=cmd_args,
                shortopts='',
                longopts=[
                    'output=',
                    'input=',
                ]
            )
            cmd_args_items = check_cmd_env2json_opts(opts)
        except GetoptError:
            print_help_cmd_env2json()
        output_env(
            output_type='json',
            output_path=cmd_args_items['OPSCTL_OUTPUT'],
            input_path=cmd_args_items.get('OPSCTL_INPUT')
        )
    elif tool_cmd == 'env2yaml':
        try:
            opts, args = getopt(
                args=cmd_args,
                shortopts='',
                longopts=[
                    'output=',
                    'input=',
                ]
            )
            cmd_args_items = check_cmd_env2yaml_opts(opts)
        except GetoptError:
            print_help_cmd_env2yaml()
        output_env(
            output_type='yaml',
            output_path=cmd_args_items['OPSCTL_OUTPUT'],
            input_path=cmd_args_items.get('OPSCTL_INPUT')
        )
    elif tool_cmd == 'bamboo':
        try:
            opts, args = getopt(
                args=cmd_args,
                shortopts='',
                longopts=[
                    'host=',
                    'token=',
                    'deploy=',
                    'param=',
                ]
            )
            cmd_args_items = check_cmd_bamboo_opts(opts)
        except GetoptError:
            print_help_cmd_bamboo()
        run_bamboo(
            bamboo_host=cmd_args_items['OPSCTL_HOST'],
            bamboo_token=cmd_args_items['OPSCTL_TOKEN'],
            run_info={
                "deploy_project": cmd_args_items['OPSCTL_DEPLOY_PROJECT'],
                "deploy_environment": cmd_args_items['OPSCTL_DEPLOY_ENVIRONMENT'],
                "trigger_param": cmd_args_items['OPSCTL_PARAM']
            }
        )
    elif tool_cmd == 'version':
        print('opsctl v0.0.1')
    else:
        print_help_tool()


if __name__ == '__main__':
    main()
