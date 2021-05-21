#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: v.stone@163.com


from getopt import getopt, GetoptError
import sys
import os
from opsctl.render import Render as opsctlRender


def print_help_tool():
    print('\n'.join([
        '\nopsctl',
        '\t'.join([
            '  tmpl2art   ',
            'Render templates to articles'
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
            '  --tmpldir',
            'Template root path'
        ]),
        '\t'.join([
            '  --artdir',
            'Articles output path'
        ]),
    ]))
    exit(1)


def check_cmd_tmpl2art_opts(cmd_tmpl2art_opts):
    """
    config, template, render are required
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
    if not _items.get('OPSCTL_TEMPLATE'):
        print('--template is required')
        print_help_cmd_tmpl2art()
    if not _items.get('OPSCTL_RENDER'):
        print('--render is required')
        print_help_cmd_tmpl2art()
    if not os.path.isfile(_items['OPSCTL_CONFIG']):
        print('%s is not a valid file' % _items['OPSCTL_CONFIG'])
        print_help_cmd_tmpl2art()
    if not os.path.isdir(_items['OPSCTL_TEMPLATE']):
        print('%s is not a valid dir' % _items['OPSCTL_TEMPLATE'])
        print_help_cmd_tmpl2art()
    return _items


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
                    'template=',
                    'render=',
                ]
            )
            cmd_args_items = check_cmd_tmpl2art_opts(opts)
        except GetoptError:
            print_help_cmd_tmpl2art()
        yaml_render = opsctlRender(
            config_file=cmd_args_items['OPSCTL_CONFIG'],
            template_dir=cmd_args_items['OPSCTL_TEMPLATE'],
            render_dir=cmd_args_items['OPSCTL_RENDER']
        )
        yaml_render.render_all()
    elif tool_cmd == 'version':
        print('opsctl v{{OPSC_VERSION}}')
    else:
        print_help_tool()


if __name__ == '__main__':
    main()
