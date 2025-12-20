from setuptools import setup, Extension
import numpy

_sources = \
[
    './slime_src/ext/main.cpp',
    './slime_src/ext/slime.cpp',
]

modExt = Extension\
(
    "slime.ext", 
    sources = _sources,
    include_dirs = ["./slime_src/ext/", numpy.get_include()],
    language = 'c++',
    extra_compile_args = ["-O3", "-fopenmp"],
    extra_link_args = ["-fopenmp"],
)

_packages = \
[
    "slime", 
    "slime.ext",
]

_package_dir = \
{
    "slime":"./slime_src/", 
    "slime.ext":"./slime_src/ext/",
}

setup\
(
    name = 'slime',
    ext_modules = [modExt],
    packages = _packages,
    package_dir = _package_dir,
    include_package_data = True
)
