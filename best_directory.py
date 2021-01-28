import subprocess as sp
import csv
import para_best as para
filename="result.csv"
bestfile="Final_DATA.csv"
sr="/"
cha="change"
save="save"
evalue = 0
enumber = 0
#dataparamater
improvedirectory="improve"
defocus_chr = "defocus"
ntfftx_chr = "ntfftx"
ntffty_chr = "ntffty"
bion_focus_chr = "bion_focus"
improveth_plus_chr = "improveth_plus"
improveth_minus_chr = "improveth_minus"
improvefeedback_plus_chr = "improvefeedback_plus"
improvefeedback_minus_chr = "improvefeedback_minus"
spacedensity_chr = "spacedensity"
intparamater_chr = "intparamater"
phasereverseparamater_chr = "phasereverseparamater"
duplicateparamater_chr = "duplicateparamater"
field_chr = "field"
digt_EMT_phase_chr = "digt_EMT_phase"
digt_EMT_intensity_chr = "digt_EMT_intensity"
improveparamater_chr = "improveparamater"

def setdat_chr(a1,a2):
    with open(a1) as f:
        lines = f.readlines()
        lines_strip = [line.strip() for line in lines]
        xxx = [line for line in lines_strip if a2 in line]
        return xxx[0]
def setdat(a1,a2,a3):
    with open(a1) as f:
        lines = f.readlines()
        lines_strip = [line.strip() for line in lines]
        xxx = [line for line in lines_strip if a2 in line]
        yyy = xxx[0].split(' ')
        return yyy[a3]

pluslist = setdat_chr(cha,improvefeedback_plus_chr).split()
minuslist = setdat_chr(cha,improvefeedback_minus_chr).split()

nplist=[]
np_plus_list=[]
np_minus_list=[]
evalist=[]
eva_plus_list=[]
eva_minus_list=[]
number_cont = []

######

########
for i in range(1,len(pluslist)):
    for j in range(1,len(minuslist)):
        for k in range(2,para.improveparamater+1):
# paradata = pd.read_csv(filename)
# print(paradata)

            #operationfile = filename
            # import numpy as np
            cont=[]
            try:
                operationfile = para.current+sr+improvedirectory+sr+str(i)+sr+\
                    str(j)+sr+save+str(k)+sr+filename
                with open(operationfile)as f:
                    for row in csv.reader(f):
                        arr=row
                        cont.append(arr)
            except FileNotFoundError :
                continue
            number_single="{0}_{1}_{2}".format(str(i),str(j),str(k))
            number_cont.append(number_single)
            npsingle=int(float(cont[3][0]))
            np_plus_single=int(float(cont[3][1]))
            np_minus_single=int(float(cont[3][2]))
            evasingle=float(cont[5][0])
            eva_plus_single=float(cont[5][1])
            eva_minus_single=float(cont[5][2])
            nplist.append(npsingle)
            np_plus_list.append(np_plus_single)
            np_minus_list.append(np_minus_single)
            evalist.append(evasingle)
            eva_plus_list.append(eva_plus_single)
            eva_minus_list.append(eva_minus_single)
            print(i,j,k)

#sort
sort_nplist = sorted(nplist)
sort_np_plus_list = sorted(np_plus_list)
sort_np_minus_list = sorted(np_minus_list)
sort_evalist = sorted(evalist)
sort_eva_plus_list = sorted(eva_plus_list)
sort_eva_minus_list = sorted(eva_minus_list)

def get_duplicate_list(seq):
    seen = []
    return [x for x in seq if not seen.append(x) and seen.count(x) == 1]

for i in range(1,2):
    for j in range(1,2):
        for k in range(1,2):
# paradata = pd.read_csv(filename)
# print(paradata)

            operationfile = para.current+sr+improvedirectory+sr+str(i)+sr+\
                str(j)+sr+save+str(k)+sr+filename
            #operationfile = filename
            # import numpy as np
            cont=[]
            with open(operationfile)as f:
                for row in csv.reader(f):
                    arr=row
                    cont.append(arr)            
                number_single="FIRST_{0}_{1}_{2}".format(str(i),str(j),str(k))
                npsingle=int(float(cont[3][0]))
                np_plus_single=int(float(cont[3][1]))
                np_minus_single=int(float(cont[3][2]))
                evasingle=float(cont[5][0])
                eva_plus_single=float(cont[5][1])
                eva_minus_single=float(cont[5][2])
                # nplist.append(npsingle)
                # np_plus_list.append(np_plus_single)
                # np_minus_list.append(np_minus_single)
                # evalist.append(evasingle)
                # eva_plus_list.append(eva_plus_single)
                # eva_minus_list.append(eva_minus_single)


finalplace=para.current+sr+bestfile
f = open(finalplace,'w')
empty=[]
f.write("npnumber,{}\n".format(npsingle))
for i in range(len(sort_nplist)):
    seen = []
    empty = empty +[[j for j, x in enumerate(nplist) if x ==sort_nplist[i] \
        and not seen.append(x) and not seen.count(x) ==0]]
readylist=get_duplicate_list(empty)
for i in range(len(readylist)):
    if len(readylist[i]) !=1:
        for j in range(len(readylist[i])):
            f.write("{0},".format(number_cont[readylist[i][j]]))
    if len(readylist[i]) ==1:
        f.write("{0},".format(number_cont[readylist[i][0]]))
f.write("\n")
for i in range(len(number_cont)):
    f.write("{0},".format(str(sort_nplist[i])))
f.write("\n")
empty=[]
f.write("npnumber_plus,{}\n".format(np_plus_single))
for i in range(len(sort_np_plus_list)):
    seen = []
    empty = empty +[[j for j, x in enumerate(np_plus_list) if x ==sort_np_plus_list[i] \
        and not seen.append(x) and not seen.count(x) ==0]]
readylist=get_duplicate_list(empty)
for i in range(len(readylist)):
    if len(readylist[i]) !=1:
        for j in range(len(readylist[i])):
            f.write("{0},".format(number_cont[readylist[i][j]]))
    if len(readylist[i]) ==1:
        f.write("{0},".format(number_cont[readylist[i][0]]))
f.write("\n")
for i in range(len(number_cont)):
    f.write("{0},".format(str(sort_np_plus_list[i])))
f.write("\n")
empty=[]
f.write("npnumber_minus,{}\n".format(np_minus_single))
for i in range(len(sort_np_minus_list)):
    seen = []
    empty = empty +[[j for j, x in enumerate(np_minus_list) if x ==sort_np_minus_list[i] \
        and not seen.append(x) and not seen.count(x) ==0]]
readylist=get_duplicate_list(empty)
for i in range(len(readylist)):
    if len(readylist[i]) !=1:
        for j in range(len(readylist[i])):
            f.write("{0},".format(number_cont[readylist[i][j]]))
    if len(readylist[i]) ==1:
        f.write("{0},".format(number_cont[readylist[i][0]]))
f.write("\n")
for i in range(len(number_cont)):
    f.write("{0},".format(str(sort_np_minus_list[i])))
f.write("\n")
empty=[]
f.write("evaluation,{}\n".format(evasingle))
for i in range(len(sort_evalist)):
    seen = []
    empty = empty +[[j for j, x in enumerate(evalist) if x ==sort_evalist[i] \
        and not seen.append(x) and not seen.count(x) ==0]]
readylist=get_duplicate_list(empty)
for i in range(len(readylist)):
    if len(readylist[i]) !=1:
        for j in range(len(readylist[i])):
            f.write("{0},".format(number_cont[readylist[i][j]]))
    if len(readylist[i]) ==1:
        f.write("{0},".format(number_cont[readylist[i][0]]))
f.write("\n")
for i in range(len(number_cont)):
    f.write("{0},".format(str(sort_evalist[i])))
f.write("\n")
empty=[]
f.write("evaluation_plus,{}\n".format(eva_plus_single))
for i in range(len(sort_eva_plus_list)):
    seen = []
    empty = empty +[[j for j, x in enumerate(eva_plus_list) if x ==sort_eva_plus_list[i] \
        and not seen.append(x) and not seen.count(x) ==0]]
readylist=get_duplicate_list(empty)
for i in range(len(readylist)):
    if len(readylist[i]) !=1:
        for j in range(len(readylist[i])):
            f.write("{0},".format(number_cont[readylist[i][j]]))
    if len(readylist[i]) ==1:
        f.write("{0},".format(number_cont[readylist[i][0]]))
f.write("\n")
for i in range(len(number_cont)):
    f.write("{0},".format(str(sort_eva_plus_list[i])))
f.write("\n")
empty=[]
f.write("evaluation_minus,{}\n".format(eva_minus_single))
for i in range(len(sort_eva_minus_list)):
    seen = []
    empty = empty +[[j for j, x in enumerate(eva_minus_list) if x ==sort_eva_minus_list[i] \
        and not seen.append(x) and not seen.count(x) ==0]]
readylist=get_duplicate_list(empty)
for i in range(len(readylist)):
    if len(readylist[i]) !=1:
        for j in range(len(readylist[i])):
            f.write("{0},".format(number_cont[readylist[i][j]]))
    if len(readylist[i]) ==1:
        f.write("{0},".format(number_cont[readylist[i][0]]))
f.write("\n")
for i in range(len(number_cont)):
    f.write("{0},".format(str(sort_eva_minus_list[i])))
f.write("\n")
f.write("\n")
f.write("FILE_NAME,")
for i in range(1,len(pluslist)):
    for j in range(1,len(minuslist)):
        f.write("{0}_{1},".format(str(i),str(j)))
f.write("\n")
f.write("fb_plus,")
for i in range(1,len(pluslist)):
    for j in range(1,len(minuslist)):
        f.write("{0},".format(str(pluslist[i])))
f.write("\n")
f.write("fb_minus,")
for i in range(1,len(pluslist)):
    for j in range(1,len(minuslist)):
        f.write("{0},".format(str(minuslist[j]))) 
f.write("\n")
f.write("spacedensity,{}".format(str(para.spacedensity)))
f.write("\n")
f.write("intparamater,{}".format(str(para.intparamater)))
f.write("\n")
f.write("phasereverseparamater,{}".format(str(para.phasereverseparamater)))
f.write("\n")
f.write("duplicateparamater,{}".format(str(para.duplicateparamater)))
f.write("\n")
f.write("digt_EMT_phase,{}".format(str(para.digt_EMT_phase)))
f.write("\n")
f.write("digt_EMT_intensity,{}".format(str(para.digt_EMT_intensity)))
f.write("\n")
f.write("digialnumber,{}".format(para.digtalnumber))
f.write("\n")
f.write("improveth_plus,{}".format(str(para.improveth_plus)))
f.write("\n")
f.write("improveth_minus,{}".format(str(para.improveth_minus)))
f.write("\n")
f.write("improveparamater,{}".format(str(para.improveparamater)))
f.close()
