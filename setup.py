from decimal import ExtendedContext
from distutils.core import setup, Extension

module_spam = Extension('spam', sources = ['spammodule.c']) 

setup(
    name='2018180010_Script_Project',
    version= '1.0',

    py_modules=['Project_main_Final'],

    packages=['image'],
    package_data={'image':['*.png']},
    
    ext_modules=[module_spam]
)