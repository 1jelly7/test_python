"""
pandas 초보자용 종합 정리

이 파일은 여러 pandas 학습 코드를 한 파일로 합치고,
초보자가 읽기 쉽도록 설명 주석을 충분히 추가한 버전입니다.

학습 순서
2) DataFrame 기본
3) loc / iloc 인덱싱
4) 인덱스 조작
5) 정렬 / 집계 / apply / 결측치 / 범주화
6) 파일 입출력
7) 시계열 데이터
8) 외부 데이터 조회 예시

주의
- print() 결과를 직접 보면서 공부하는 용도로 작성되었습니다.
- 일부 파일 입출력 예시는 실제 파일이 없으면 실행하지 않고, 예시 코드만 보여줍니다.
- pandas_datareader 예시는 설치 환경에 따라 실행이 안 될 수 있어서 예시만 제공합니다.
"""

import datetime as dt
import numpy as np
import pandas as pd

# --------------------------------------------------
# 4. 인덱스 조작
# --------------------------------------------------
def demo_index_manipulation():
    np.random.seed(0)

    # set_index()는 기존 열 하나를 행 인덱스로 바꿉니다.
    df1 = pd.DataFrame(
        np.vstack([list("ABCDE"), np.round(np.random.rand(3, 5), 2)]).T,
        columns=["C1", "C2", "C3", "C4"],
    )
    print("[4-1] 원본 DataFrame")
    print(df1)

    df2 = df1.set_index("C1")
    print("\n[4-2] set_index('C1')")
    print(df2)

    # reset_index()는 인덱스를 다시 일반 열로 되돌립니다.
    print("\n[4-3] reset_index()")
    print(df2.reset_index())

    # drop=True를 주면 기존 인덱스를 일반 열로 되돌리지 않고 버립니다.
    print("\n[4-4] reset_index(drop=True)")
    print(df2.reset_index(drop=True))

    # 다중 인덱스(MultiIndex)는 행 또는 열에 계층 구조를 만드는 기능입니다.
    print("\n[4-5] 다중 컬럼 인덱스")
    df3 = pd.DataFrame(
        np.round(np.random.randn(5, 4), 2),
        columns=[["A", "A", "B", "B"], ["C1", "C2", "C3", "C4"]],
    )
    df3.columns.names = ["Cidx1", "Cidx2"]
    print(df3)

    print("\n[4-6] 다중 행/열 인덱스")
    df4 = pd.DataFrame(
        np.round(np.random.randn(6, 4), 2),
        columns=[["A", "A", "B", "B"], ["C1", "C2", "C3", "C4"]],
        index=[["M", "M", "M", "F", "F", "F"], [f"id_{i+1}" for i in range(3)] * 2],
    )
    df4.columns.names = ["Cidx1", "Cidx2"]
    df4.index.names = ["Ridx1", "Ridx2"]
    print(df4)

    # stack(): 열 인덱스를 행 인덱스로 내립니다.
    print("\n[4-7] stack('Cidx1')")
    print(df4.stack("Cidx1"))

    # unstack(): 행 인덱스를 열 인덱스로 올립니다.
    print("\n[4-8] unstack('Ridx2')")
    print(df4.unstack("Ridx2"))


# --------------------------------------------------
# 5. 정렬 / 집계 / apply / 결측치 / 범주화
# --------------------------------------------------
def demo_analysis_functions():
    print("\n" + "=" * 70)
    print("5. 정렬 / 집계 / apply / 결측치 / 범주화")
    print("=" * 70)

    # NaN은 결측값(값이 비어 있음)을 의미합니다.
    s = pd.Series(range(10), dtype=float)
    s[3] = np.nan

    print("[5-1] count(): NaN 제외 개수 세기")
    print(s)
    print("count =", s.count())

    np.random.seed(0)
    df = pd.DataFrame(np.random.randint(5, size=(4, 4)), dtype=float)
    df.iloc[2, 3] = np.nan

    print("\n[5-2] DataFrame의 count(): 열별 개수")
    print(df)
    print(df.count())

    np.random.seed(1)
    s2 = pd.Series(np.random.randint(6, size=100))

    # value_counts()는 각 값이 몇 번 등장했는지 세어 줍니다.
    print("\n[5-3] value_counts()")
    print(s2.value_counts())

    # sort_index()는 인덱스 기준 정렬입니다.
    print("\n[5-4] sort_index()")
    print(s2.value_counts().sort_index())

    # sort_values()는 값 기준 정렬입니다.
    print("\n[5-5] sort_values()")
    print(s.sort_values())
    print(s.sort_values(ascending=False))
    print(df.sort_values(by=2))

    np.random.seed(1)
    df2 = pd.DataFrame(np.random.randint(10, size=(4, 8)))
    print("\n[5-6] sum(): 합계 구하기")
    print(df2)

    # axis=1은 행 방향 계산입니다.
    print("행별 합계")
    print(df2.sum(axis=1))

    # 계산 결과를 새 열로 추가할 수 있습니다.
    df2["RowSum"] = df2.sum(axis=1)
    print("\nRowSum 열 추가")
    print(df2)

    # 새 행도 추가할 수 있습니다.
    df2.loc["colTotal", :] = df2.sum()
    print("\n합계 행 추가")
    print(df2)

    # apply()는 행 또는 열 단위로 사용자 정의 함수를 적용할 때 자주 사용합니다.
    df3 = pd.DataFrame({
        "A": [1, 3, 1, 3, 4],
        "B": [2, 3, 1, 2, 3],
        "C": [1, 3, 2, 4, 4],
    })

    print("\n[5-7] apply()")
    print(df3)

    print("열별 max - min")
    print(df3.apply(lambda x: x.max() - x.min()))

    print("\n행별 max - min")
    print(df3.apply(lambda x: x.max() - x.min(), axis=1))

    print("\n각 열의 값 빈도표")
    freq_table = df3.apply(lambda x: x.value_counts(), axis=0)
    print(freq_table)

    # fillna()는 NaN을 원하는 값으로 채웁니다.
    print("\n[5-8] fillna() + astype()")
    print(freq_table.fillna(0.0).astype(int))

    # cut()은 숫자 데이터를 구간으로 나누어 범주형 데이터로 바꿉니다.
    print("\n[5-9] cut(): 연속형 데이터 -> 범주형 데이터")
    ages = [0, 2, 10, 21, 23, 37, 31, 61, 20, 41, 32, 101]
    bins = [1, 20, 30, 50, 70, 100]
    labels = ["미성년자", "청년", "중년", "장년", "노년"]
    result = pd.cut(ages, bins=bins, labels=labels)
    print(result)
    print("categories:", result.categories)
    print("codes:", result.codes)

    df4 = pd.DataFrame({"age": ages})
    df4["age_category"] = pd.cut(ages, bins=bins, labels=labels)
    print("\nDataFrame에 범주형 열 추가")
    print(df4)

# --------------------------------------------------
# 7. 시계열 데이터
# --------------------------------------------------
def demo_timeseries():
    print("\n" + "=" * 70)
    print("7. 시계열 데이터")
    print("=" * 70)

    # pandas에서 날짜/시간 데이터를 다룰 때는 DatetimeIndex가 중요합니다.
    # 먼저 문자열 날짜를 datetime으로 바꿔 봅니다.
    date_str = ["2024. 1. 4", "2024. 1. 5", "2024. 1. 6"]
    idx = pd.to_datetime(date_str)

    print("[7-1] to_datetime()")
    print(idx)

    # date_range()는 날짜 범위를 자동 생성해 줍니다.
    print("\n[7-2] date_range()")
    print(pd.date_range("2025-04-01", "2025-04-05"))
    print(pd.date_range("2024-12-01", periods=5))
    print(pd.date_range("2019-04-01", "2019-04-30", freq="B"))
    print(pd.date_range("2019-04-01", "2019-04-30", freq="W-MON"))
    print(pd.date_range("2019-04-01", "2019-04-30", freq="MS"))
    print(pd.date_range("2019-04-01", "2019-04-30", freq="ME"))

    # shift()는 데이터를 위/아래로 이동시킬 때 사용합니다.
    np.random.seed(0)
    ts = pd.Series(np.random.randn(4), index=pd.date_range("2023-01-31", periods=4, freq="ME"))
    print("\n[7-3] shift()")
    print(ts)
    print("\n아래로 1칸 이동")
    print(ts.shift(1))
    print("\n위로 1칸 이동")
    print(ts.shift(-1))
    print("\n인덱스도 함께 한 달 뒤로 이동")
    print(ts.shift(1, freq="ME"))

    # resample()은 시간 간격을 다시 조정하는 기능입니다.
    # 예: 일별 데이터를 주별 평균으로 바꾸기
    ts2 = pd.Series(np.random.randn(100), index=pd.date_range("2023-01-01", periods=100, freq="D"))
    print("\n[7-4] resample() - 다운샘플링")
    print(ts2.resample("W").mean().head())
    print(ts2.resample("MS").first().head())

    # 분 단위 데이터 예시
    ts3 = pd.Series(np.random.randn(60), index=pd.date_range("2024-01-01", periods=60, freq="min"))
    print("\n[7-5] resample() - 분 단위 집계")
    print(ts3.resample("10min").sum().head())
    print(ts3.resample("10min", closed="right").sum().head())

    # ohlc()는 금융 데이터처럼 시가/고가/저가/종가를 볼 때 많이 씁니다.
    print("\n[7-6] ohlc()")
    print(ts3.resample("5min").ohlc().head())

    # 업샘플링은 없는 시점을 새로 만들어야 해서 채우기 방식이 필요합니다.
    print("\n[7-7] 업샘플링: ffill / bfill")
    print(ts3.resample("30s").ffill().head(10))
    print(ts3.resample("30s").bfill().head(10))

    # dt 접근자는 datetime Series에서 년/월/일/요일 등을 쉽게 뽑아낼 때 사용합니다.
    s = pd.Series(pd.date_range("2024-12-25", periods=5, freq="D"))
    print("\n[7-8] dt 접근자")
    print(s.dt.year)
    print(s.dt.weekday)
    print(s.dt.strftime("%Y년 %m월 %d일"))


# --------------------------------------------------
# 8. 외부 데이터 조회 예시
# --------------------------------------------------
def demo_external_data_example():
    print("\n" + "=" * 70)
    print("8. 외부 데이터 조회 예시")
    print("=" * 70)

    # pandas_datareader는 외부 경제/금융 데이터를 불러올 때 사용할 수 있습니다.
    # 다만 별도 설치가 필요할 수 있고, 파이썬 버전에 따라 환경 이슈가 생길 수 있습니다.
    print("[8-1] pandas_datareader 예시 코드")
    print("import pandas_datareader as pdr")
    print("start = dt.datetime(2025, 1, 1)")
    print("end = dt.datetime(2026, 4, 30)")
    print("gdp = pdr.get_data_fred('GDP', start=start, end=end)")
    print("inflation = pdr.get_data_fred(['CPIAUCSL', 'CPILFESL'], start=start, end=end)")
    print("※ 실행 전 pandas_datareader 설치 여부를 확인하세요.")
