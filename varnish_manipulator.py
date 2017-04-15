import re
import os
import datetime
import subprocess

#files = [f.split('-') for f in os.listdir('.') if os.path.isfile(f)]


#for item in files:
#	print item
yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
files = [f for f in os.listdir('/home/erowz/varnishlog/SaveExtract/') if  len(f.split('-'))>1 and f.split('-')[1] == yesterday.strftime("%Y%m%d")]


#files = ['ES.log-20170404']

#files = ['PL.log-20170327']
print files
print('cleaning old Manipulated_ logs. . .\n')

os.system('rm -rf /home/erowz/varnish_scripts/Manipulated_*')
for item in files:
	fl = open('/home/erowz/varnish_scripts/Manipulated_'+item+'.csv','w' )
        
        with open('/home/erowz/varnishlog/SaveExtract/'+item,'r') as f:
            for line in f:
                tmp = re.findall(r'\"(.*?)\"',line)
                if len(tmp) == 0:
                    continue
		if len(tmp) != 9:
		    continue
                if tmp[2] == 'refresh from purgequeue':
                    continue
		if tmp[2] == '-':
		    continue
                if tmp[0] in ['/stat','/help','/SendAdsIdStats']:
                    continue
                else:
                    tmp_date = tmp[1].split(' ')
                    if len(tmp_date) != 3:
                        #case if no tz
                        tmp_date = tmp_date[0] + ' 00:00:00'
                        tmp[1] = tmp_date
                        result = ('|').join(tmp)+'\n'
                        fl.write(result)
                    elif len(tmp_date) == 3:
                        #case if tz
                        tmp.append(tmp_date[2])
                        tmp_date = tmp_date[0] + ' 00:00:00'
                        tmp[1] = tmp_date
                        result = ('|').join(tmp)+'\n'
                        fl.write(result)


	print('done',item)
	fl.close()
