import os
import datetime
import subprocess

#files = [f.split('-') for f in os.listdir('.') if os.path.isfile(f)]


#for item in files:
#	print item
files = [f for f in os.listdir('.') if os.path.isfile(f) and len(f.split('-'))>1 and f.split('-')[1] == datetime.datetime.now().strftime("%Y%m%d")]

#files = ['PL.log-20170327']
print files
for item in files:
	fl = open( 'Manipulated_'+item+'.csv','w' )
	l = '''cat %s| awk -F";" '{gsub(/"/,"",$5);print$1,$2,$3,$4,$5/1000000,$6,$7,$8,$9}' OFS=";"'''%item
	for line in subprocess.check_output(l,shell=True).split('\n')[5:]:
		if len(line)==0:
			continue
		if line.split(';')[0].replace('"','') in ['/stat','help','SendAdsIdStats']:
			continue
		if line.split(';')[2].replace('"','') == 'refresh from purgequeue':
			continue
		else:
			tmp = line.split(';')
			tmp_date = tmp[1].split(' ')
			if len(tmp_date) != 3:
				#case if no tz
				tmp_date = tmp_date[0]+' 00:00:00'
				tmp[1] = tmp_date
				lol = (';').join(tmp)[:-1]+'\n'
				fl.write(lol)
			elif len(tmp_date) == 3:
				#case if tz
				tmp.append('"'+tmp_date[2])
				tmp_date = tmp_date[0]+' 00:00:00'
				tmp[1] = tmp_date
				lol = (';').join(tmp)+'\n'
				fl.write(lol)
	print('done',item)
	fl.close()
