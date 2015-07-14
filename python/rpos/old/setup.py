from distutils.core import setup, Extension

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
                                     "/opt/radar/include/general/",
                                     "/opt/radar/include/base/",
                                     "/opt/radar/include/superdarn"],
                                library_dirs = [
                                     "/opt/radar/lib/"],
				libraries=["rpos.1","rtime.1","radar.1","igrf.1","aacgm.1"]),]
       )


