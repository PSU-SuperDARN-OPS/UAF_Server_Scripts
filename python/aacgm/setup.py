from distutils.core import setup, Extension
import os
rst = os.environ['RSTPATH']
setup (name = "pyaacgm",
       version = "1.0",
       description = "aacgm interface",
       author = "Jef Spaleta",
       author_email = "jspaleta@gi.alaska.edu",
       url = "http://gi.alaska.edu",
       long_description =
"""The pyaacgm module provides a python wrapper over aacgm.
""",

       ext_modules = [Extension("pyaacgm",
                                sources=["pyaacgm.c"],
                                include_dirs = [
                                     rst+"/include/analysis/",
                                     rst+"/include/superdarn"],
                                library_dirs = [
                                     rst+"/lib/"],
				libraries=["aacgm.1"]),]
       )


