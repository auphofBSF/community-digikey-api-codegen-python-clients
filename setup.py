# coding: utf-8

"""
    Builder for Digikey V3 API's  and provides a simple interface to the API's

    Automates and customizes the Swagger Codgen to take swagger API specification from Digikey and produce and install the Python Clients to the Digikey API, also integrates and installs community-digikey-simple-v3-api that is a simplified  interface handling Authentication under Oauth2 protocol.

    See README.md for installation and use

    Digikey API's use OpenAPI spec version: v3
    Contact: api.support@digikey.com
    Builder and community produced Digikey interface by: https://github.com/auphofBSF with Oauth2 token management from the Digikey V2 api https://github.com/peeter123/digikey-api
"""


from setuptools import setup, find_packages  # noqa: H301

NAME = "community-digikey-api-builder-python-client"
VERSION = "0.1.0"
# To install the library, run the following
#
# pip install -e .
#
# prerequisite: pip, gitpython
# 

REQUIRES = [
    "GitPython",
]
    

setup(
    name=NAME,
    version=VERSION,
    description="Builder for Digikey V3 API's ",
    author_email="auphofBSF_GH1@blacksheepfarm.co.nz",
    url="https://github.com/auphofBSF/community-digikey-api-build-python-client",
    keywords=["Swagger", "Digikey Api"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description="""\
    Automates and customizes the Swagger Codgen to take swagger API specification from Digikey and produce and install the Python Clients to the Digikey API, also integrates and installs community-digikey-simple-v3-api that is a simplified  interface handling Authentication under Oauth2 protocol.  # noqa: E501
    """
)

from community_digikey_api_build import tools

# Currently supported API's
apiBuildList = ['product-information','order-support']
# apiBuildList = ['order-support']

#Generate Digikey API python clients
builds= [
  tools.build_api(tools.digikeyAPIdef_all[api], 
            tools.swaggerCodeGen_config_all[api])
    for api in apiBuildList
]

# Install the builds generated
import os, subprocess
rememberDir = os.getcwd()
for build in builds:
    os.chdir(build['locationPath'])
    subprocessCMD = [
    'pip'
    , 'install'
    , '--editable'
    , '.'
    ]
    tools.subprocess_run(subprocessCMD)
os.chdir(rememberDir)
    
