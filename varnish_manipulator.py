import re
import os, csv
#import datetime
import subprocess, datetime
from datetime import datetime
import datetime as dt
os.chdir(os.path.dirname(os.path.realpath(__file__)))
from dateutil.rrule import rrule, DAILY
from datetime import date
#files = [f.split('-') for f in os.listdir('.') if os.path.isfile(f)]


#for item in files:
#	print item
today = dt.datetime.now()# - dt.timedelta(days=5)
files = [f for f in os.listdir('/home/erowz/varnishlog/SaveExtract/') if  len(f.split('-'))>1 and f.split('-')[1] == today.strftime("%Y%m%d")]


#files = ['IT.log-20170419']

#files = ['PL.log-20170327']
print files
print('cleaning old Manipulated_ logs. . .\n')
dtstop = date.today()
dtstart = date.today() - dt.timedelta(5)
fresh = [dt.strftime('%Y%m%d') for dt in rrule(DAILY, dtstart=dtstart, until=dtstop)]

all_files = [f for f in os.listdir('/home/erowz/varnishlog/SaveExtract/') if  len(f.split('-'))>1]

for f in all_files:
    for fresh_date in fresh:
        if fresh_date not in f: os.system('rm -rf /home/erowz/varnishlog/BackupLogs/'+f)


for item in files:
	if 'old_US' in item:
		continue
        fl = open('/home/erowz/varnishlog/BackupLogs/Manipulated_'+item+'.csv','w' )
        
        with open('/home/erowz/varnishlog/SaveExtract/'+item,'r') as f:
            reader = csv.reader(f, delimiter=' ')
            writer = csv.writer(fl)
            for line in reader:
                tmp = [x for x in line]#re.findall(r'\"(.*?)\"',line)
                tmp[1] = tmp[0]+tmp[1]
                tmp.remove(tmp[0])
                if len(tmp) == 0:
                    continue
		if len(tmp) != 12:
		    continue
                if tmp[2] in ['/stat','/help','/SendAdsIdStats']:
                    continue
                if tmp[1] in ['PURGE','REFRESH','OPTIONS','HEAD']: continue

                tmp[0] = datetime.strptime(tmp[0].replace('[','').replace(']','').split(':')[0],"%d/%b/%Y").strftime('%Y-%m-%d 00:00:00')
                try:tmp[5] = tmp[5]/1000000
                except:pass
                if tmp[-1] == '-': tmp[-1] = '' #age fix
                if tmp[3] == '-': tmp[3] = '' #status fix
                result = ('|').join(tmp)+'\n'
                fl.write(result)


	print('done',item)
	fl.close()
