# SPDX-FileCopyrightText: 2023-present Datadog, Inc. <dev@datadoghq.com>
#
# SPDX-License-Identifier: MIT
import pytest

from hatch_datadog_build_metadata import vcs_utils


@pytest.mark.parametrize(
    'remote_url, http_url',
    [
        ('http://foo.bar.baz/path/repo.git', 'http://foo.bar.baz/path/repo.git'),
        ('https://foo.bar.baz/path/repo.git', 'https://foo.bar.baz/path/repo.git'),
        ('git@foo.bar.baz:path/repo.git', 'https://foo.bar.baz/path/repo.git'),
        ('git@foo.bar.baz:9000:path/repo.git', 'https://foo.bar.baz:9000/path/repo.git'),
        ('git@foo.bar.baz/path/repo.git', 'https://foo.bar.baz/path/repo.git'),
        ('git+ssh://git@foo.bar.baz:path/repo.git', 'https://foo.bar.baz/path/repo.git'),
        ('git+ssh://git@foo.bar.baz:9000:path/repo.git', 'https://foo.bar.baz:9000/path/repo.git'),
        ('git+ssh://git@foo.bar.baz/path/repo.git', 'https://foo.bar.baz/path/repo.git'),
        ('git+ssh://git@foo.bar.baz:9000/path/repo.git', 'https://foo.bar.baz:9000/path/repo.git'),
        ('https://ci-token:12345AbcDFoo_qbcdef@foo.bar.baz/path/repo.git', 'https://foo.bar.baz/path/repo.git'),
    ],
)
def test_parse_http_url(remote_url, http_url):
    assert vcs_utils.parse_http_url(remote_url) == http_url
