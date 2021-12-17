# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os

from azure.cli.testsdk import (ScenarioTest)


TEST_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), '..'))


class InitScenarioTest(ScenarioTest):

    def test_init(self):
        pass
