# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import json

from azure.cli.core.azclierror import AzCLIError
from azure.cli.core.azclierror import AzCLIErrorType
from knack import help_files
from .utils import get_yes_or_no_option, get_int_option
from .constants import RecommendType
from colorama import Fore, init


def _get_last_cmd(cmd):
    '''Get last executed command from local log files'''
    import os
    history_file_name = os.path.join(cmd.cli_ctx.config.config_dir, 'recommendation', 'cmd_history.log')
    if not os.path.exists(history_file_name):
        return ''
    with open(history_file_name, "r") as f:
        lines = f.read().splitlines()
        lines = [x for x in lines if x != 'next']
        return lines[-1]
    return ''


def _get_last_exception(cmd):
    '''Get last executed command from local log files'''
    import os
    history_file_name = os.path.join(cmd.cli_ctx.config.config_dir, 'recommendation', 'exception_history.log')
    if not os.path.exists(history_file_name):
        return ''
    with open(history_file_name, "r") as f:
        lines = f.read().splitlines()
        return lines[-1]
    return ''


def _process_exception(exception_str):
    '''Extract more information from the exception string'''
    return exception_str


def _handle_error_no_exception_found():
    '''You choose to solve the previous problems but no exception found'''
    error_msg = 'The error information is missing, ' \
                'the solution is recommended only if only an exception occurs in the previous step.'
    recommendation = 'You can set the recommendation type to 1 to get all available recommendations.'
    az_error = AzCLIError(AzCLIErrorType.RecommendationError, error_msg)
    az_error.set_recommendation(recommendation)
    az_error.print_error()


def _get_recommend_from_api(last_cmd, type, top_num=5, error_info=None):  # pylint: disable=unused-argument
    '''query next command from web api'''
    import requests
    url = "https://cli-recommendation.azurewebsites.net/api/RecommendationService"
    payload = {
        "command": last_cmd,
        "type": type,
        "top_num": top_num,
        'error_info': error_info
    }
    response = requests.post(url, json.dumps(payload))
    if response.status_code != 200:
        raise AzCLIError(AzCLIErrorType.RecommendationError,
                         "Failed to connect to '{}' with status code '{}' and reason '{}'".format(
                             url, response.status_code, response.reason))

    recommends = []
    if 'data' in response.json():
        recommends = response.json()['data']

    return recommends


def _give_recommends(recommends):
    idx = 0
    for rec in recommends:
        idx += 1
        if 'scenario' in rec:
            _give_recommend_scenarios(idx, rec)
        else:
            _give_recommend_commands(idx, rec)


def _give_recommend_commands(idx, rec):
    command_item = "{}. az {}".format(idx, rec['command'])
    if 'arguments' in rec:
        command_item = "{} {}".format(command_item, ' '.join(rec['arguments']))
    print(command_item)

    if 'reason' in rec:
        reason = rec['reason']
    else:
        reason = ""
        cmd_help = help_files._load_help_file(rec['command'])
        if cmd_help and 'short-summary' in cmd_help:
            reason = cmd_help['short-summary']
        if 'ratio' in rec and rec['ratio']:
            reason = "{} {:.1f}% people use this command in next step. ".format(reason, rec['ratio'] * 100)
    print(Fore.LIGHTCYAN_EX + "Recommended reason: {}.\n".format(reason))


def _give_recommend_scenarios(idx, rec):
    print("{}. \033[1;33m[E2E]\033[0m {}".format(idx, rec['scenario']))
    print(Fore.LIGHTCYAN_EX + "Recommended reason: the E2E scenarios you may be using.\n")


def _execute_recommends(cmd, rec):
    if 'scenario' in rec:
        _execute_recommend_scenarios(cmd, rec)
    else:
        _execute_recommend_commands(cmd, rec)


def _execute_nx_cmd(cmd, nx_cmd, nx_param):
    args = []
    args.extend(nx_cmd.split())
    nx_param = [param for param in nx_param if param and param != '']
    for param in nx_param:
        value = input("Please input {}: ".format(param))
        args.append(param)
        if value:
            args.append(value)

    return cmd.cli_ctx.invoke(args)


def _execute_recommend_commands(cmd, rec):
    doit = get_yes_or_no_option("Do you want to run it in prompt mode immediately? (y/n): ")
    if not doit:
        print('Recommend abort \n')
        return

    nx_param = []
    if "arguments" in rec:
        nx_param = rec["arguments"]
    print(Fore.LIGHTYELLOW_EX + "Running: az {} {}".format(rec["command"], ' '.join(nx_param) if nx_param else ""))
    _execute_nx_cmd(cmd, rec["command"], nx_param)


def _execute_recommend_scenarios(cmd, rec):
    print("The scenario of '{}' contains the following commands:\n".format(rec['scenario']))

    nx_cmd_set = rec["nextCommandSet"]
    idx = 0
    for nx_cmd in nx_cmd_set:
        idx += 1
        if "arguments" in nx_cmd:
            nx_param = nx_cmd["arguments"]
        print("{}. az {} {}".format(idx, nx_cmd['command'], ' '.join(nx_param) if nx_param else ""))
        print(Fore.LIGHTCYAN_EX + "{}\n".format(nx_cmd['reason']))

    doit = get_yes_or_no_option("Do you want to run this scenario in prompt mode immediately? (y/n): ")
    if not doit:
        print('Recommend abort \n')
        return

    for nx_cmd in nx_cmd_set:
        nx_param = []
        if "arguments" in nx_cmd:
            nx_param = nx_cmd["arguments"]
        print(Fore.LIGHTYELLOW_EX + "Running: az {} {}".format(nx_cmd['command'],
                                                               ' '.join(nx_param) if nx_param else ""))
        step_msg = "How do you want to run this step? 1. Run 2. Skip 3. Stop (RETURN is to Run): "
        run_option = get_int_option(step_msg, 1, 3, 1)
        if run_option == 1:
            execute_result = _execute_nx_cmd(cmd, nx_cmd['command'], nx_param)
            if execute_result != 0:
                print()
                break
        elif run_option == 2:
            print()
            continue
        else:
            print()
            break

    print('All commands in this scenario have been executed! \n')


def _get_filter_option():
    msg = '''
Please select the type of recommendation you need:
1. all: It will intelligently analyze the types of recommendation you need, and may recommend multiple types of command to you
2. solution: Only the solutions to problems when errors occur are recommend
3. command: Only the commands with high correlation with previously executed commands are recommend
4. scenario: Only the E2E scenarios related to current usage scenarios are recommended
'''
    print(msg)
    return get_int_option("What kind of recommendation do you want? (RETURN is to set all): ", 1, 4, 1)


def handle_next(cmd):
    init(autoreset=True) # turn on automatic color recovery for colorama

    option = _get_filter_option()
    processed_exception = None
    if option == RecommendType.All or option == RecommendType.Solution:
        last_exception = _get_last_exception(cmd)
        processed_exception = _process_exception(last_exception)

    if option == RecommendType.Solution and not processed_exception:
        _handle_error_no_exception_found()
        return None

    last_cmd = _get_last_cmd(cmd)
    recommends = _get_recommend_from_api(last_cmd, option, error_info=processed_exception)
    if not recommends:
        print("\nSorry, no recommendation for '{}' yet.".format(last_cmd))
        return

    print()
    _give_recommends(recommends)

    if len(recommends) > 1:
        option = get_int_option("Which one is helpful to you? (If none, please input 0): ", 0, len(recommends), -1)
    else:
        option = get_yes_or_no_option("Does it helpful to you? (y/n): ")
        option = 1 if option else 0
    if option == 0:
        # we can send feedback here
        print('Thank you for your feedback \n')
        return
    print()

    _execute_recommends(cmd, recommends[option - 1])

    return None
