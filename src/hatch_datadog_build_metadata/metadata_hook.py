# SPDX-FileCopyrightText: 2023-present Datadog, Inc. <dev@datadoghq.com>
#
# SPDX-License-Identifier: MIT
import os
from collections import ChainMap

from hatchling.metadata.plugin.interface import MetadataHookInterface
from hatchling.utils.context import ContextStringFormatter

from hatch_datadog_build_metadata import vcs_utils


class DatadogBuildMetadataHook(MetadataHookInterface):
    PLUGIN_NAME = 'datadog-build-metadata'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__config_urls = None

    @property
    def config_urls(self):
        if self.__config_urls is None:
            urls = self.config.get('urls', {})
            if not isinstance(urls, dict):
                raise TypeError('option `urls` must be a table')

            for key, url in urls.items():
                if not isinstance(url, str):
                    raise TypeError(f'URL `{key}` in option `urls` must be a string')

            self.__config_urls = urls

        return self.__config_urls

    def update(self, metadata):
        pkg_info_file = os.path.join(self.root, 'PKG-INFO')
        if os.path.isfile(pkg_info_file):
            import email

            with open(pkg_info_file, encoding='utf-8') as f:
                message = email.message_from_string(f.read())

            urls = {}
            for header, value in message.items():
                if header.lower() == 'project-url':
                    key, _, url = value.partition(',')
                    urls[key.strip()] = url.strip()

            metadata['urls'] = urls
            return

        urls = self.config_urls.copy()
        urls.setdefault('source_code_link', '{remote_http_url}#{commit_hash}')

        formatter = ContextStringFormatter(
            ChainMap(
                {
                    'commit_hash': lambda *args: vcs_utils.get_commit_hash(self.root),
                    'remote_http_url': lambda *args: vcs_utils.get_http_url(self.root),
                    'remote_url': lambda *args: vcs_utils.get_remote_url(self.root),
                },
            )
        )
        for key, url in urls.items():
            urls[key] = formatter.format(url)

        metadata['urls'] = urls
