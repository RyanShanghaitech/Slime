from setuptools import setup, Extension
import numpy
import sys

_sources = \
[
    './slime_src/ext/main.cpp',
    './slime_src/ext/slime.cpp',
]

extra_compile_args = []
extra_link_args = []

if sys.platform.startswith("win"):
    # MSVC
    extra_compile_args += ["/O2", "/openmp"]
    # usually no extra_link_args needed
elif sys.platform == "darwin":
    # macOS clang: OpenMP is not enabled by default; uses libomp
    extra_compile_args += ["-O3", "-Xpreprocessor", "-fopenmp"]
    extra_link_args += ["-lomp"]
else:
    # Linux (gcc/clang)
    extra_compile_args += ["-O3", "-fopenmp"]
    extra_link_args += ["-fopenmp"]

modExt = Extension\
(
    "slime.ext", 
    sources = _sources,
    include_dirs = ["./slime_src/ext/", numpy.get_include()],
    language = 'c++',
    extra_compile_args=extra_compile_args,
    extra_link_args=extra_link_args,
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
    # install_requires = ["numpy", "matplotlib"], # pip will automatically upgrade numpy if it see this, which might corrupt the environment
    ext_modules = [modExt],
    packages = _packages,
    package_dir = _package_dir,
    include_package_data = True
)
