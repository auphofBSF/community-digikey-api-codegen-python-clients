#conda: activate TRIAL18W06PY36websautomation
#Test: Atom

'''
A community initiative to automatically create a python client for the Digikey set of API's 
this application automates for the following API's 
    COMPLETED: productinformation
    COMPLETED: ordersupport
    TODO:barcode
    TODO:Ordering

The Digikey API specification in Swagger.json format is the basis of the generated python clients
The generation is done by using the Swagger Codegen, a java application.

This script then performs a fresh build of the 

The platform prerequisites are java and python the package are gitpython


'''
# def is_interactive():
#     import __main__ as main
#     return not hasattr(main, '__file__')
# if not is_interactive():
#     %load_ext autoreload
#     %autoreload 2


import logging
logging.basicConfig(level=logging.DEBUG)
import os
import configparser
config = configparser.ConfigParser()
config['custom'] = {
    'DEST_PATH': '..'
    , 'TMP_PATH': r'.\tmp'
    }
config.read(os.path.join('.env','config.ini'))
DEST_PATH = config['custom']['DEST_PATH']
TMP_PATH = config['custom']['TMP_PATH']

import zipfile, subprocess, shutil
import sys,requests
import git
import json
import re

logging.info("Build Directory for Digikey API's: {buildDir}".format(buildDir=TMP_PATH))

envExecureRoot = os.getcwd()

if not os.path.exists(TMP_PATH):
    os.makedirs(TMP_PATH)
os.chdir(TMP_PATH)


def getDigikeyAPIswaggerSpecJSON(destPath,**kwargs):
    # refererURL='https://developer.digikey.com/products/product-information/partsearch/productdetails?prod=true'
    refererURL='https://developer.digikey.com/products/{apiGroup}/{apiSubGroup}/{apiQuery}?prod=true'.format(**kwargs)
    url = 'https://developer.digikey.com/node/432/oas-download'
    r = requests.get(url, headers={
          'referer': refererURL
        , 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        })
    if r.ok:
        swaggerSpecFile="digikeyAPI-{apiGroup}-swagger-spec.json".format(**kwargs)
        with open(os.path.join(destPath,swaggerSpecFile), 'wb') as f:
            f.write(r.content)
        logging.info('Retrieved Digikey API Specification: {}'.format(swaggerSpecFile))
    else:
        message='Unable to retrieve Digikey API Specification: {apiGroup}/{apiSubGroup}/{apiQuery}'.format(kwargs)
        logging.error(message)
        raise Exception(message)
    return(os.path.join(destPath,swaggerSpecFile))







#download the SWAGGER.JSON for the required DIGIKEY API


digikeyAPIdef =dict(apiGroup='product-information'
                ,apiSubGroup = 'partsearch'
                    ,apiQuery='productdetails')
swaggerSpecFile=getDigikeyAPIswaggerSpecJSON(TMP_PATH, **digikeyAPIdef)

#setup the CONFIG file


swaggerCodeGen_config = {
    "packageName" : "digikey_productinformation",
    "projectName" : "community-digikey-api-productinformation",
    "packageVersion" : "0.1.0",
    "packageUrl" : "https://github.com/auphofBSF/xxxxxxxxxx.git",

}
configFile_swaggerCodegen='{projectName}-config-SwaggerCodegen.json'.format(**swaggerCodeGen_config)
with open(configFile_swaggerCodegen, 'w') as outfile:
    json.dump(swaggerCodeGen_config, outfile)

logging.info("Created config file for Swagger Codegen: {}".format(configFile_swaggerCodegen))



def wget(fileName,url):
    r = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        })

    with open(fileName, 'wb') as f:
        f.write(r.content)


#check if the swagger-codgen is present, else download
if os.path.isfile('swagger-codegen-cli.jar'):
    logging.info("Swagger-CodeGen already exists, no download required")
else:
    url = 'http://central.maven.org/maven2/io/swagger/swagger-codegen-cli/2.4.10/swagger-codegen-cli-2.4.10.jar'
    wget('swagger-codegen-cli.jar' , url)
    logging.info("Swagger-CodeGen downloaded from: {}".format(url))


# execute swagger-codegen
# Check Java is installed
try:
    version = subprocess.check_output(['java', '-version'], stderr=subprocess.STDOUT).decode('utf-8')
    patternJavaVersion = '\"(\d+\.\d+).*\"'
    logging.info("Java exists, version: {}".format(re.search(patternJavaVersion, version).groups()[0]))
except:
    logging.critical("Java existence cannot be confirmed -------------------")



codeGenRunCommand = [
       'java'
     , '-jar'
     , 'swagger-codegen-cli.jar'
     , 'generate'
     , '--input-spec',  swaggerSpecFile
     , '-l', 'python'
     , '--output', os.path.join(DEST_PATH,'{projectName}'.format(**swaggerCodeGen_config))
     , '--config', configFile_swaggerCodegen
    ]

try:
    logging.info('STARTING Code generator for a Swagger API created, project name: {projectName}'.format(**swaggerCodeGen_config))
    procCall = subprocess.run(codeGenRunCommand,stdout=subprocess.PIPE,stderr=subprocess.PIPE) #, shell=True)
    logging.info('COMPLETED Code generator for a Swagger API created, project name: {projectName}'.format(**swaggerCodeGen_config))
    logging.info('----- STDOUT = \n{}'.format(procCall.stdout.decode('utf-8')))
    logging.info('----- STDERR = \n{}'.format(procCall.stderr.decode('utf-8')))
    if procCall.returncode != 0:
        message="Failure performing Swagger Codegen: Return Code:{}".format(procCall.returncode)
        logging.critical(message)
        raise Exception(message)

except Exception as e:
    logging.critical("Failure performing Swagger Codegen: Exception:{}".format(e))
    raise Exception("Failure performing Swagger Codegen: Exception:{}".format(e))





try:
    # Copy Codgen Config, swagger spec and codegen Run command into swagger folder
    buildConfigDir = os.path.join(DEST_PATH,'{projectName}'.format(**swaggerCodeGen_config),'.build-config')
    os.makedirs(buildConfigDir)
    shutil.copy(configFile_swaggerCodegen,dst=buildConfigDir)
    shutil.copy(swaggerSpecFile,dst=buildConfigDir)
    shutil.copy(__file__, dst=buildConfigDir) # Keep a copy of this script that built the client
    logging.info('----- COPIED build and/or specification files into project')
except Exception as e:
    message='Failed to copy Build and/or Specification file cause Exception:{}'.format(e)
    logging.critical(message)
    raise Exception(message)



# GIT initialize the repo and commit #
logging.info('START Code Version control enabling under GIT')

gitrepo = git.Repo.init(os.path.join(DEST_PATH,'{projectName}'.format(**swaggerCodeGen_config)))
gitrepo.git.add(all=True)
gitrepo.git.commit('-m','[INITIAL]Swagger codegen from digikey swagger specification')
assert len(gitrepo.untracked_files)==0

logging.info('---- COMPLETE Code Version control under GIT -------------------------------')
