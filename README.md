1. 아래 파일을 연다.
.../Lib/site-packages/pandas_datareader/compat/__init__.py
2. 첫 줄 근처의 import를 아래처럼 바꾼다.
from distutils.version import LooseVersion -> from packaging.version import Version as LooseVersion
3. 아래 파일을 연다.
.../Lib/site-packages/pandas_datareader/data.py
4. 273줄 근처를 아래처럼 바꾼다.
@deprecate_kwarg("access_key", "api_key") -> @deprecate_kwarg(klass=DeprecationWarning, old_arg_name="access_key", new_arg_name="api_key")
