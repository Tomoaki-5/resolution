import subprocess as sp
import asyncio
#commandcharacter
macrofile="/home/Osumi/resolution/"
MASK="MASK"
x1="BION-A"
x2="BION-D"
cha="res_change"
imp="resolution.py"
impnext="improvenext.py"
bionpy="bion_resolution.py"
datapy="data.py"
save="save"
np="np"
npy=".npy"
result="result"
csv=".csv"
point="point"
seed="seed"
slid="sild"
html=".html"
mplotmtv="mplotmtv"
py=".py"
dq='"'
space=' '
under="_"
sr="/"
single_sh="single.sh"
resolution_sh = "resolution.sh"
csv2np_py = "csv2np.py"
best_d_py="best_directory.py"
comparepy="para_compare.py"
f2pyfile="f2py_module.cpython-38-x86_64-linux-gnu.so"
f2py_div_file="f2py_div.cpython-38-x86_64-linux-gnu.so"
# interpolatepy="interpolate.py"
#dataparamater
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
size_chr="size"
interpolatenumber_chr="interpolatenumber"


async def bashwait(num,asylist_single):
    asylist_single.wait()
    print("{0}waiting".format(num))
def commandwait(asylist):
    loop = asyncio.get_event_loop()
    task = asyncio.gather(*[bashwait(x,asylist[x]) for x in range(len(asylist))])
    loop.run_until_complete(task)



def setdat(a1,a2,a3):
    with open(a1) as f:
        lines = f.readlines()
        lines_strip = [line.strip() for line in lines]
        xxx = [line for line in lines_strip if a2 in line]
        yyy = xxx[0].split(' ')
        return yyy[a3]
def setdat_chr(a1,a2):
    with open(a1) as f:
        lines = f.readlines()
        lines_strip = [line.strip() for line in lines]
        xxx = [line for line in lines_strip if a2 in line]
        return xxx[0]
def transport(b1,b2,b3):
    cmd = "cp -p {0} {1}".format(b1,b2)
    sp.run(cmd,shell=True,cwd=b3)
    return None
def digt_EMT_function(c1):
    c2="{:.2f}".format(c1-0.1)
    c3="{:.2f}".format(c1+0.1)
    return c2,c3
cmd = "pwd" 
current=sp.check_output(cmd.split()).decode('utf-8')
current=current.replace('\n',"")
print(current)
cmd = "ls" 
w = sp.check_output(cmd.split()).decode('utf-8')
w=w.replace('\n',"")
print(w)
y1 = w.split('.')[0]
print(y1)
yy=y1
minimamlist=[x1,x2,imp,bionpy,single_sh,f2pyfile,resolution_sh,csv2np_py]
firstlist=[cha,comparepy,best_d_py]
filelist=minimamlist+firstlist
wlist=[w]
cplist = minimamlist+wlist
for i in range(len(filelist)):
    cmd = "cp -p {0}{1} {2}".format(macrofile,filelist[i],current)
    sp.run(cmd,shell=True) 

cmd = "chmod -R 777 {}".format(current)
sp.run(cmd,shell=True)

m = setdat(x1,defocus_chr,3)
#digital
mdigital = setdat(x2,defocus_chr,3)
zstart = setdat(x2,defocus_chr,1)
zend = setdat(x2,defocus_chr,2)
ntfftx = setdat(x2,ntfftx_chr,1)
ntffty = setdat(x2,ntffty_chr,1)
bion_focus = setdat(x1,bion_focus_chr,1)
#gapz = -1*gapnum

fieldx = setdat(x1,field_chr,3)
fieldy = setdat(x1,field_chr,4)
xstart = setdat(x1,field_chr,1)
ystart = setdat(x1,field_chr,2)
#impnum = setdat(imp,improve_chr,2)
# improveth_plus = setdat(cha,improveth_plus_chr,1)
# improveth_minus = setdat(cha,improveth_minus_chr,1)
improveparamater = setdat(cha,improveparamater_chr,1)
size = setdat(cha,size_chr,1)
interpolatenumber = setdat(cha,interpolatenumber_chr,1)
# improveth_plus = setdat_chr(cha,improveth_plus_chr).split()
# improvefeedback_plus= setdat_chr(cha,improvefeedback_plus_chr).split()
# # improveth_minus = setdat_chr(cha,improveth_minus_chr).split()
# improvefeedback_minus= setdat_chr(cha,improvefeedback_minus_chr).split()
# spacedensity = setdat_chr(cha,spacedensity_chr).split()
# intparamater= setdat_chr(cha,intparamater_chr).split()
# phasereverseparamater = setdat_chr(cha,phasereverseparamater_chr).split()
# duplicateparamater= setdat_chr(cha,duplicateparamater_chr).split()
# digt_EMT_phase = setdat_chr(cha,digt_EMT_phase_chr).split()
# digt_EMT_intensity= setdat_chr(cha,digt_EMT_intensity_chr).split()
# improveparamater= setdat_chr(cha,improveparamater_chr).split()


#digt_num=dq+digt_num+dq

#only analog
Azstart = setdat(x1,defocus_chr,1)
Azend = setdat(x1,defocus_chr,2)
Antfftx = setdat(x1,ntfftx_chr,1)
Antffty = setdat(x1,ntffty_chr,1)

fixnamelist=["m","mdigital","zstart","zend","ntfftx","ntffty","bion_focus","fieldx",\
        "fieldy","xstart","ystart","Azstart","Azend","Antfftx","Antffty","field",\
        "improveparamater","size","interpolatenumber"]

# fixnamelist=["m","mdigital","zstart","zend","ntfftx","ntffty","bion_focus","fieldx",\
#         "fieldy","xstart","ystart","Azstart","Azend","Antfftx","Antffty","field",\
#         "improveth_plus","improveth_minus","improveparamater","size","interpolatenumber"]
# changenamelist=["improvefeedback_plus","improvefeedback_minus",\
#             "spacedensity","intparamater","phasereverseparamater","duplicateparamater",\
#              "digt_EMT_phase","digt_EMT_intensity"]
fixdatalist=[m,mdigital,zstart,zend,ntfftx,ntffty,bion_focus,\
            fieldx,fieldy,xstart,ystart,Azstart,Azend,Antfftx,Antffty,fieldx,\
            improveparamater,size,interpolatenumber]
# changedatalist=[improvefeedback_plus,improvefeedback_minus,spacedensity,\
#     intparamater,phasereverseparamater,duplicateparamater,digt_EMT_phase,digt_EMT_intensity]




class Para:
    def __init__(self,data_set_list,data_set_name_list):
        self.data_set_list=data_set_list
        self.data_set_name_list=data_set_name_list

    def bash_pmgo(self):
        for cm in range(1,int(improveparamater)+1):
            folder=r"{0}".format(current)
            foldername=current+sr+str(cm)
            cmd = f"mkdir {foldername}"
            sp.run(cmd,shell=True,cwd=folder)

            folder=r"{0}/{1}".format(current,str(cm))

            f = open(datapy,'w')
            for i in range(0,len(self.data_set_list)):
                f.write(f"{self.data_set_name_list[i]} = {self.data_set_list[i]}\n")
            f.write("digtalnumber='0.1 0.9 1 180 60 3'\n")

            f.write("yy = '{0}'\n".format(yy))

            f.write("foldername = '{0}'\n".format(foldername))
            f.write("current = '{0}'\n".format(current))
            f.write("paramaternumber = {0}\n".format(str(cm)))

            f.close()
            folder=r"{0}".format(current)
            cmd = "cp -p {0} {1}".format(datapy,foldername)
            sp.run(cmd,shell=True,cwd=folder)
            for i in range(len(cplist)):
                cmd = "cp -p {0} {1}".format(cplist[i],foldername)
                sp.run(cmd,shell=True,cwd=folder)


            folder=r"{0}".format(foldername)
            cmd = 'sed -i -e "s*foldername*{0}*g" {1}'.format(foldername,single_sh)
            sp.run(cmd,shell=True,cwd=folder)

    def bash_pmdone(self):
        pmcont=[]
        for i in range(1,int(improveparamater)+1):

            cmd = "bash {}".format(single_sh)
            folder=r"{0}/{1}".format(current,str(i))
            pm = sp.Popen(cmd,shell=True,cwd=folder)
            pmcont.append(pm)
        if __name__ == '__main__':
            commandwait(pmcont)

    def bash_resdone(self):
        for i in range(1,int(improveparamater)+1):
            directory = save + under + str(i)
            cmd = "bash {}".format(resolution_sh)
            folder=r"{0}/{1}".format(current,directory)
            sp.run(cmd,shell=True,cwd=folder)

        


    def compare(self):
        folder=r"{0}".format(current)
        cmd = "python {0}".format(best_d_py)
        sp.run(cmd,shell=True,cwd=folder)

        cmd = "python {0}".format(comparepy)
        sp.run(cmd,shell=True,cwd=folder)

XX=Para(fixdatalist,fixnamelist)
XX.bash_pmgo()
XX.bash_pmdone()
XX.bash_resdone()
#XX.compare()

