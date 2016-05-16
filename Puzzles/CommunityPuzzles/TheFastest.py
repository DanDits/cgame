n = int(input())
times = [tuple(map(int, input().split(":"))) for _ in range(n)]
times.sort(key=lambda time: time[0] * 60 * 60 + time[1] * 60 + time[2])
print("%02d:%02d:%02d" % times[0])