import os
import csv
import subprocess
import pydicom
import glob
from string import Template

Q = 'findscu -S -k QueryRetrieveLevel=STUDY ' \
    '-k PatientName=$pn ' \
    '-k PatientBirthDate=$bd ' \
    '-k StudyDate=$sd ' \
    '-k StudyInstanceUID ' \
    '-k StudyDescription ' \
    '-aec $aet $host $port ' \
    '-od $od -X'


def main():

    TMP = os.path.join(os.getenv('XDG_RUNTIME_DIR'),'fetchSUID')
    os.makedirs(TMP,exist_ok=True)

    d = {'aet': 'AET-TITLE', 'host': 'localhost', 'port': '104'}
    d['od'] = TMP

    t = Template(Q)
    t = Template(t.safe_substitute(**d))

    ofile = open('../../out.csv', 'w')
    writer = csv.DictWriter(ofile,fieldnames=['pn','bd','sd','StudyInstanceUID','StudyDescription'])
    writer.writeheader()
    with open('../../in.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)


        for line in reader:
            cmd = (t.safe_substitute(**line)).split()
            process = subprocess.Popen(cmd)
            process.wait()

            ris = glob.glob(TMP + '/*.dcm')
            if ris:
                ds = pydicom.dcmread(ris[0])
                line['StudyInstanceUID'] = ds.StudyInstanceUID
                line['StudyDescription'] = ds.StudyDescription
            writer.writerow(line)

            [os.remove(r) for r in ris]
    ofile.close()


if __name__ == '__main__':
    main()