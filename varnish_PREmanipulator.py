import os
import datetime
import re

yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
files = [f for f in os.listdir('/home/erowz/varnishlog/SaveExtract/') if  f.split('-')[0] == 'US.log' and f.split('-')[1] == yesterday.strftime("%Y%m%d")]
#files = ['test']
print files

for item in files:
	CA = open('/home/erowz/varnishlog/SaveExtract/CA.log-'+yesterday.strftime("%Y%m%d"),'w' )
	AU = open('/home/erowz/varnishlog/SaveExtract/AU.log-'+yesterday.strftime("%Y%m%d"),'w' )
	US = open('/home/erowz/varnishlog/SaveExtract/new_US.log-'+yesterday.strftime("%Y%m%d"),'w')

        with open('/home/erowz/varnishlog/SaveExtract/'+item,'r') as f:
            for line in f:
                tmp = re.findall(r'\"(.*?)\"',line)
		if tmp[0].split('/')[1] == 'canada':
			CA.write('"'+'";"'.join(tmp)+'"\n')
		elif tmp[0].split('/')[1] == 'australia':
			AU.write('"'+'";"'.join(tmp)+'"\n')
		else:
			US.write('"'+'";"'.join(tmp)+'"\n')
if len(files)>0:
	os.system('mv /home/erowz/varnishlog/SaveExtract/'+files[0]+' /home/erowz/varnishlog/SaveExtract/old_'+files[0])
	os.system('mv /home/erowz/varnishlog/SaveExtract/new_'+files[0]+' /home/erowz/varnishlog/SaveExtract/'+files[0])
