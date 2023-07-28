import csv
import argparse
import os
import time

parser = argparse.ArgumentParser(description="Split csv grouped by specified column",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-f", "--file", help="input .csv file", required=True)
parser.add_argument("-fd", "--fulldump", help="input fulldump .csv file", required=True)
args = parser.parse_args()
config = vars(args)
path = args.file
pathFulldump = args.fulldump
file =os.path.splitext(os.path.basename(path))[0]
fulldump =os.path.splitext(os.path.basename(pathFulldump))[0]
folder = os.path.dirname(path)

REFERENCE2 = 'REFERENCE 2 (orig)'
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
start_time = time.time()
with open(path) as inputFile:
    input_csv_reader = csv.DictReader(inputFile, delimiter=';')   
    filename = os.path.join(folder, f'{file}.output.csv')
    with open(filename, 'w', newline='') as outfile:
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

        with open(pathFulldump) as inputFulldump:      
            fulldump_csv_reader = csv.DictReader(inputFulldump, delimiter=';')

            rows = list(fulldump_csv_reader)

            dumpDict1 = {}
            dumpDict2 = {}

            for rowfd in rows:
                dumpDict1[(rowfd[ProjectNumber], rowfd[ResellerCode])] = {
                   ProjectNumber: rowfd[ProjectNumber],
                   ProductionNumber: rowfd[ProductionNumber],
                   ContractId: rowfd[ContractId],
                   ResellerCode: rowfd[ResellerCode],
                   }
            for rowfd in rows:
                dumpDict2[rowfd[ProjectNumber]] = {
                   ProjectNumber: rowfd[ProjectNumber],
                   ProductionNumber: rowfd[ProductionNumber],
                   ContractId: rowfd[ContractId]
                   }


            for row in input_csv_reader:
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
                        ,REFERENCE2: row[REFERENCE2]
                        ,REFERENCE3: row[REFERENCE3]
                        ,COMP_CODE: row[COMP_CODE]
                        ,PS_XSTAT: row[PS_XSTAT]
                        ,PROFIT_CTR: row[PROFIT_CTR]
                        ,PS_PRJTYPE: row[PS_PRJTYPE]
                        ,STATUSSYS0: row[STATUSSYS0]
                        ,PS_LEVEL: row[PS_LEVEL]
                        ,BIC_ZWBSSP: row[BIC_ZWBSSP]}
                
                _reference2 = row[REFERENCE2]
                _reference3 = row[REFERENCE3]
                if (_reference2,_reference3) in dumpDict1:
                    newrow[ProjectNumber] = dumpDict1[(_reference2,_reference3)][ProjectNumber]
                    newrow[ProductionNumber] = dumpDict1[(_reference2,_reference3)][ProductionNumber]
                    newrow[ContractId] = dumpDict1[(_reference2,_reference3)][ContractId]
                    newrow[ResellerCode] = dumpDict1[(_reference2,_reference3)][ResellerCode]
                elif (_reference2) in dumpDict2:
                    newrow[ProjectNumber] = dumpDict2[(_reference2)][ProjectNumber]
                    newrow[ProductionNumber] = dumpDict2[(_reference2)][ProductionNumber]
                    newrow[ContractId] = dumpDict2[(_reference2)][ContractId]
                output_csv_writer.writerow(newrow)

######Part2########################################
with open(pathFulldump) as inputFulldump: 
    fulldump_csv_reader = csv.DictReader(inputFulldump, delimiter=';')    
    with open(path) as inputFile:
        input_csv_reader = csv.DictReader(inputFile, delimiter=';')
        filename = os.path.join(folder, f'{fulldump}.output.csv')
        with open(filename, 'w', newline='') as outfile:

            header = next(fulldump_csv_reader)            
            fieldnames = list(header.keys()) + ['Match']
            output_csv_writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=';')
            output_csv_writer.writeheader()

            rows = list(input_csv_reader)

            dumpDict1 = {}
            dumpDict2 = {}

            for rowfd in rows:
                dumpDict1[(rowfd[REFERENCE2], rowfd[REFERENCE3])] = object()

            for rowfd in rows:
                dumpDict2[rowfd[REFERENCE2]] = object()

            for rowfd in fulldump_csv_reader:
                newrow = rowfd
                newrow['Match'] = 'N'

                _projectNumber = rowfd[ProjectNumber]
                _resellerCode = rowfd[ResellerCode]

                if (_projectNumber, _resellerCode) in dumpDict1:
                    newrow['Match'] = 'Y'
                elif _projectNumber in dumpDict2:
                    newrow['Match'] = 'P'

                output_csv_writer.writerow(newrow)
                continue
print("--- %s seconds ---" % (time.time() - start_time))
                    




