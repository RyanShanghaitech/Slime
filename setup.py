from setuptools import setup, Extension
import numpy

_sources = \
[
    './mrphantom_src/ext/main.cpp',
    './mrphantom_src/ext/slime.cpp',
]

modExt = Extension\
(
    "mrphantom.ext", 
    sources = _sources,
    include_dirs = ["./mrphantom_src/ext/", numpy.get_include()],
    language = 'c++',
    extra_compile_args = ["-O3", "-fopenmp"],
    extra_link_args = ["-fopenmp"],
)

_packages = \
[
    "mrphantom", 
    "mrphantom.ext",
]

_package_dir = \
{
    "mrphantom":"./mrphantom_src/", 
    "mrphantom.ext":"./mrphantom_src/ext/",
}

setup\
(
    name = 'mrphantom',
    ext_modules = [modExt],
    packages = _packages,
    package_dir = _package_dir,
    include_package_data = True
)
