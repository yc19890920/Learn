from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
from Cython.Distutils import build_ext
import Cython.Compiler
import os


files_path = "soso/*.py"



def to_so():
    try:
        ext_modules = [Extension('*', [files_path],)]
        setup(
            name="py to so",
            cmdclass={'build_ext': build_ext},
            ext_modules=cythonize(ext_modules)
        )
    except Cython.Compiler.Errors.CompileError as e:
        # 捕获异常，从报错信息的最后一行获取文件名并格式化
        filename = str(e).split('\n')[-1]
        os.popen(
            'autopep8 --in-place --aggressive --aggressive ' +
            os.getcwd() +
            "/" +
            filename)
        # 继续转换
        to_so()

to_so()
