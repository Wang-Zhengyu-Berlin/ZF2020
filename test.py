import time

today = '2021-03-08'
# print(time)
# thisTime = "2021-01-28"
# thisTime = thisTime.replace('-', '/')
thisTime = time.strptime(today, "%Y-%m-%d")
# thisTime = time.strptime(thisTime, "%Y-%m-%d")
print(thisTime.tm_yday)
print(thisTime)


is_week = ((int(thisTime.tm_yday) - 4) // 7) - 6
print(is_week)
weekStr = "星期一星期二星期三星期四星期五星期六星期日"
# weekId = int(time.strftime("%w"))
pos = (thisTime.tm_wday) * 3
week_name = weekStr[pos: pos+3]
print(week_name)


