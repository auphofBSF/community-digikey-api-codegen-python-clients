# community-digikey-api-build-python-client
A community initiative to automatically create  python clients for the Digikey set of API's 
this application automates for the following API's.
    COMPLETED: productinformation
    COMPLETED: ordersupport
    TODO:barcode
    TODO:Ordering

As they are all specified individually they are seperated into seperate projects, this project, the builder,  creates all the api projects.

The Digikey API specification in Swagger.json format is the basis of the generated python clients for each api
The generation is done by using the Swagger Codegen, a java application.

This script then performs a fresh build of the 

The platform prerequisites are java and python the package are gitpython

- API version: v3
- Package version: 0.1.0

## Requirements.

Python 3.4+
Python Package GitPython
Java 1.8+

## Installation & Usage
### pip install

If the python package is hosted on Github, you can install directly from Github

```sh
pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git
```
(you may need to run `pip` with root permission: `sudo pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git`)


TODO: further instructions