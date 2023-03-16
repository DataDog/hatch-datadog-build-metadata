# SPDX-FileCopyrightText: 2023-present Datadog, Inc. <dev@datadoghq.com>
#
# SPDX-License-Identifier: MIT
import os
import subprocess
import sys


def create_file(path):
    with open(path, 'a'):
        os.utime(path, None)


def read_file(path):
    with open(path, encoding='utf-8') as f:
        return f.read()


def write_file(path, contents):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(contents)


def build_project(*args):
    _run_command(sys.executable, '-m', 'hatchling', 'build', *args)


def git(*args):
    return _run_command('git', *args)


def _run_command(*command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, _ = process.communicate()
    stdout = stdout.decode('utf-8')

    if process.returncode:  # no cov
        raise Exception(stdout)

    return stdout
