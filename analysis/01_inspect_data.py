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

# cnt = 0

# prev_last = None
# pending_last = None

# exception_count = 0

# for chunk in pd.read_csv(csv_path, chunksize=10_000):
#     motor = chunk["Motor_current"].reset_index(drop=True)

#     # 이전 chunk의 마지막 값 검사
#     if pending_last is not None:
#         current = pending_last
#         previous = prev_last
#         next_value = motor.iloc[0]

#         if 1 < current < 3:
#             if not (previous >= 3 and next_value <= 1):
#                 print(previous, current, next_value)
#                 exception_count += 1

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

#         if not (previous >= 3 and next_value <= 1):
#             print(previous, current, next_value)
#             exception_count += 1

#     # 다음 chunk를 위해 마지막 두 값 기억
#     if len(motor) >= 2:
#         prev_last = motor.iloc[-2]
#         pending_last = motor.iloc[-1]

# print("\n예외 패턴 개수")
# print(exception_count)

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

#  0 -> 5 , 5 -> 0 등 중간값 없이 바로 바뀌는 개수 비교,
#  start, stop이 번갈아 나오는지 확인
# start_cnt = 0
# stop_cnt = 0
# events = []

# for chunk in pd.read_csv(csv_path, chunksize=10_000):
#     motor = chunk["Motor_current"].reset_index(drop=True)

#     for i in range(len(motor) - 2):
#         current = motor.iloc[i]
#         next_value = motor.iloc[i + 1]
#         next_next_value = motor.iloc[i + 2]
#         event_added = False
#         # timestamp = chunk["timestamp"].iloc[i + 1] # 05:10:00  0.04   ← 마지막으로 확인된 정지
#         #                                            # 05:10:10  5.40   ← 처음으로 확인된 운전

#         # START 조건
#         if current <= 1:
#             if next_value >= 3:
#                 start_cnt += 1
#                 events.append(("START", chunk["timestamp"].iloc[i + 1]))
#                 event_added = True
#             elif (1 < next_value < 3 and next_next_value >= 3):
#                 start_cnt += 1
#                 events.append(("START", chunk["timestamp"].iloc[i + 2]))
#                 event_added = True
            

#         # STOP 조건
#         elif current >= 3:
#             if next_value <= 1:
#                 stop_cnt += 1
#                 events.append(("STOP", chunk["timestamp"].iloc[i + 1]))
#                 event_added = True
#             elif (3 > next_value > 1 and next_next_value <= 1):
#                 stop_cnt += 1
#                 events.append(("STOP", chunk["timestamp"].iloc[i + 2]))
#                 event_added = True

#         else:
#            continue

#         # 연속된 운행이 감지되면 print
#         if event_added and len(events) >= 2:
#             if events[-2][0] == events[-1][0]:
#                 print(events[-2], events[-1])

# print("START:", start_cnt)
# print("STOP:", stop_cnt)

# 결과
# ('START', '2020-03-19 09:47:14') ('START', '2020-03-19 10:20:47')
# ('START', '2020-04-06 06:01:51') ('START', '2020-04-06 06:27:47')
# ('START', '2020-04-09 01:41:07') ('START', '2020-04-09 04:59:55')
# ('START', '2020-04-29 23:27:16') ('START', '2020-04-29 23:53:03')
# ('STOP', '2020-05-18 01:25:01') ('STOP', '2020-05-18 01:42:41')
# ('STOP', '2020-06-19 01:42:18') ('STOP', '2020-06-19 01:56:20')
# ('STOP', '2020-07-20 06:00:15') ('STOP', '2020-07-20 06:19:35')
# ('START', '2020-08-11 10:19:03') ('START', '2020-08-11 10:43:30')
# ('START', '2020-08-19 07:42:38') ('START', '2020-08-19 08:02:28')
# START: 10376
# STOP: 10203

#  첫 번째 연속된 운행의 범위를 프린트하여 원인 확인
# for chunk in pd.read_csv(csv_path, chunksize=10_000):
#     chunk["timestamp"] = pd.to_datetime(chunk["timestamp"])
#     condition = (
#         (chunk["timestamp"] >= "2020-03-19 09:47:14")
#         & (chunk["timestamp"] <= "2020-03-19 10:20:47")
#     )
#     print(
#         chunk.loc[condition, ["timestamp", "Motor_current"]]
#     )
# => 기존 코드는 청크 경계를 확인하지 않아서 경계에 있는 값을 놓치는 것으로 확인


# 청크 경계도 확인하도록 코드 수정
# start_cnt = 0
# stop_cnt = 0
# events = []

# previous_rows = None

# for chunk in pd.read_csv(csv_path, chunksize=10_000):
    
#     # 이전 chunk의 마지막 2행을 현재 chunk 앞에 붙임
#     if previous_rows is not None:
#         chunk = pd.concat([previous_rows, chunk], ignore_index=True)
#     else:
#         chunk = chunk.reset_index(drop=True)

#     motor = chunk["Motor_current"]

#     for i in range(len(motor) - 2):
#         current = motor.iloc[i]
#         next_value = motor.iloc[i + 1]
#         next_next_value = motor.iloc[i + 2]
#         event_added = False

#         # START 조건
#         if current <= 1:
#             if next_value >= 3:
#                 start_cnt += 1
#                 events.append(("START", chunk["timestamp"].iloc[i + 1]))
#                 event_added = True
#             elif (1 < next_value < 3 and next_next_value >= 3):
#                 start_cnt += 1
#                 events.append(("START", chunk["timestamp"].iloc[i + 2]))
#                 event_added = True
            

#         # STOP 조건
#         elif current >= 3:
#             if next_value <= 1:
#                 stop_cnt += 1
#                 events.append(("STOP", chunk["timestamp"].iloc[i + 1]))
#                 event_added = True
#             elif (3 > next_value > 1 and next_next_value <= 1):
#                 stop_cnt += 1
#                 events.append(("STOP", chunk["timestamp"].iloc[i + 2]))
#                 event_added = True

#         else:
#            continue

#         # 연속된 운행이 감지되면 print
#         if event_added and len(events) >= 2:
#             if events[-2][0] == events[-1][0]:
#                 print(events[-2], events[-1])

#     # 이번 chunk의 마지막 2행을 다음 chunk를 위해 저장
#     previous_rows = chunk.tail(2).copy()

# print("START:", start_cnt)
# print("STOP:", stop_cnt)

# 결과
# (연속된 운행 없음)
# START: 10393
# STOP: 10393


# 아래와 같은 데이터를 만들고자 함
# ===============================
# operation_cycles = [
#     {
#         "start_time": ...,
#         "end_time": ...,
#         "duration": ...
#     },
#     ...
# ]
# ===============================

# previous_rows = None
# operation_cycles = []

# one_cycle = {
#     "start_time" : None,
#     "end_time" : None,
#     "duration" : None
# }

# longest_time = {
#     "start_time" : None,
#     "end_time" : None,
#     "duration" : None
# }
# shortest_time = {
#     "start_time" : None,
#     "end_time" : None,
#     "duration" : None
# }

# for chunk in pd.read_csv(csv_path, chunksize=10_000):
    
#     # 이전 chunk의 마지막 2행을 현재 chunk 앞에 붙임
#     if previous_rows is not None:
#         chunk = pd.concat([previous_rows, chunk], ignore_index=True)
#     else:
#         chunk = chunk.reset_index(drop=True)

#     motor = chunk["Motor_current"]

#     for i in range(len(motor) - 2):
#         current = motor.iloc[i]
#         next_value = motor.iloc[i + 1]
#         next_next_value = motor.iloc[i + 2]
#         event_added = False

#         # START 조건
#         if current <= 1:
#             if next_value >= 3:
#                 event_added = True
#                 one_cycle["start_time"] = chunk["timestamp"].iloc[i + 1]
#             elif (1 < next_value < 3 and next_next_value >= 3):
#                 event_added = True
#                 one_cycle["start_time"] = chunk["timestamp"].iloc[i + 2]
            
#         # STOP 조건
#         elif current >= 3:
#             if next_value <= 1:
#                 event_added = True
#                 one_cycle["end_time"] = chunk["timestamp"].iloc[i + 1]
#             elif (3 > next_value > 1 and next_next_value <= 1):
#                 event_added = True
#                 one_cycle["end_time"] = chunk["timestamp"].iloc[i + 2]

#         else:
#            continue

#         # one_cycle의 start_time과 end_time이 채워지면 duration 채우고 operation_cycles에 저장
#         if one_cycle["start_time"] and one_cycle["end_time"]:
#             start = pd.to_datetime(one_cycle["start_time"])
#             end = pd.to_datetime(one_cycle["end_time"])

#             one_cycle["duration"] = end - start
#             operation_cycles.append(one_cycle)

#             if longest_time["duration"] == None or (longest_time["duration"] and longest_time["duration"] < end - start):
#                 longest_time = one_cycle

#             if shortest_time["duration"] ==  None or (shortest_time["duration"] and shortest_time["duration"] > end - start):
#                 shortest_time = one_cycle

#             one_cycle = {
#               "start_time" : None,
#               "end_time" : None,
#               "duration" : None
#             }

#     # 이번 chunk의 마지막 2행을 다음 chunk를 위해 저장
#     previous_rows = chunk.tail(2).copy()

# print("\noperation_cycles")
# print(len(operation_cycles))
# print(operation_cycles[:5])

# print("\n정상확인 - 가장 긴 운행 시간, 가장 짧은 운행 시간")
# print(longest_time)
# print(shortest_time)

# 정상확인 - 가장 긴 운행 시간, 가장 짧은 운행 시간
# {'start_time': '2020-06-05 09:48:30', 'end_time': '2020-06-08 14:01:15', 'duration': Timedelta('3 days 04:12:45')}
# {'start_time': '2020-05-15 21:13:45', 'end_time': '2020-05-15 21:13:55', 'duration': Timedelta('0 days 00:00:10')}
# 가장 긴 운행이 3일, 가장 짧은 운행이 10초로 정상적으로 보이지 않아 다시 확인
# 긴 운행은 데이터 설명에서 확인한 6월 5일~7일 Air Leak / High stress 기록과 겹치는 구간

targets = [
    ("LONG START", "2020-06-05 09:47:00", "2020-06-05 09:50:00"),
    ("LONG STOP",  "2020-06-08 14:00:00", "2020-06-08 14:03:00"),
    ("SHORT",      "2020-05-15 21:12:00", "2020-05-15 21:15:00"),
]

for chunk in pd.read_csv(
    csv_path,
    chunksize=100_000,
    usecols=["timestamp", "Motor_current"]
):
    chunk["timestamp"] = pd.to_datetime(chunk["timestamp"])

    for name, start, end in targets:
        condition = (
            (chunk["timestamp"] >= start)
            & (chunk["timestamp"] <= end)
        )

        result = chunk.loc[condition, ["timestamp", "Motor_current"]]

        if not result.empty:
            print(f"\n{name}")
            print(result.to_string(index=False))

# SHORT
#           timestamp  Motor_current
# 2020-05-15 21:12:06         0.0400
# 2020-05-15 21:12:16         0.0400
# 2020-05-15 21:12:26         0.0400
# 2020-05-15 21:12:36         0.0400
# 2020-05-15 21:12:46         0.0425
# 2020-05-15 21:12:55         0.0400
# 2020-05-15 21:13:05         0.0400
# 2020-05-15 21:13:15         0.0425
# 2020-05-15 21:13:25         0.0375
# 2020-05-15 21:13:35         0.0425
# 2020-05-15 21:13:45         4.5550
# 2020-05-15 21:13:55         0.0275
# 2020-05-15 21:14:05         0.0300
# 2020-05-15 21:14:15         0.0275
# 2020-05-15 21:14:25         0.0275
# 2020-05-15 21:14:35         0.0275
# 2020-05-15 21:14:44         0.0275
# 2020-05-15 21:14:54         0.0275

# LONG START
#           timestamp  Motor_current
# 2020-06-05 09:47:01         0.0400
# 2020-06-05 09:47:11         0.0400
# 2020-06-05 09:47:21         0.0425
# 2020-06-05 09:47:31         0.0425
# 2020-06-05 09:47:41         0.0425
# 2020-06-05 09:47:51         0.0425
# 2020-06-05 09:48:00         0.0400
# 2020-06-05 09:48:10         0.0425
# 2020-06-05 09:48:20         0.0425
# 2020-06-05 09:48:30         4.7900
# 2020-06-05 09:48:40         5.7400
# 2020-06-05 09:48:50         5.8450
# 2020-06-05 09:49:00         5.8800
# 2020-06-05 09:49:10         5.7875
# 2020-06-05 09:49:20         5.8950
# 2020-06-05 09:49:30         6.0325
# 2020-06-05 09:49:40         6.0200
# 2020-06-05 09:49:49         5.9150
# 2020-06-05 09:49:59         6.0000

# LONG STOP
#           timestamp  Motor_current
# 2020-06-08 14:00:05         3.7950
# 2020-06-08 14:00:15         3.6900
# 2020-06-08 14:00:25         3.7575
# 2020-06-08 14:00:35         3.7450
# 2020-06-08 14:00:45         3.7250
# 2020-06-08 14:00:55         3.7800
# 2020-06-08 14:01:05         3.6700
# 2020-06-08 14:01:15         0.0600
# 2020-06-08 14:01:24         0.0475
# 2020-06-08 14:01:34         0.0475
# 2020-06-08 14:01:44         0.0450
# 2020-06-08 14:01:54         0.0450
# 2020-06-08 14:02:04         0.0450
# 2020-06-08 14:02:14         0.0450
# 2020-06-08 14:02:24         0.0450
# 2020-06-08 14:02:34         0.0450
# 2020-06-08 14:02:44         0.0450
# 2020-06-08 14:02:54         0.0450

# Motor_current 임계값을 기반으로 정의한 START/STOP 추출 로직은 전체 이벤트의 교대 여부와 극단값의 원본 데이터 검증 결과, 내부적으로 일관되게 동작함을 확인.