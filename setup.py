from decimal import ExtendedContext
from distutils.core import setup, Extension

module_spam = Extension('spam', sources = ['spammodule.c']) 

setup(
    name='project_main_ver.2.py',
    version= '1.0',

    py_modules=['project_main_ver.2'],

    #packages=['image'],
    #package_data={'image':['*.gif']},
    
    ext_modules=[module_spam]
)