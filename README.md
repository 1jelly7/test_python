# 개발 환경

## 소프트웨어 버전

| 항목 | 버전 |
| :---: | :---: |
| CUDA | 13.2 |

1. 아래 파일을 연다.
.../Lib/site-packages/pandas_datareader/compat/__init__.py
2. 첫 줄 근처의 import를 아래처럼 바꾼다.
from distutils.version import LooseVersion -> from packaging.version import Version as LooseVersion
3. 아래 파일을 연다.
.../Lib/site-packages/pandas_datareader/data.py
4. 273줄 근처를 아래처럼 바꾼다.
@deprecate_kwarg("access_key", "api_key") -> @deprecate_kwarg(klass=DeprecationWarning, old_arg_name="access_key", new_arg_name="api_key")

## OpenJDK 환경변수 설정

### 1. OpenJDK 다운로드
https://jdk.java.net/archive/ 에서 필요한 버전의 OpenJDK를 다운로드한다.
예: `21.0.2` 

### 2. 설치 경로 확인
예시 경로:
- `C:\Program Files\Java\jdk-21.0.2`

압축을 푼 OpenJDK의 최상위 폴더 경로를 확인한다.

### 3. 환경 변수에 추가

#### 3-1. JAVA_HOME 등록
1. 시작 메뉴에서 `시스템 환경 변수 편집`을 연다.
2. `환경 변수` 버튼을 클릭한다.
3. 시스템 변수에서 `새로 만들기`를 클릭한다.
4. 변수 이름에 `JAVA_HOME`을 입력한다.
5. 변수 값에 JDK 설치 경로를 입력한다.
6. `확인` 버튼을 클릭해 창을 닫는다.

#### 3-2. Path에 추가
1. 시스템 변수에서 `Path`를 선택하고 `편집` 버튼을 클릭한다.
2. `새로 만들기`를 클릭한다.
3. `%JAVA_HOME%\bin`을 추가한다.
4. `확인` 버튼을 클릭해 모든 창을 닫는다.

### 4. 설치 확인
명령 프롬프트에서 아래 명령을 실행한다.
```
java -version
javac -version
echo %JAVA_HOME%
```
버전 정보가 출력되면 설정이 정상이다.
