import os
import subprocess
os.chdir(os.path.dirname(os.path.realpath(__file__)))
files = [f for f in os.listdir('.') if os.path.isfile(f) and len(f.split('_'))>1 and f.split('_')[0] == 'Manipulated']

#files = ['Manipulated_ES.log-20170404.csv','Manipulated_IT.log-20170404.csv']
#files = ['Manipulated_ZA.log-20170428.csv']
print files


def bq_loader(f):
    print('trying to start. . .\n')
    os.system('bq mk LogFilesv2_Dataset.'+f.split('_')[1].split('.')[0]+'_Varnish URl:string,Date:string,UserAgent:string,Status:integer,TimeTakenVarnish:float,MissHit:string,Client_IP:string,Referer:string,Size:integer,Timezone:string')
    #os.system("bq load --max_bad_records=10 --field_delimiter='|' --allow_quoted_newlines --allow_jagged_rows Logfilesv2_Dataset."+f.split('_')[1].split('.')[0]+"_Vanish ./"+f)
    s = subprocess.Popen(['bq','load','--max_bad_records=10','--field_delimiter=|','--allow_jagged_rows','--allow_quoted_newlines','LogFilesv2_Dataset.'+f.split('_')[1].split('.')[0]+'_Varnish', './'+f], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout = s.stdout.readlines()
    print(stdout)
    if stdout == ['\n', '\n']:
        print '\nSuccessfully loaded into '+f.split('_')[1].split('.')[0]+'_Varnish\n',
        return
    if stdout[2].split(' ')[0].lower() == 'warning':
        print '\nSuccessfully loaded into '+f.split('_')[1].split('.')[0]+'_Varnish\n',
        return
    if stdout[2].split(' ')[0].lower() == 'bigquery' :
        repeat = True
        print 'failed to load file, repeating 10 times until first success. . .'
        while repeat:
            for i in range(10):
                a = subprocess.Popen(['bq','load','--max_bad_records=10','--field_delimiter=|','--allow_jagged_rows','--allow_quoted_newlines','LogFilesv2_Dataset.'+f.split('_')[1].split('.')[0]+'_Varnish', './'+f], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                stdout = a.stdout.readlines()
                if stdout == ['\n','\n']:
                    print('Successfully loaded')
                    repeat = False
                    break
                if stdout[2].split(' ')[0].lower() == 'warning':
                    print('Successfully loaded')
                    repeat = False
                    break
            repeat = False
    

for f in files:
    if os.stat(f).st_size == 0:
        print 'empty file, skipping %s\n'%f
        continue
    bq_loader(f)
