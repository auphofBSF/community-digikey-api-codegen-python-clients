# coding: utf-8

"""
    CodeGen automater for Digikey V3 API's  and provides a simple interface to the API's

    Automates and customizes the Swagger Codgen to take swagger API specification from Digikey and produce and install the Python Clients to the Digikey API, also integrates and installs community-digikey-simple-v3-api that is a simplified  interface handling Authentication under Oauth2 protocol.

    See README.md for installation and use

    Digikey API's use OpenAPI spec version: v3
    Contact: api.support@digikey.com
    CodeGen Automater and community produced Digikey interface by: https://github.com/auphofBSF with Oauth2 token management from the Digikey V2 api https://github.com/peeter123/digikey-api
"""


from setuptools import setup, find_packages  # noqa: H301
from setuptools.command.develop import develop
from setuptools.command.install import install
from setuptools.command.build_py import build_py
from setuptools.command.bdist_egg import bdist_egg
from setuptools.command.egg_info import egg_info
# from setuptools.command.bdist_wheel import bdist_wheel

NAME = "community-digikey-api-codegen-python-clients"
VERSION = "0.1.0"
# To install the library, run the following
#
# pip install -e .
#
# prerequisite: pip, gitpython
# 

REQUIRES = [
    "gitpython",
    "requests",
]
    

class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        # check_call("apt-get install this-package".split())
        print("----Custom Develop - pre develop.run")
        develop.run(self)
        print("----Custom Develop - post develop.run")
        digikeyAPIclientGenerate()

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        # check_call("apt-get install this-package".split())
        print("----Custom Install - pre install.run")
        install.run(self)
        print("----Custom Install - post install.run")
        digikeyAPIclientGenerate()
#TODO: Generate seem to be called to frequently, identify whic are necssary
class PostBuild_pyCommand(build_py):
    """Post-installation for installation mode."""
    def run(self):
        # check_call("apt-get install this-package".split())
        print("----Custom Build_py - pre install.run")
        build_py.run(self)
        print("----Custom Build_py - post install.run")
        digikeyAPIclientGenerate()

class PostBdist_eggCommand(bdist_egg):
    """Post-installation for installation mode."""
    def run(self):
        # check_call("apt-get install this-package".split())
        print("----Custom bdist_egg - pre install.run")
        bdist_egg.run(self)
        print("----Custom bdist_egg - post install.run")
        digikeyAPIclientGenerate()

class PostEgg_infoCommand(egg_info):
    """Post-installation for installation mode."""
    def run(self):
        # check_call("apt-get install this-package".split())
        print("----Custom egg_info - pre install.run")
        egg_info.run(self)
        print("----Custom egg_info - post install.run")
        digikeyAPIclientGenerate()

def digikeyAPIclientGenerate():

    from community_digikey_api_codegen import tools

    # Currently supported API's
    apiGenerateList = ['product-information','order-support']
    # apiGenerateList = ['order-support']

    #Generate Digikey API python clients
    generated= [
    tools.codeGen_api(tools.digikeyAPIdef_all[api], 
                tools.swaggerCodeGen_config_all[api])
        for api in apiGenerateList
    ]

    # Install the generated generated
    import os, subprocess
    rememberDir = os.getcwd()
    for api in generated:
        os.chdir(api['locationPath'])
        subprocessCMD = [
        'pip'
        , 'install'
        # , '--editable'
        , '.'
        ]
        tools.subprocess_run(subprocessCMD)
    os.chdir(rememberDir)


setup(
    name=NAME,
    version=VERSION,
    description="CodeGen Automater for Digikey V3 API's ",
    author_email="auphofBSF_GH1@blacksheepfarm.co.nz",
    url="https://github.com/auphofBSF/community-digikey-api-codegen-python-clients",
    keywords=["Swagger", "CodeGen","Digikey Api"],
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
        'build_py': PostBuild_pyCommand,
        'bdist_egg': PostBdist_eggCommand,
        # 'egg_info': PostEgg_infoCommand,

        },
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description="""\
    Automates and customizes the Swagger CodGen to take swagger API specification from Digikey then generate and install the Python Clients to the Digikey API, also integrates and installs community-digikey-simple-v3-api that is a simplified  interface handling Authentication under Oauth2 protocol.  # noqa: E501
    """
)

    
