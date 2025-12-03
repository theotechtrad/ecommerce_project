# setup.py
from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy

extensions = [
    Extension(
        "shop.similarity_calc",
        ["shop/similarity_calc.pyx"],
        include_dirs=[numpy.get_include()],
    )
]

setup(
    name='ecommerce_recommendation',
    ext_modules=cythonize(extensions, compiler_directives={'language_level': "3"}),
    include_dirs=[numpy.get_include()]
)