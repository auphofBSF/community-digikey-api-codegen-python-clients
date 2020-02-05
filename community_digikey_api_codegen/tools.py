'''
A community initiative to automatically create the python client for the Digikey set of API's 
this application customizes and automates the Swagger CodeGen for the following API's 
    COMPLETED: productinformation
    COMPLETED: ordersupport
    TODO:barcode
    TODO:Ordering

The Digikey API specification in Swagger.json format is the basis of the generated python clients
The generation is done by using the Swagger Codegen, a java application.


The platform prerequisites are java and python the package are gitpython


'''


import logging
logging.basicConfig(level=logging.INFO)

import os
import configparser
config = configparser.ConfigParser()
logging.debug("------------------------------tools.py File directory is:{}".format(os.path.realpath(__file__)))
config['custom'] = {
    'DEST_PATH': os.path.realpath(os.path.expanduser(
    os.path.join(os.path.dirname( __file__ ), '..','..'))
    )
    , 'TMP_PATH': os.path.realpath(os.path.expanduser(
    os.path.join(os.path.dirname( __file__ ), '..','.tmp'))
    )
    }
if not os.path.exists(".env/config.ini"):
    if not os.path.exists(".env"):
        os.mkdir(".env")
    with open(".env/config.ini",'w') as f:
        config.write(f)

config.read(os.path.join('.env','config.ini'))
DEST_PATH = config['custom']['DEST_PATH']
TMP_PATH = config['custom']['TMP_PATH']
logging.debug("config.ini - DEST_PATH:{}".format(DEST_PATH))
logging.debug("config.ini - TMP_PATH:{}".format(TMP_PATH))


import zipfile, subprocess, shutil
import sys,requests
import git
import json
import re


logging.debug("CodeGen Digikey API Clients: module: tools.py is loading ......")
logging.debug("CodeGen Directory for Digikey API's: {tmpDir}".format(tmpDir=TMP_PATH))

envExecuteRoot = os.getcwd()

if not os.path.exists(TMP_PATH):
    os.makedirs(TMP_PATH)
os.chdir(TMP_PATH)

swaggerCodeGenURL = 'https://repo1.maven.org/maven2/io/swagger/swagger-codegen-cli/2.4.10/swagger-codegen-cli-2.4.10.jar'
_, swagger_codegen_cli_version_jar = os.path.split(swaggerCodeGenURL)

swaggerCodeGen_config_all = {
    'product-information':{
            "packageName" : "digikey_productinformation",
            "projectName" : "community-digikey-api-productinformation",
            "packageVersion" : "0.1.0",
            "packageUrl" : "https://github.com/auphofBSF/community-digikey-api-productinformation.git",
    }
    , 'order-support':{
            "packageName" : "digikey_ordersupport",
            "projectName" : "community-digikey-api-ordersupport",
            "packageVersion" : "0.1.0",
            "packageUrl" : "https://github.com/auphofBSF/community-digikey-api-ordersupport.git",
    }
}

digikeyAPIdef_all = {
            'product-information':
                dict(apiGroup='product-information'
                    ,apiSubGroup = 'partsearch'
                    ,apiQuery='productdetails'
                    ,urlNode='432'
                    )
            , 'order-support':
                dict(apiGroup='order-support'
                    ,apiSubGroup = 'orderdetails'
                    ,apiQuery='orderhistory'
                    ,urlNode='480'
                    )

}


def getDigikeyAPIswaggerSpecJSON(destPath,**kwargs):
    # refererURL='https://developer.digikey.com/products/product-information/partsearch/productdetails?prod=true'
    refererURL='https://developer.digikey.com/products/{apiGroup}/{apiSubGroup}/{apiQuery}?prod=true'.format(**kwargs)
    url = 'https://developer.digikey.com/node/{urlNode}/oas-download'.format(**kwargs)
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



def wget(fileName,url):
    r = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        })

    with open(fileName, 'wb') as f:
        f.write(r.content)




def codeGen_api(digikeyAPIdef, swaggerCodeGen_config):
    logging.info('CodeGen Automation STARTING for  {apiGroup}------------------------------------'.format(**digikeyAPIdef))

    if not os.path.exists(TMP_PATH):
        logging.info('making TMP directory:  {}------------------------------------'.format(TMP_PATH))
        os.mkdir(TMP_PATH)
    #download the SWAGGER.JSON for the required DIGIKEY API
    swaggerSpecFile=getDigikeyAPIswaggerSpecJSON(TMP_PATH, **digikeyAPIdef)

    #setup the CONFIG file
    configFile_swaggerCodegen='{projectName}-config-SwaggerCodegen.json'.format(**swaggerCodeGen_config)
    with open(configFile_swaggerCodegen, 'w') as outfile:
        json.dump(swaggerCodeGen_config, outfile)

    logging.info("Created config file for Swagger Codegen: {}".format(configFile_swaggerCodegen))

    #check if the swagger-codgen is present, else download
    if os.path.isfile(swagger_codegen_cli_version_jar):
        logging.info(f"Swagger-CodeGen: {swagger_codegen_cli_version_jar} already exists, no download required")
    else:
        try:
            url = swaggerCodeGenURL
            wget(swagger_codegen_cli_version_jar , url)
            logging.info(f"Swagger-CodeGen : {swagger_codegen_cli_version_jar} downloaded from: {url}")
        except Exception as e:
            logging.critical(f"Unable to download swaggerCodegen from {url} :exception: {e}")

    # execute swagger-codegen
    # Check Java is installed
    try:
        version = subprocess.check_output(['java', '-version'], stderr=subprocess.STDOUT).decode('utf-8')
        patternJavaVersion = '\"(\d+\.\d+).*\"'
        logging.info("Java exists, version: {}".format(re.search(patternJavaVersion, version).groups()[0]))
    except:
        logging.critical("Java existence cannot be confirmed -------------------")

    # Do CodeGen
    codeGenRunCommand = [
        'java'
        , '-jar'
        , swagger_codegen_cli_version_jar
        , 'generate'
        , '--input-spec',  swaggerSpecFile
        , '-l', 'python'
        , '--output', os.path.join(DEST_PATH,'{projectName}'.format(**swaggerCodeGen_config))
        , '--config', configFile_swaggerCodegen
        ]

    try:
        logging.info(f"STARTING Code generator:{swagger_codegen_cli_version_jar} for a Swagger API created, project name: {swaggerCodeGen_config['projectName']}")
        procCall = subprocess.run(codeGenRunCommand,stdout=subprocess.PIPE,stderr=subprocess.PIPE) #, shell=True)
        logging.info(f"COMPLETED Code generator for a Swagger API created, project name: {swaggerCodeGen_config['projectName']}")
        logging.debug('----- STDOUT = \n{}'.format(procCall.stdout.decode('utf-8')))
        logging.debug('----- STDERR = \n{}'.format(procCall.stderr.decode('utf-8')))
        if procCall.returncode != 0:
            message="Failure performing Swagger Codegen: Return Code:{}".format(procCall.returncode)
            logging.critical(message)
            logging.critical('----- STDOUT = \n{}'.format(procCall.stdout.decode('utf-8')))
            logging.critical('----- STDERR = \n{}'.format(procCall.stderr.decode('utf-8')))
 
            raise Exception(message)

    except Exception as e:
        logging.critical("Failure performing Swagger Codegen: Exception:{}".format(e))
        raise Exception("Failure performing Swagger Codegen: Exception:{}".format(e))


    try:
        # Copy Codgen Config, swagger spec and codegen Run command into swagger folder
        codegenDestPath = os.path.join(DEST_PATH,'{projectName}'.format(**swaggerCodeGen_config),'.codegen-config')
        if not os.path.exists(codegenDestPath):
            os.makedirs(codegenDestPath)

        def overwriteCopy(srcFile,dstPath):
            dstFullFilePath=os.path.join(dstPath,os.path.basename(srcFile))
            if os.path.exists(dstFullFilePath):
                os.remove(dstFullFilePath)
            try:
                shutil.copy(srcFile,dst=dstPath)
            except Exception as e:
                message='Failed to copy src:{} to destPath{} result Exception:{}'.format(srcFile,dstPath,e)
                logging.critical(message)
                raise e

        overwriteCopy(configFile_swaggerCodegen,dstPath=codegenDestPath)
        overwriteCopy(swaggerSpecFile,dstPath=codegenDestPath)
        overwriteCopy(__file__, dstPath=codegenDestPath) # Keep a copy of this script that built the client
        logging.info('----- COPIED CodeGen and/or specification files into project')
    except Exception as e:
        message='Failed to copy CodeGen and/or Specification file cause Exception:{}'.format(e)
        logging.critical(message)
        raise Exception(message)



    # GIT initialize the repo and commit #
    logging.info('START Code Version control enabling under GIT')

    #TODO: Check if git already initiated

    try: 
        gitrepo = git.Repo(os.path.join(DEST_PATH,'{projectName}'.format(**swaggerCodeGen_config)))
        logging.info('     Code Version control already a GIT repository')
    except git.InvalidGitRepositoryError:
        gitrepo = git.Repo.init(os.path.join(DEST_PATH,'{projectName}'.format(**swaggerCodeGen_config)))
        logging.info('     Code Version control initialized as a GIT repository')
    if len(gitrepo.untracked_files) > 0:
        gitrepo.git.add(all=True)
        gitrepo.git.commit('-m','[INITIAL]Swagger codegen from digikey swagger specification')
        logging.info('     Code Version control committing changes to GIT repository')
    else:
        logging.info('     Code Version control no changes to commit to GIT repository')
    # assert len(gitrepo.untracked_files)==0

    logging.info('---- COMPLETE Code Version control under GIT -------------------------------')
    logging.info('CodeGen Automation IS NOW COMPLETE for  {apiGroup}------------------------------------'.format(**digikeyAPIdef))
    return({
            'project':swaggerCodeGen_config['projectName'],
            'locationPath': os.path.join(DEST_PATH,'{projectName}'.format(
                                            **swaggerCodeGen_config))
        })


def subprocess_run(subprocessCMD, shell=False):
    """
    Run a subprocess command, passed by dict of arguments. Executes by default with shell=False, and then logging STDOUT and STDERR
    """
    procCall = subprocess.run(subprocessCMD,stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=shell)
    logging.info('----- STDOUT = \n{}'.format(procCall.stdout.decode('utf-8')))
    logging.info('----- STDERR = \n{}'.format(procCall.stderr.decode('utf-8')))
    return procCall
