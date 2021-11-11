"""A script to build the C++ code via Cython.

For building only, the user should not be at
the entry point of the project. It should be
in the folder containing the file "setup.py".

Type:
$ python setup.py build_ext --inplace

"""

import numpy
import os
from Cython.Build import cythonize
from distutils.core import setup, Extension
# from distutils.extension import Extension

if __name__ == '__main__':
    path_to_cplusplus = '/kaggle/temp/Autoencoder/kodak_tensorflow/lossless/c++/source/'
    sources = [
        '/kaggle/temp/Autoencoder/kodak_tensorflow/lossless/interface_cython.pyx',
        os.path.join(path_to_cplusplus, 'utils.cpp'),
        os.path.join(path_to_cplusplus, 'Bitstream.cpp'),
        os.path.join(path_to_cplusplus, 'BinaryArithmeticCoder.cpp'),
        os.path.join(path_to_cplusplus, 'LosslessCoder.cpp'),
        os.path.join(path_to_cplusplus, 'compression.cpp')
    ]
    ext = Extension('/kaggle/temp/Autoencoder/kodak_tensorflow/lossless/interface_cython.pyx',
                    sources=sources,
                    language='c++',
                    extra_compile_args=['-std=c++11']
                    )
    setup(ext_modules=cythonize(ext),
          include_dirs=[numpy.get_include()])


# sdfsdjnfgjf