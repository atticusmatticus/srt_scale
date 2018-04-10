# python srt_scale.py [srt_file] [out_file] [minute_shift] [second_shift] [milsec_shift]
import numpy as np
import sys

srt_file = sys.argv[1]
outFile = str(sys.argv[2])
min_shift = int(sys.argv[3])
sec_shift = int(sys.argv[4])
mil_shift = int(sys.argv[5])

i=0
f = open(srt_file)
for line in f:
    i+=1

index = np.empty(((i+1)/4),dtype=int)
time = []
caption = []
cap_lines = np.empty(((i+1)/4),dtype=int)

i=0; j=0
f = open(srt_file)
for line in f:
    if i == 0:
        index[j] = line
        i+=1
        j+=1
    elif i == 1:
        time.append(line)
        i+=1
    elif i == 2:
        caption.append(line)
        i+=1
    elif i == 3: # either empty or another caption line
        if not line.strip(): # if line is empty
            k=1
            cap_lines[j-1] = k
            i=0 # start over again
        else: # if there is another caption line
            caption.append(line)
            k=2
            cap_lines[j-1] = k
            i=4
    elif i == 4:
        i=0

i=0; k=0
f = open(outFile, 'w')
for item in time:
    # start time
    hour1 = int(item[0:2])
    minute1 = int(item[3:5])
    second1 = int(item[6:8])
    milsec1 = int(item[9:12])
    # stop time
    hour2 = int(item[17:19])
    minute2 = int(item[20:22])
    second2 = int(item[23:25])
    milsec2 = int(item[26:29])
    # shift time
    time1 = hour1*60*60*1000 + minute1*60*1000 + second1*1000 + milsec1
    time2 = hour2*60*60*1000 + minute2*60*1000 + second2*1000 + milsec2
    time1 += min_shift*60*1000 + sec_shift*1000 + mil_shift
    time2 += min_shift*60*1000 + sec_shift*1000 + mil_shift
    # convert back into hours, minutes, seconds, and miliseconds
    new_hr1,rem1 = divmod(time1, 60*60*1000)
    new_min1,rem2 = divmod(rem1, 60*1000)
    new_sec1,new_mil1 = divmod(rem2, 1000)
    new_hr2,rem1 = divmod(time2, 60*60*1000)
    new_min2,rem2 = divmod(rem1, 60*1000)
    new_sec2,new_mil2 = divmod(rem2, 1000)
    # write to output file
    if cap_lines[i] == 1:
        f.write('{:d}\n{:02d}:{:02d}:{:02d},{:03d} --> {:02d}:{:02d}:{:02d},{:03d}\n{}\n'.format(index[i], new_hr1, new_min1, new_sec1, new_mil1, new_hr2, new_min2, new_sec2, new_mil2, caption[i+k]))
    elif cap_lines[i] == 2:
        f.write('{:d}\n{:02d}:{:02d}:{:02d},{:03d} --> {:02d}:{:02d}:{:02d},{:03d}\n{}{}\n'.format(index[i], new_hr1, new_min1, new_sec1, new_mil1, new_hr2, new_min2, new_sec2, new_mil2, caption[i+k], caption[i+k+1]))
        k+=1
    i+=1

f.close()
