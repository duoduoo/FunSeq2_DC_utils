
import re, sys
import os

tempPath = os.environ['PWD']

vcfCol = ['chr','posStart','posEnd','ref','alt','sampleID','CDS','VA','HUB','GNEG','GERP','UCONS','HOT','SEN','USEN','GENE','CDSS','NCDS','NCENC','MOTIFBR','MOTIFG','RECUR','DBRECUR','tumorType']
len(vcfCol)

eachPatient = str(sys.argv[1])
inputVCF=tempPath+'/'+eachPatient+'.vcf'
outputCDS=tempPath+'/'+eachPatient+'_CDS.txt'
outputNCDS=tempPath+'/'+eachPatient+'_NCDS.txt'


with open(inputVCF, 'r') as fin, open(outputCDS, 'w') as foutCDS, open(outputNCDS,'w') as foutNCDS:
    foutCDS.write('\t'.join(vcfCol)+'\n')
    foutNCDS.write('\t'.join(vcfCol)+'\n')
    for line in fin:
        if line.startswith('#'):
            continue
        
        #         print(line)
        line=line.strip()
        fields = line.split('\t')
        
        chrom=fields[0]
        posStart=fields[1]
        posEnd=fields[1]
        ref=fields[3]
        alt=fields[4]
        
        
        infoList = fields[7].split(';')
        infoOut = ['NA']*19
        
        for info in infoList:
            if info.startswith('SAMPLE'):
                infoOut[0]=info.split('=')[1].replace('--*','')
            elif info.startswith('CDS='):
                infoOut[1]=info.split('=')[1]
                cdsStatus=info.split('=')[1]
            
            elif info.startswith('VA'):
                infoOut[2]=info.split('=')[1]
            elif info.startswith('HUB'):
                infoOut[3]=info.split('=')[1]
            elif info.startswith('GNEG'):
                infoOut[4]=info.split('=')[1]
            elif info.startswith('GERP'):
                infoOut[5]=info.split('=')[1]
            elif info.startswith('UCONS'):
                infoOut[6]=info.split('=')[1]
            elif info.startswith('HOT'):
                infoOut[7]=info.split('=')[1]
            elif info.startswith('SEN'):
                infoOut[8]=info.split('=')[1]
            elif info.startswith('USEN'):
                infoOut[9]=info.split('=')[1]
            elif info.startswith('GENE'):
                infoOut[10]=re.sub('\[[^\[]+\]','', info.split('=')[1])
            elif info.startswith('CDSS'):
                infoOut[11]=info.split('=')[1]
            elif info.startswith('NCDS'):
                infoOut[12]=info.split('=')[1]
            elif info.startswith('NCENC'):
                infoOut[13]=re.sub('\[[^\[]+\]','', info.split('=')[1])
            elif info.startswith('MOTIFBR'):
                infoOut[14]=info.split('=')[1]
            elif info.startswith('MOTIFG'):
                infoOut[15]=info.split('=')[1]
            elif info.startswith('RECUR'):
                infoOut[16]=info.split('=')[1]
            elif info.startswith('DBRECUR'):
                infoOut[17]=info.split('=')[1]
            else:
                continue

        infoOut[18] = 'XXXX\n'
        
        if infoOut[16] != 'NA':
            infoOut[16]='Yes'
        else:
            infoOut[16]='No'
        if infoOut[17] != 'NA':
            infoOut[17]='Yes'
        else:
            infoOut[17]='No'
        

        if cdsStatus == 'Yes':
            foutCDS.write('\t'.join([chrom,posStart,posEnd,ref,alt])+'\t')
            foutCDS.write('\t'.join(infoOut))
        elif cdsStatus == 'No':
            foutNCDS.write('\t'.join([chrom,posStart,posEnd,ref,alt])+'\t')
            foutNCDS.write('\t'.join(infoOut))
        else:
            print('Error: something is wrong')

