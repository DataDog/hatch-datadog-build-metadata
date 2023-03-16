# SPDX-FileCopyrightText: 2023-present Datadog, Inc. <dev@datadoghq.com>
#
# SPDX-License-Identifier: MIT
import os
import zipfile

from .utils import build_project, git, read_file, write_file


def test_basic(new_project_basic):
    build_project('-t', 'wheel')

    build_dir = os.path.join(new_project_basic, 'dist')
    assert os.path.isdir(build_dir)

    artifacts = os.listdir(build_dir)
    assert len(artifacts) == 1
    wheel_file = artifacts[0]

    assert wheel_file == 'my_app-1.2.3-py2.py3-none-any.whl'

    extraction_directory = os.path.join(os.path.dirname(new_project_basic), '_archive')
    os.mkdir(extraction_directory)

    with zipfile.ZipFile(os.path.join(build_dir, wheel_file), 'r') as zip_archive:
        zip_archive.extractall(extraction_directory)

    metadata_directory = os.path.join(extraction_directory, 'my_app-1.2.3.dist-info')
    assert os.path.isdir(metadata_directory)

    package_directory = os.path.join(extraction_directory, 'my_app')
    assert os.path.isdir(package_directory)
    assert len(os.listdir(package_directory)) == 4

    assert os.path.isfile(os.path.join(package_directory, '__init__.py'))
    assert os.path.isfile(os.path.join(package_directory, 'foo.py'))
    assert os.path.isfile(os.path.join(package_directory, 'bar.py'))
    assert os.path.isfile(os.path.join(package_directory, 'baz.py'))

    contents = read_file(os.path.join(metadata_directory, 'METADATA'))

    assert 'Project-URL' not in contents


def test_default(new_project_default):
    build_project('-t', 'wheel')

    build_dir = os.path.join(new_project_default, 'dist')
    assert os.path.isdir(build_dir)

    artifacts = os.listdir(build_dir)
    assert len(artifacts) == 1
    wheel_file = artifacts[0]

    assert wheel_file == 'my_app-1.2.3-py2.py3-none-any.whl'

    extraction_directory = os.path.join(os.path.dirname(new_project_default), '_archive')
    os.mkdir(extraction_directory)

    with zipfile.ZipFile(os.path.join(build_dir, wheel_file), 'r') as zip_archive:
        zip_archive.extractall(extraction_directory)

    metadata_directory = os.path.join(extraction_directory, 'my_app-1.2.3.dist-info')
    assert os.path.isdir(metadata_directory)

    package_directory = os.path.join(extraction_directory, 'my_app')
    assert os.path.isdir(package_directory)
    assert len(os.listdir(package_directory)) == 4

    assert os.path.isfile(os.path.join(package_directory, '__init__.py'))
    assert os.path.isfile(os.path.join(package_directory, 'foo.py'))
    assert os.path.isfile(os.path.join(package_directory, 'bar.py'))
    assert os.path.isfile(os.path.join(package_directory, 'baz.py'))

    contents = read_file(os.path.join(metadata_directory, 'METADATA'))

    assert f'Project-URL: source_code_link, https://foo.bar.baz/path/repo#{git("rev-parse", "HEAD")}' in contents


def test_override(new_project_override):
    build_project('-t', 'wheel')

    build_dir = os.path.join(new_project_override, 'dist')
    assert os.path.isdir(build_dir)

    artifacts = os.listdir(build_dir)
    assert len(artifacts) == 1
    wheel_file = artifacts[0]

    assert wheel_file == 'my_app-1.2.3-py2.py3-none-any.whl'

    extraction_directory = os.path.join(os.path.dirname(new_project_override), '_archive')
    os.mkdir(extraction_directory)

    with zipfile.ZipFile(os.path.join(build_dir, wheel_file), 'r') as zip_archive:
        zip_archive.extractall(extraction_directory)

    metadata_directory = os.path.join(extraction_directory, 'my_app-1.2.3.dist-info')
    assert os.path.isdir(metadata_directory)

    package_directory = os.path.join(extraction_directory, 'my_app')
    assert os.path.isdir(package_directory)
    assert len(os.listdir(package_directory)) == 4

    assert os.path.isfile(os.path.join(package_directory, '__init__.py'))
    assert os.path.isfile(os.path.join(package_directory, 'foo.py'))
    assert os.path.isfile(os.path.join(package_directory, 'bar.py'))
    assert os.path.isfile(os.path.join(package_directory, 'baz.py'))

    contents = read_file(os.path.join(metadata_directory, 'METADATA'))

    assert (
        f'Project-URL: source_code_link, git+ssh://git@foo.bar.baz/path/repo.git#{git("rev-parse", "HEAD")}' in contents
    )


def test_source_distribution(new_project_default):
    write_file(
        os.path.join(new_project_default, 'PKG-INFO'),
        """\
Name: my_app
Version: 1.2.3
Project-URL: foo     ,     https://foo.baz/path/repo
Project-URL: bar     ,     https://bar.baz/path/repo
""",
    )
    build_project('-t', 'wheel')

    build_dir = os.path.join(new_project_default, 'dist')
    assert os.path.isdir(build_dir)

    artifacts = os.listdir(build_dir)
    assert len(artifacts) == 1
    wheel_file = artifacts[0]

    assert wheel_file == 'my_app-1.2.3-py2.py3-none-any.whl'

    extraction_directory = os.path.join(os.path.dirname(new_project_default), '_archive')
    os.mkdir(extraction_directory)

    with zipfile.ZipFile(os.path.join(build_dir, wheel_file), 'r') as zip_archive:
        zip_archive.extractall(extraction_directory)

    metadata_directory = os.path.join(extraction_directory, 'my_app-1.2.3.dist-info')
    assert os.path.isdir(metadata_directory)

    package_directory = os.path.join(extraction_directory, 'my_app')
    assert os.path.isdir(package_directory)
    assert len(os.listdir(package_directory)) == 4

    assert os.path.isfile(os.path.join(package_directory, '__init__.py'))
    assert os.path.isfile(os.path.join(package_directory, 'foo.py'))
    assert os.path.isfile(os.path.join(package_directory, 'bar.py'))
    assert os.path.isfile(os.path.join(package_directory, 'baz.py'))

    contents = read_file(os.path.join(metadata_directory, 'METADATA'))

    assert 'Project-URL: source_code_link' not in contents
    assert 'Project-URL: foo, https://foo.baz/path/repo' in contents
    assert 'Project-URL: bar, https://bar.baz/path/repo' in contents
