from distutils.core import setup, Extension

setup (name = "pydarn",
       version = "0.1",
       description = "python bindings for SuperDARN RST",
       author = "Jef Spaleta",
       author_email = "jspaleta@gi.alaska.edu",
       url = "http://www.fedorhosted.org/pydarn",
       long_description =
"""The pydmap module provides functions to interact with dmap based files and is part of the collection of python tools for working with the SuperDARN datasets and C language based RST and ROS codebase.  
""",
       classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: (BSD)',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: System :: Science'
       ],

       ext_modules = [Extension("dmap",
                                sources=["pydmap.c"],
                                include_dirs = [
                                     "/opt/radar/include/general/",
                                     "/opt/radar/include/base/",
                                     "/opt/radar/include/superdarn"],
                                library_dirs = [
                                     "/opt/radar/lib/"],
				libraries=["m","z","oldfit.1","fit.1","rscan.1",
                                           "radar.1","dmap.1","rtime.1",
                                           "rcnv.1"]),]
       )

