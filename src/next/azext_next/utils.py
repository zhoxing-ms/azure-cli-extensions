# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------


def read_int(msg, default_value=0):
    ret = input(msg)
    if ret == '' or ret is None:
        return default_value
    while not ret.isnumeric():
        ret = input("Please input a legal number: ")
        if ret == '' or ret is None:
            return default_value
    return int(ret)


def get_yes_or_no_option(option_description):
    option = input(option_description)
    yes_options = ["y", "yes", "Y", "Yes", "YES"]
    no_options = ["n", "no", "N", "No", "NO"]
    while (option not in yes_options) and (option not in no_options):
        option = input("This option can only be Yes or No, please input again: ")
    return option in yes_options


def get_int_option(option_description, min_option, max_option, default_option):
    option = read_int(option_description, default_option)
    while option < min_option or option > max_option:
        option = read_int("The range of options is {}-{}, please input again: ".format(min_option, max_option),
                          default_option)
    return option
