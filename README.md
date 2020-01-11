# community-digikey-api-build-python-client
---------
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=ZHPF7ZLDCYEYY&source=url)

A community initiative to automatically create  python clients for the Digikey set of API's 
this application automates for the following API's.

    COMPLETED: productinformation
    COMPLETED: ordersupport
    TODO:barcode
    TODO:Ordering

As they are all specified individually they are generated into individual projects and thus individual python module names. This project, the builder,  generates  all the api projects.

The Digikey API specification in Swagger.json format is the basis of the generated python clients for each api
The generation for each API is done by using the Swagger Codegen, a java application.

When this package is installed its only purpose is to perform the fresh CodeGens of each api and then install them. At present they are installed in an editable manner

The platform prerequisites are java and for python the package requirement is gitpython

------------
## IF THIS WORK BENEFITS YOU in a way that you can contribute to my time in supporting Open Source Community Benefiting Software then please contribute here. 

# Any donations are always graciously accepted

[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=ZHPF7ZLDCYEYY&source=url)

---------------------


## Versions
- DIGIKEY API version: v3
- Build Package version: 0.1.0

## Requirements.

Python 3.4+
Python Package GitPython
Java 1.8+

## Installation & Usage

`pip install -e .`

If the python package is hosted on Github, you can install directly from Github

```sh
pip install -e git+https://github.com/auphofBSF/community-digikey-api-build-python-client.git
```
(you may need to run `pip` with root permission: `sudo pip install -e git+https://github.com/auphofBSF/community-digikey-api-build-python-client.git`

