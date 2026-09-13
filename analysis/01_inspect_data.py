from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


csv_path = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "raw"
    / "MetroPT3(AirCompressor).csv"
)

df = pd.read_csv(csv_path, nrows=10_000)

print("데이터 크기:", df.shape)

print("\n컬럼 목록")
print(df.columns.tolist())

print("\n처음 5행")
print(df.head())

print("\n데이터 정보")
df.info()

print("\n센서별 기초 통계")
print(df.describe())

# print("\n누락된 값")
# print(df.isna().sum())

print("\n값의 분포")
print(df["Motor_current"].describe())

# ===============================================
# 모터에 전류가 흐르는 상태로 운행 상태 확인 (운전 중 / 정지 라벨이 없음)
# ===============================================

# 최댓값, 최솟값이 pdf와 동일하게 0~10 사이에 분포하는지 확인
# 약 0 A → 모터가 꺼져 있음
# 약 4 A → 무부하 운전
# 약 7 A → 부하 운전
# 약 9 A → 모터가 기동할 때

# min_current = None
# max_current = None

# for chunk in pd.read_csv(csv_path, chunksize=10_000):
#   chunk_min = chunk["Motor_current"].min()
#   chunk_max = chunk["Motor_current"].max()

#   if min_current is None or min_current > chunk_min : 
#     min_current = chunk_min

#   if max_current is None or max_current < chunk_max :
#     max_current = chunk_max

# print("\n최댓값, 최솟값")
# print(max_current, min_current)

# 모터 값 분포 히스토그램 확인
# 문서상 정지 상태가 약 0A, 무부하 운전은 약 4A 
# => 몇 A 이상부터 “모터가 실제로 운전 중”이라고 판단할지 값의 분포를 통해 확인

# df["Motor_current"].hist()
# plt.show()

# 첫 10,000행에서는 1~3A 구간이 거의 비어 있는 것으로 보였음
# 전체 데이터에서도 동일한지 확인

cnt = 0
for chunk in pd.read_csv(csv_path, chunksize=10_000):
  condition = (chunk["Motor_current"] > 1) & (chunk["Motor_current"] < 3)
  cnt += condition.sum()
    
print("\n1A ~ 3A 사이의 motor_current개수")
print(cnt)

# 209개 있음. list에 담자

# values_1to3 = []
# for chunk in pd.read_csv(csv_path, chunksize=10_000):
#   condition = (chunk["Motor_current"] > 1) & (chunk["Motor_current"] < 3)
#   values_1to3.extend(chunk.loc[condition, "Motor_current"])

# 히스토그램으로 다시 확인
# plt.hist(values_1to3)
# plt.show()

# 전체 데이터에서는 1~3A 구간의 값이 209개 존재
# 해당 값들이 어떤 상황에서 발생하는지 시간 흐름을 확인

# 첫 번째 true 부분을 찾아서 근처의 데이터를 보고 튀는 값이 있는지 확인
# (정지 -> 운행중으로 바뀔 때의 특징이 있는지 보기 위해)

# cnt = 0
# for chunk in pd.read_csv(csv_path, chunksize=10_000):
#   condition = (chunk["Motor_current"] > 1) & (chunk["Motor_current"] < 3)

#   if condition.any():
#     for i, v in enumerate(condition):
#       if(v):
#         cnt = cnt + 1
#         #  결과값, 근처 데이터 확인
#         print(chunk.index[i])
#         print(chunk.loc[chunk.index[i-3]:chunk.index[i+3], ["timestamp", "Motor_current"]])
#         print("\n")
#       if cnt >= 5:
#         break
#     if cnt >= 5:
#       break

# 전체 209개 중 최초 5개를 확인한 결과 모두 3A 이상 → 1~3A → 1A 이하 패턴

# 전체 패턴 확인
# cnt = 0
# for chunk in pd.read_csv(csv_path, chunksize=10_000):
#   condition = (chunk["Motor_current"] > 1) & (chunk["Motor_current"] < 3)

#   if condition.any():
#     for i, v in enumerate(condition):
#       if( v
#           and chunk["Motor_current"].iloc[i - 1] >= 3
#           and chunk["Motor_current"].iloc[i + 1] <= 1):
#         cnt = cnt + 1

# print("\n3A 이상 → 1~3A → 1A 이하 패턴의 개수")
# print(cnt)
# print("\n")

# cnt = 0

# prev_last = None
# pending_last = None

# for chunk in pd.read_csv(csv_path, chunksize=10_000):
#     motor = chunk["Motor_current"].reset_index(drop=True)

#     # 이전 chunk의 마지막 값 검사
#     if pending_last is not None:
#         current = pending_last
#         previous = prev_last
#         next_value = motor.iloc[0]

#         if (
#             1 < current < 3
#             and previous >= 3
#             and next_value <= 1
#         ):
#             cnt += 1

#     # 현재 chunk 내부 검사
#     for i in range(len(motor)):
#         current = motor.iloc[i]

#         if not (1 < current < 3):
#             continue

#         # 첫 번째 행
#         if i == 0:
#             if prev_last is None:
#                 continue

#             previous = prev_last
#             next_value = motor.iloc[i + 1]

#         # 마지막 행은 다음 chunk가 필요하므로 보류
#         elif i == len(motor) - 1:
#             continue

#         # 일반적인 경우
#         else:
#             previous = motor.iloc[i - 1]
#             next_value = motor.iloc[i + 1]

#         if previous >= 3 and next_value <= 1:
#             cnt += 1

#     # 다음 chunk를 위해 마지막 두 값 기억
#     if len(motor) >= 2:
#         prev_last = motor.iloc[-2]
#         pending_last = motor.iloc[-1]

# print("\n3A 이상 → 1~3A → 1A 이하 패턴의 개수")
# print(cnt)

# 1~3A 값 209개 중 187개가
# 3A 이상 → 1~3A → 1A 이하 패턴에 해당
# chunksize 경계까지 고려해도 결과는 187개로 동일
# 나머지 22개의 패턴은 추가 확인 필요

# 1~3A 값 중 기존 패턴에 해당하지 않는 22개 확인

cnt = 0

prev_last = None
pending_last = None

exception_count = 0

for chunk in pd.read_csv(csv_path, chunksize=10_000):
    motor = chunk["Motor_current"].reset_index(drop=True)

    # 이전 chunk의 마지막 값 검사
    if pending_last is not None:
        current = pending_last
        previous = prev_last
        next_value = motor.iloc[0]

        if 1 < current < 3:
            if not (previous >= 3 and next_value <= 1):
                print(previous, current, next_value)
                exception_count += 1

    # 현재 chunk 내부 검사
    for i in range(len(motor)):
        current = motor.iloc[i]

        if not (1 < current < 3):
            continue

        # 첫 번째 행
        if i == 0:
            if prev_last is None:
                continue

            previous = prev_last
            next_value = motor.iloc[i + 1]

        # 마지막 행은 다음 chunk가 필요하므로 보류
        elif i == len(motor) - 1:
            continue

        # 일반적인 경우
        else:
            previous = motor.iloc[i - 1]
            next_value = motor.iloc[i + 1]

        if not (previous >= 3 and next_value <= 1):
            print(previous, current, next_value)
            exception_count += 1

    # 다음 chunk를 위해 마지막 두 값 기억
    if len(motor) >= 2:
        prev_last = motor.iloc[-2]
        pending_last = motor.iloc[-1]

print("\n예외 패턴 개수")
print(exception_count)

# ===============================================
# Motor_current 기반 운전 상태 분석 메모
# ===============================================
# 목표: 운전/정지 라벨이 없어 Motor_current로 설비 운전 이력을 추정
#
# 임시 기준
# - 정지: <= 1A
# - 운전: >= 3A
# - 중간값: 1A < current < 3A
#
# 전체 데이터에서 1~3A 값은 209개
# - 187개: >=3A → 1~3A → <=1A (운전 → 정지 후보)
# - 나머지 22개:
#   - <=1A → 1~3A → >=3A 형태의 기동 후보 다수
#   - >=3A → 1~3A → >=3A 형태의 일시적 전류 하락도 존재
#
# 의문점:
# 종료 후보(187개)에 비해 기동 후보가 너무 적음.
# => 기동 시 1~3A를 거치지 않고 <=1A → >=3A로 바로 변하는 경우가 있을 수 있음.
#
# TODO:
# 1. 전체 시계열에서 <=1A → >=3A START 후보 추출
# 2. >=3A → <=1A STOP 후보 추출
# 3. START/STOP 개수 비교
# 4. 시간순으로 START → STOP → START → STOP 형태로 번갈아 나오는지 확인
# 5. 결과를 바탕으로 operation cycle 생성 규칙 확정