#      Copyright 2020. ThingsBoard
#  #
#      Licensed under the Apache License, Version 2.0 (the "License");
#      you may not use this file except in compliance with the License.
#      You may obtain a copy of the License at
#  #
#          http://www.apache.org/licenses/LICENSE-2.0
#  #
#      Unless required by applicable law or agreed to in writing, software
#      distributed under the License is distributed on an "AS IS" BASIS,
#      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#      See the License for the specific language governing permissions and
#      limitations under the License.
#
#

from os import path
from setuptools import setup


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

VERSION = "1.2"

setup(
    version=VERSION,
    name="vl-mqtt-client",
    author="Viralink",
    author_email="info@viralink.io",
    license="Apache Software License (Apache Software License 2.0)",
    description="ViraLink python client SDK",
    url="https://github.com/viralinkio/viralink-python-client-sdk",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    packages=["."],
    install_requires=['paho-mqtt', 'jsonschema', 'requests', 'mmh3'],
    download_url='https://github.com/viralinkio/viralink-python-client-sdk/archive/%s.tar.gz' % VERSION)
