import subprocess as sp
import csv
import para_best as para
result="result.csv"
bestfile="ME_DATA.csv"
sr="/"
cha="change"
save="save"
under="_"
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

dataname_changelist=["improvefeedback_plus","improvefeedback_minus",\
            "spacedensity","intparamater","phasereverseparamater","duplicateparamater",\
             "digt_EMT_phase","digt_EMT_intensity"]

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

spacedensity = setdat_chr(cha,spacedensity_chr).split()
intparamater= setdat_chr(cha,intparamater_chr).split()
phasereverseparamater = setdat_chr(cha,phasereverseparamater_chr).split()
duplicateparamater= setdat_chr(cha,duplicateparamater_chr).split()
digt_EMT_phase = setdat_chr(cha,digt_EMT_phase_chr).split()
digt_EMT_intensity= setdat_chr(cha,digt_EMT_intensity_chr).split()

d_namelist=[spacedensity,intparamater,phasereverseparamater,duplicateparamater,\
    digt_EMT_intensity,digt_EMT_phase]

nplist=[]
np_plus_list=[]
np_minus_list=[]
evalist=[]
eva_plus_list=[]
eva_minus_list=[]
number_cont = []
paramaternamelist = []
paramaternumberlist = []
paramaterchangelist = []
######
########
for i in range(0,len(d_namelist),1):
    for j in range(1,len(d_namelist[i]),1):
        # for k in range(2,para.improveparamater+1):
# paradata = pd.read_csv(filename)
# print(paradata)
        number_single="{0}_{1}".format(dataname_changelist[i+2],str(j))
        number_cont.append(number_single)
        operationresult = para.current+sr+dataname_changelist[i+2]+sr+\
            save+under+str(j)+sr+result
            #operationfile = filename
            # import numpy as np
        try: 
            cont=[]
            with open(operationresult)as f:
                for row in csv.reader(f):
                    arr=row
                    cont.append(arr)
        except FileNotFoundError :
            continue
        npsingle=int(float(cont[3][0]))
        np_plus_single=int(float(cont[3][1]))
        np_minus_single=int(float(cont[3][2]))
        evasingle=float(cont[5][0])
        eva_plus_single=float(cont[5][1])
        eva_minus_single=float(cont[5][2])
        paramaternamesingle=cont[9][0]
        paramaternumbersingle=cont[9][1]
        paramaterchangesingle=cont[9][2]
        nplist.append(npsingle)
        np_plus_list.append(np_plus_single)
        np_minus_list.append(np_minus_single)
        evalist.append(evasingle)
        eva_plus_list.append(eva_plus_single)
        eva_minus_list.append(eva_minus_single)
        paramaternamelist.append(paramaternamesingle)
        paramaternumberlist.append(paramaternumbersingle)
        paramaterchangelist.append(paramaterchangesingle)
#sort
# sort_nplist = sorted(nplist)
# sort_np_plus_list = sorted(np_plus_list)
# sort_np_minus_list = sorted(np_minus_list)
# sort_evalist = sorted(evalist)
# sort_eva_plus_list = sorted(eva_plus_list)
# sort_eva_minus_list = sorted(eva_minus_list)

# def get_duplicate_list(seq):
#     seen = []
#     return [x for x in seq if not seen.append(x) and seen.count(x) == 1]

# for i in range(1,2):
#     for j in range(1,2):
#         for k in range(1,2):
# # paradata = pd.read_csv(filename)
# # print(paradata)
#             number_single="FIRST_{0}_{1}_{2}".format(str(i),str(j),str(k))
#             # number_cont.append(number_single)
#             operationfile = para.current+sr+improvedirectory+sr+str(i)+sr+\
#                 str(j)+sr+save+str(k)+sr+filename
#             #operationfile = filename
#             # import numpy as np
#             cont=[]
#             with open(operationfile)as f:
#                 for row in csv.reader(f):
#                     arr=row
#                     cont.append(arr)
#                 npsingle=int(cont[1][0])
#                 np_plus_single=int(cont[1][1])
#                 np_minus_single=int(cont[1][2])
#                 evasingle=float(cont[7][0])
#                 eva_plus_single=float(cont[7][1])
#                 eva_minus_single=float(cont[7][2])
#                 # nplist.append(npsingle)
#                 # np_plus_list.append(np_plus_single)
#                 # np_minus_list.append(np_minus_single)
#                 # evalist.append(evasingle)
#                 # eva_plus_list.append(eva_plus_single)
#                 # eva_minus_list.append(eva_minus_single)


finalplace=para.current+sr+bestfile
f = open(finalplace,'w')
f.write("File_NAME,")
for i in range(len(number_cont)):
    f.write("{},".format(number_cont[i]))
f.write("\n")
f.write("npnumber,")
for i in range(len(nplist)):
    f.write("{},".format(nplist[i]))
f.write("\n")
f.write("np_plus_number,")
for i in range(len(np_plus_list)):
    f.write("{},".format(np_plus_list[i]))
f.write("\n")
f.write("np_minus_number,")
for i in range(len(np_plus_list)):
    f.write("{},".format(np_minus_list[i]))
f.write("\n")
f.write("evaluation,")
for i in range(len(evalist)):
    f.write("{},".format(evalist[i]))
f.write("\n")
f.write("evaluation_plus,")
for i in range(len(eva_plus_list)):
    f.write("{},".format(eva_plus_list[i]))
f.write("\n")
f.write("evaluation_minus,")
for i in range(len(eva_minus_list)):
    f.write("{},".format(eva_minus_list[i]))
f.write("\n")
f.write("paramatername,")
for i in range(len(paramaternamelist)):
    f.write("{},".format(paramaternamelist[i]))
f.write("\n")
f.write("paramaternumber,")
for i in range(len(paramaternumberlist)):
    f.write("{},".format(paramaternumberlist[i]))
f.write("\n")
f.write("paramaterchange,")
for i in range(len(paramaterchangelist)):
    f.write("{},".format(paramaterchangelist[i]))
f.write("\n")
f.close()
