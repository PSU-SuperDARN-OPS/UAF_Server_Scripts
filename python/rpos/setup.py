from distutils.core import setup, Extension
import os
rst = os.environ['RSTPATH']

setup (name = "pyrpos",
       version = "1.0",
       description = "rpos interface",
       author = "Jef Spaleta",
       author_email = "jspaleta@gi.alaska.edu",
       url = "http://gi.alaska.edu",
       long_description =
"""The pyrpos module provides a python wrapper over rpos.
""",

       ext_modules = [Extension("pyrpos",
                                sources=["pyrpos.c"],
                                include_dirs = [
                                     rst+"/include/general/",
                                     rst+"/include/base/",
                                     rst+"/include/superdarn"],
                                library_dirs = [
                                     rst+"/lib/"],
				libraries=["rpos.1","rtime.1","radar.1","igrf.1","aacgm.1","dmap.1","rcnv.1"]),]
       )


