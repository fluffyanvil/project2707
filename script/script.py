import csv
import argparse
import os
import time

parser = argparse.ArgumentParser(description="Split csv grouped by specified column",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-f", "--file", help="input .csv file, example, WBS.csv", required=True)
parser.add_argument("-fd", "--fulldump", help="input fulldump .csv file, example WON2SAP__fulldump.csv", required=True)
args = parser.parse_args()
config = vars(args)
path = args.file
pathFulldump = args.fulldump
file =os.path.splitext(os.path.basename(path))[0]
fulldump =os.path.splitext(os.path.basename(pathFulldump))[0]
folder = os.path.dirname(path)

REFERENCE2 = 'REFERENCE 2'
REFERENCE3 = 'REFERENCE 3'
ProjectNumber = 'ProjectNumber'
ResellerCode = 'ResellerCode'

PROJECT_GROUP = 'PROJECT_GROUP'
PROJECTGRP_TEXT = 'PROJECTGRP_TEXT'
PROJECT = 'PROJECT'
PROJECT_TEXT = 'PROJECT_TEXT'
WBS_ELEMT = 'WBS_ELEMT'
TEXT = 'TEXT'
REFERENCE1 = 'REFERENCE 1'
ProductionNumber = 'ProductionNumber'
ContractId = 'ContractId'
ResellerCode = 'ResellerCode'
COMP_CODE = 'COMP_CODE'
PS_XSTAT = 'PS_XSTAT'
PROFIT_CTR = 'PROFIT_CTR'
PS_PRJTYPE = 'PS_PRJTYPE'
STATUSSYS0 = 'STATUSSYS0'
PS_LEVEL = 'PS_LEVEL'
BIC_ZWBSSP = '/BIC/ZWBSSP'

ExternalReference = 'ExternalReference'
ProgramTitle = 'ProgramTitle'
WBS = 'WBS'
AssetId = 'AssetId'

######Part1#####################################################
# populate WBS with WON2SAP data
start_time = time.time()
with open(path, encoding="utf-8") as inputFile:
    input_csv_reader = csv.DictReader(inputFile, delimiter=';')   
    filename = os.path.join(folder, f'{file}.output.csv')
    
    modified_input = filename;
    with open(filename, 'w', newline='', encoding="utf-8") as outfile:
        fieldnames = [PROJECTGRP_TEXT
                    ,PROJECT
                    ,PROJECT_TEXT
                    ,WBS_ELEMT
                    ,TEXT
                    ,REFERENCE1
                    ,ProjectNumber
                    ,ProductionNumber
                    ,ContractId
                    ,ResellerCode
                    ,REFERENCE2
                    ,REFERENCE3
                    ,COMP_CODE
                    ,PS_XSTAT
                    ,PROFIT_CTR
                    ,PS_PRJTYPE
                    ,STATUSSYS0
                    ,PS_LEVEL
                    ,BIC_ZWBSSP]
        output_csv_writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=';')
        output_csv_writer.writeheader()

        with open(pathFulldump, encoding="utf-8") as inputFulldump:      
            fulldump_csv_reader = csv.DictReader(inputFulldump, delimiter=';')

            rows = list(fulldump_csv_reader)

#index with ProjectNumber and ResellerCode
            dumpDict1 = {}
            
#index with ProjectNumber and empty ResellerCode
            dumpDict2 = {}            
# fill index for full match (ProjectNumber + ResellerCode)
            for rowfd in rows:
                pr_num = str(rowfd[ProjectNumber]).strip();
                res_code = str(rowfd[ResellerCode]).strip();
                
                if (len(pr_num) == 0):
                    continue
                # fill only if ProljectNumber and ResellerCode not empty
                if (len(pr_num) > 0 and len(res_code) > 0):
                    dumpDict1[pr_num, res_code] = {
                       ProjectNumber: str(rowfd[ProjectNumber]).strip(),
                       ProductionNumber: str(rowfd[ProductionNumber]).strip(),
                       ContractId: str(rowfd[ContractId]).strip(),
                       ResellerCode: str(rowfd[ResellerCode]).strip(),
                       }
# fill index for full match (ProjectNumber)
                if (len(pr_num) > 0):
                    dumpDict2[pr_num] = {
                       ProjectNumber: str(rowfd[ProjectNumber]).strip(),
                       ProductionNumber: str(rowfd[ProductionNumber]).strip(),
                       ContractId: str(rowfd[ContractId]).strip(),
                       }
                
# counters for fillings
            ref23_fill = 0
            ref2_fill = 0
            no_fill = 0
            rows = list(input_csv_reader)
            for row in rows:

                _reference2 = str(row[REFERENCE2]).strip()
                _reference3 = str(row[REFERENCE3]).strip()                

                newrow = {
                            PROJECTGRP_TEXT:row[PROJECTGRP_TEXT]
                        ,PROJECT: row[PROJECT]
                        ,PROJECT_TEXT: row[PROJECT_TEXT]
                        ,WBS_ELEMT: row[WBS_ELEMT]
                        ,TEXT: row[TEXT]
                        ,REFERENCE1: row[REFERENCE1]
                        ,ProjectNumber: ''
                        ,ProductionNumber: ''
                        ,ContractId: ''
                        ,ResellerCode: ''
                        ,REFERENCE2: _reference2
                        ,REFERENCE3: _reference3
                        ,COMP_CODE: row[COMP_CODE]
                        ,PS_XSTAT: row[PS_XSTAT]
                        ,PROFIT_CTR: row[PROFIT_CTR]
                        ,PS_PRJTYPE: row[PS_PRJTYPE]
                        ,STATUSSYS0: row[STATUSSYS0]
                        ,PS_LEVEL: row[PS_LEVEL]
                        ,BIC_ZWBSSP: row[BIC_ZWBSSP]}
 # if REFERENCE 2 in WBS is empty, skip               
                if (len(_reference2) == 0):
                    no_fill+=1
 # if REFERENCE 2 and REFERENCE 3 is not empty, try find match in index (dumpDict1)
                elif (len(_reference2) > 0 and len(_reference3) > 0):
                    if (_reference2, _reference3) in dumpDict1:
                        r = dumpDict1[(_reference2, _reference3)]
                        newrow[ProjectNumber] = str(r[ProjectNumber]).strip()
                        newrow[ProductionNumber] = str(r[ProductionNumber]).strip()
                        newrow[ContractId] = str(r[ContractId]).strip()
                        newrow[ResellerCode] = str(r[ResellerCode]).strip()
                        ref23_fill+=1
                    else:
                        no_fill+=1
 # if REFERENCE 3 is emplty and  REFERENCE 2 is not empty, try find match in index (dumpDict2) - patrial matching
                elif (len(_reference2) > 0):
                    if (_reference2) in dumpDict2:
                        r = dumpDict2[(_reference2)]
                        newrow[ProjectNumber] = str(r[ProjectNumber]).strip()
                        newrow[ProductionNumber] = str(r[ProductionNumber]).strip()
                        newrow[ContractId] = str(r[ContractId]).strip()
                        ref2_fill+=1
                    else:
                        no_fill+=1
                    
                output_csv_writer.writerow(newrow)


print("--- Populated: REFERENCE2+REFERENCE3 = %s, REFERENCE2 = %s, NOFILL = %s ---" % (ref23_fill, ref2_fill, no_fill))
######Part2########################################
# populating WON2SAP__fulldump with WBS data
with open(pathFulldump, encoding="utf-8") as inputFulldump: 
    fulldump_csv_reader = csv.DictReader(inputFulldump, delimiter=';')    
    with open(modified_input, encoding="utf-8") as inputFile:
        input_csv_reader = csv.DictReader(inputFile, delimiter=';')
        filename = os.path.join(folder, f'{fulldump}.output.csv')
        with open(filename, 'w', newline='', encoding="utf-8") as outfile:

            header = next(fulldump_csv_reader)            
            fieldnames = list(header.keys()) + ['Match']
            output_csv_writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=';')
            output_csv_writer.writeheader()

            rows = list(input_csv_reader)

            dumpDict1 = {}
            dumpDict2 = {}

            for rowfd in rows:
                
                _reference2 = str(rowfd[REFERENCE2]).strip()
                _reference3 = str(rowfd[REFERENCE3]).strip()
                if (len(_reference2) == 0):
                    continue
                if (len(_reference3) > 0):
                    dumpDict1[_reference2, _reference3] = object()
                dumpDict2[_reference2] = object()
                

            y = 0
            n = 0
            p = 0
            
            for rowfd in fulldump_csv_reader:
                newrow = rowfd                

                _projectNumber = str(rowfd[ProjectNumber]).strip()
                _resellerCode = str(rowfd[ResellerCode]).strip()
                
                if (len(_projectNumber) > 0 and len(_resellerCode) > 0 and (_projectNumber, _resellerCode) in dumpDict1):
                    newrow['Match'] = 'Y'
                    y+=1
                elif (len(_projectNumber) > 0 and len(_resellerCode) > 0 and _projectNumber in dumpDict2):       
                    newrow['Match'] = 'P'
                    p+=1  
                else:
                    newrow['Match'] = 'N'
                    n+=1 

                output_csv_writer.writerow(newrow)

print("--- Matches: Y = %s, P = %s, N = %s ---" % (y, p, n))
print("--- %s seconds ---" % (time.time() - start_time))
                    




