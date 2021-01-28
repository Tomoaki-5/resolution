import math
import numpy as np
import data
import csv
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import math
import f2py_module
lamda=0.365


def spacenum(start,end,sp):
    s=(end-start)/sp
    s_num=math.floor(s)
    return s_num


Azstart=data.Azstart
Azend=data.Azend
ntfftx=data.ntfftx
ntffty=data.ntffty
mdigital=data.mdigital
mult=data.m
m=data.m
bion_focus=data.bion_focus
fieldx=data.fieldx
fieldy=data.fieldy
field=data.fieldx
spacedensity=1
duplicateparamater=0.01
phasereverseparamater=1
intparamater=0.1
improveth_plus=0.1
improveth_minus=0.01

xstart=data.xstart
ystart=data.ystart
interpolatenumber=data.interpolatenumber
size=data.size
zlength=Azend-Azstart

improvefeedback_plus=0.67
improvefeedback_minus=0.33
space=field/(ntfftx*interpolatenumber)

mseed=spacenum(0,zlength,space)
intfftx=ntfftx*interpolatenumber
intffty=ntffty*interpolatenumber
xend=xstart+fieldx
yend=ystart+fieldy


paralistlen=8
randomseed=1
stoptrans1 = 0.2
stoptrans2 = 0.6
decnum = 0.1
transmax=0.95
randomseeed=1
pointcut = 3

def remove_extension(filename):
    remove_extension_name = filename.split('.')[0]
    return remove_extension_name

def phasefct(z,phasenum):

    ph=360*z/lamda
    if phasenum % phasereverseparamater == 0:
        ph = ph + 180
    pha = ph % 360
    return pha




def NAfct(z):
    if z == 0:
        return 1
    if z !=0:
        c1 = math.sin(fieldx/2/(z)) 
        return c1

def intfunction(z):
    c2 = 0.95 - z*intparamater
    return c2

def digitxy(c1,start,end,mult):
    width=(end-start)/mult
    c2 = c1 - start
    q = c2 // width
    return int(q)
    # dig1=start-width*3/2
    # for i in range(mult+1):
    #     dig1=dig1+width
    #     dig2=dig1+width
    #     if dig1<c1<=dig2:
    #         return i
        
        
def digitz(cz,start,end,mult):
    width=(end-start)/(mult-1)
    q = (mult-1)-cz // width  
    return int(q)
    # dig1=end+width*3/2
    # for i in range(mult+1):
    #     dig1=dig1-width
    #     dig2=dig1-width
    #     if dig2<cz<=dig1:
    #         return i
def phasefct_for_improve(z):
    #lamda=0.365
    ph=360*z/lamda
    pha = ph % 360
    return pha

def rotx(x,y,z,arg):
    xr=x
    yr=y*math.cos(math.radians(arg))+z*math.sin(math.radians(arg))
    zr=(-1)*y*math.sin(math.radians(arg))+z*math.cos(math.radians(arg))
    return xr,yr,zr
def roty(x,y,z,arg):
    xr=x*math.cos(math.radians(arg))-z*math.sin(math.radians(arg))
    yr=y
    zr=x*math.sin(math.radians(arg))+z*math.cos(math.radians(arg))
    return xr,yr,zr
def rotz(x,y,z,arg):
    xr=x*math.cos(math.radians(arg))+y*math.sin(math.radians(arg))
    yr=(-1)*x*math.sin(math.radians(arg))+y*math.cos(math.radians(arg))
    zr=z
    return xr,yr,zr


def arr_to_csv(arr,csvname,pointcut):
    arrmax=np.max(arr)
    xend=xstart+fieldx
    yend=ystart+fieldy
    f2py_module.arr2csv(arr,xstart,xend,ystart,yend,Azstart,Azend,arrmax,csvname,pointcut)


def seedcsv_to_plotcsv(seedcsv,seedname,basetxt,plotcsv):
    f2py_module.arrraw(seedcsv,xstart,xend,ntfftx+1,ystart,yend,ntffty+1,Azstart,Azend,mseed+1,\
    bion_focus,duplicateparamater,\
    phasereverseparamater,size,intparamater,randomseeed,transmax,spacedensity,seedname,basetxt,plotcsv)

def seedtxt_to_plotcsv(txtname,plot_csvname):
    f2py_module.txt2csv_for_seed(txtname,plot_csvname)


def interpolate(arr):
    zmp = int(mseed/(mdigital-1))
    arr_inter=f2py_module.interpolate(arr,interpolatenumber,zmp)
    return arr_inter
# def interpolatefunction(arr):
    

#     zm=arr[0][0].shape
#     zmp=int(mseed/(zm[0]-1))

#     qq=arr
#     arrinter=f2p_module.interpolate(qq,interpolatenumber,zmp)

#     return arrinter


def csv_to_np():
    cont=[]
    for num in range(1,mdigital+1):
        numz = str(num).zfill(3)
        
        filename = "3D-test_GD{0}.csv".format(numz)
        columns = np.arange(1,ntfftx+2)
        arr = np.loadtxt(filename, delimiter=",", skiprows=1,usecols=columns) 
        cont.append(arr)
    arr3=np.dstack(cont)
    np.save('np_saveD_before.npy' , arr3)


def csv_to_np_Analog():
    ntfftx=data.Antfftx
    ntffty = data.Antffty
    cont=[]
    for num in range(3,m+3):
        numz = str(num).zfill(3)
        
        filename = "3D-test_GA{0}.csv".format(numz)
        columns = np.arange(1,ntfftx+2)
        arr = np.loadtxt(filename, delimiter=",", skiprows=1,usecols=columns) 
        cont.append(arr)
    arr2=np.dstack(cont)
    np.save('np_saveA_Graphic.npy' , arr2)




def load_np():
    arr = np.load('np_saveD_before.npy')
    arrmax=np.max(arr)
    arrmin=np.min(arr)
    with open('max_min.csv','w') as re:
        re.write("max,min\n")
        re.write("{0},{1}\n".format(arrmax,arrmin))   
        re.close()
    return arr


def load_np_Analog():
    arr = np.load('np_saveA_Graphic.npy')
    arrmax=np.max(arr)
    arrmin=np.min(arr)
    with open('max_min_A.csv','w') as re:
        re.write("max,min\n")
        re.write("{0},{1}\n".format(arrmax,arrmin))   
        re.close()
    return arr


def np_normalization(arr):
    arrn = f2py_module.arr2normalization(arr)
    return arrn


def plot_slid(arr3n,htmlname,slidcut):

    filename = remove_extension(htmlname)
    slidcut=int(slidcut)
    arrmax=np.max(arr3n)
    arrS = arr3n.shape
    ntfftx = arrS[0]-1
    ntffty = arrS[1]-1
    mdigital = arrS[2]

    volume = arr3n.T
    r, c = volume[0].shape

    # Define frames

    nb_frames = mdigital

    fig = go.Figure(frames=[go.Frame(data=go.Surface(
        z=((-1)*Azstart-k*(Azend-Azstart)/(mdigital-1)) * np.ones((r, c)),
        surfacecolor=np.flipud(volume[k]),
        cmin=arrmax/slidcut, cmax=arrmax
        ),
        name=str(k) # you need to name the frame for the animation to behave properly
        )
        for k in range(nb_frames)])

    # Add data to be displayed before animation starts
    fig.add_trace(go.Surface(
        z=((-1)*Azstart) * np.ones((r, c)),
        surfacecolor=np.flipud(volume[mdigital-1]),
        colorscale= [[0, 'navy'],[0.2,'navy'] ,[0.2, 'rgb(153,255,255)'],[0.334,'rgb(153,255,255)'],[0.334,'green'],\
            [0.667,'green'],[0.667,'red'],[1,'red']],
        cmin=arrmax/slidcut, cmax=arrmax,
        colorbar=dict(thickness=20, ticklen=4)
        ))


    def frame_args(duration):
        return {
                "frame": {"duration": duration},
                "mode": "immediate",
                "fromcurrent": True,
                "transition": {"duration": duration, "easing": "linear"},
            }

    sliders = [
                {
                    "pad": {"b": 10, "t": 60},
                    "len": 0.9,
                    "x": 0,
                    "y": 0,
                    "steps": [
                        {
                            "args": [[f.name], frame_args(0)],
                            "label": str(k),
                            "method": "animate",
                        }
                        for k, f in enumerate(fig.frames)
                    ],
                }
            ]

    # Layout
    fig.update_layout(
            title='Slices in volumetric data',
            width=600,
            height=600,
            
            scene=dict(xaxis=dict(
                            ticktext= ['{}'.format(xstart),'{}'.format(xstart+field/4),'{}'.format(xstart+field/2),'{}'.format(xstart+3*field/4),\
                                '{}'.format(xstart+field)],
                            tickvals= [0,ntfftx/4,ntfftx/2,3*ntfftx/4,ntfftx]),
                        yaxis=dict(
                            ticktext= ['{}'.format(ystart),'{}'.format(ystart+field/4),'{}'.format(ystart+field/2),'{}'.format(ystart+3*field/4),\
                                '{}'.format(ystart+field)],
                            tickvals= [0,ntffty/4,ntffty/2,3*ntffty/4,ntffty]),
                        zaxis=dict(range=[(-1)*Azstart,(-1)*Azend], autorange=True),
                        aspectratio=dict(x=1, y=1, z=1),
                        ),
            updatemenus = [
                {
                    "buttons": [
                        {
                            "args": [None, frame_args(mdigital-1)],
                            "label": "&#9654;", # play symbol
                            "method": "animate",
                        },
                        {
                            "args": [[None], frame_args(0)],
                            "label": "&#9724;", # pause symbol
                            "method": "animate",
                        },
                    ],
                    "direction": "left",
                    "pad": {"r": 10, "t": 70},
                    "type": "buttons",
                    "x": 0,
                    "y": 0,
                }
            ],
        
            sliders=sliders
    )

    fig.write_html("{0}.html".format(filename))


def plot_slid_x(arr3n,htmlname,slidcut):

    filename = remove_extension(htmlname)
    slidcut=int(slidcut)
    arrmax=np.max(arr3n)
    arrS = arr3n.shape
    ntfftx = arrS[0]-1
    ntffty = arrS[1]-1
    mdigital = arrS[2]
    x0 = xstart
    y0 = ystart
    # for l in range(10):
    #     if np.count_nonzero(arr3n > l/10) > 0:
    #         mmax=l
    #         break
    arr3n=arr3n.transpose(2,1,0)

    volume = arr3n.T
    r, c = volume[0].shape

    # Define frames
    nb_frames = ntfftx+1

    fig = go.Figure(frames=[go.Frame(data=go.Surface(
        z=(x0+k*(field)/(ntfftx)) * np.ones((r, c)),
        surfacecolor=np.flipud(volume[k]),
        cmin=arrmax/slidcut, cmax=arrmax
        ),
        name=str(k) # you need to name the frame for the animation to behave properly
        )
        for k in range(nb_frames)])

    # Add data to be displayed before animation starts
    fig.add_trace(go.Surface(
        z=(x0) * np.ones((r, c)),
        surfacecolor=np.flipud(volume[ntfftx]),
        colorscale= [[0, 'navy'],[0.2,'navy'] ,[0.2, 'rgb(153,255,255)'],[0.334,'rgb(153,255,255)'],[0.334,'green'],\
            [0.667,'green'],[0.667,'red'],[1,'red']],
        cmin=arrmax/slidcut, cmax=arrmax,
        colorbar=dict(thickness=20, ticklen=4)
        ))


    def frame_args(duration):
        return {
                "frame": {"duration": duration},
                "mode": "immediate",
                "fromcurrent": True,
                "transition": {"duration": duration, "easing": "linear"},
            }

    sliders = [
                {
                    "pad": {"b": 10, "t": 60},
                    "len": 0.9,
                    "x": 0,
                    "y": 0,
                    "steps": [
                        {
                            "args": [[f.name], frame_args(0)],
                            "label": str(k),
                            "method": "animate",
                        }
                        for k, f in enumerate(fig.frames)
                    ],
                }
            ]

    # Layout
    fig.update_layout(
            title='Slices in volumetric data',
            width=600,
            height=600,

            scene=dict(zaxis=dict(
                            ticktext= ['{}'.format(x0),'{}'.format(x0+field/4),'{}'.format(x0+field/2),'{}'.format(x0+3*field/4),'{}'.format(x0+field)],
                            #tickvals= [0,ntfftx/4,ntfftx/2,3*ntfftx/4,ntfftx],
                            autorange=True,
                            range=[0,ntfftx]),
                        yaxis=dict(
                            ticktext= ['{}'.format(y0),'{}'.format(y0+field/4),'{}'.format(y0+field/2),'{}'.format(y0+3*field/4),'{}'.format(y0+field)],
                            tickvals= [0,ntffty/4,ntffty/2,3*ntffty/4,ntffty],
                            ),
                        xaxis=dict(
                            ticktext= ['{}'.format((-1)*Azend+(Azend-Azstart)),'{}'.format((-1)*Azend+3*(Azend-Azstart)/(4)),'{}'.format((-1)*Azend+(Azend-Azstart)/2),'{}'.format((-1)*Azend+(Azend-Azstart)/4),'{}'.format((-1)*Azend)],
                            tickvals= [0,round((mdigital-1)/4),round((mdigital-1)/2),round(3*(mdigital-1)/4),mdigital-1]),
                        xaxis_title='Z_AXIS',
                        yaxis_title='Y_AXIS',
                        zaxis_title='X_AXIS',

                        aspectratio=dict(x=1, y=1, z=1),
                        ),
        
    #          scene=dict(
    #                     yaxis=dict(
    #                         ticktext = ["-32","-16","0","16","32"],
    #                         tickvals = [0,64,128,192,256]),
    #                     xaxis=dict(
    #                         ticktext= ["-40","-20","0","20","40","60"],
    #                         tickvals= [0,10,20,30,40,50]),
    #                     zaxis
    #                     aspectratio=dict(x=1, y=1, z=1),
    #                     ),
            updatemenus = [
                {
                    "buttons": [
                        {
                            "args": [None, frame_args(ntffty)],
                            "label": "&#9654;", # play symbol
                            "method": "animate",
                        },
                        {
                            "args": [[None], frame_args(0)],
                            "label": "&#9724;", # pause symbol
                            "method": "animate",
                        },
                    ],
                    "direction": "left",
                    "pad": {"r": 10, "t": 70},
                    "type": "buttons",
                    "x": 0,
                    "y": 0,
                }
            ],
        
            sliders=sliders
    )
    fig.write_html("{0}_X.html".format(filename))


def plot_slid_y(arr3n,htmlname,slidcut):

    filename = remove_extension(htmlname)
    slidcut=int(slidcut)
    arrmax=np.max(arr3n)
    arrS = arr3n.shape
    ntfftx = arrS[0]-1
    ntffty = arrS[1]-1
    mdigital = arrS[2]
    x0 = xstart
    y0 = ystart

    arr3n=arr3n.transpose(0,2,1)

    volume = arr3n.T
    r, c = volume[0].shape

    # Define frames
    nb_frames = ntffty+1

    fig = go.Figure(frames=[go.Frame(data=go.Surface(
        z=(y0+k*(field)/(ntffty)) * np.ones((r, c)),
        surfacecolor=np.flipud(volume[k]),
        cmin=arrmax/slidcut, cmax=arrmax
        ),
        name=str(k) # you need to name the frame for the animation to behave properly
        )
        for k in range(nb_frames)])

    # Add data to be displayed before animation starts
    fig.add_trace(go.Surface(
        z=(y0) * np.ones((r, c)),
        surfacecolor=np.flipud(volume[ntffty]),
        colorscale= [[0, 'navy'],[0.2,'navy'] ,[0.2, 'rgb(153,255,255)'],[0.334,'rgb(153,255,255)'],[0.334,'green'],\
            [0.667,'green'],[0.667,'red'],[1,'red']],
        cmin=arrmax/slidcut, cmax=arrmax,
        colorbar=dict(thickness=20, ticklen=4)
        ))


    def frame_args(duration):
        return {
                "frame": {"duration": duration},
                "mode": "immediate",
                "fromcurrent": True,
                "transition": {"duration": duration, "easing": "linear"},
            }

    sliders = [
                {
                    "pad": {"b": 10, "t": 60},
                    "len": 0.9,
                    "x": 0,
                    "y": 0,
                    "steps": [
                        {
                            "args": [[f.name], frame_args(0)],
                            "label": str(k),
                            "method": "animate",
                        }
                        for k, f in enumerate(fig.frames)
                    ],
                }
            ]

    # Layout
    fig.update_layout(
            title='Slices in volumetric data',
            width=600,
            height=600,

            scene=dict(xaxis=dict(
                            ticktext= ['{}'.format(x0),'{}'.format(x0+field/4),'{}'.format(x0+field/2),'{}'.format(x0+3*field/4),'{}'.format(x0+field)],
                            tickvals= [0,ntfftx/4,ntfftx/2,3*ntfftx/4,ntfftx]),
                        zaxis=dict(
                            ticktext= ['{}'.format(y0),'{}'.format(y0+field/4),'{}'.format(y0+field/2),'{}'.format(y0+3*field/4),'{}'.format(y0+field)],
                            #tickvals= [0,ntffty/4,ntffty/2,3*ntffty/4,ntffty],
                            autorange=True,
                            range=[0,ntffty]),
                        yaxis=dict(
                            ticktext= ['{}'.format((-1)*Azend+(Azend-Azstart)),'{}'.format((-1)*Azend+3*(Azend-Azstart)/(4)),'{}'.format((-1)*Azend+(Azend-Azstart)/2),'{}'.format((-1)*Azend+(Azend-Azstart)/4),'{}'.format((-1)*Azend)],
                            tickvals= [0,round((mdigital-1)/4),round((mdigital-1)/2),round(3*(mdigital-1)/4),mdigital-1]),
                        xaxis_title='X_AXIS',
                        yaxis_title='Z_AXIS',
                        zaxis_title='Y_AXIS',

                        aspectratio=dict(x=1, y=1, z=1),
                        ),
        
    #          scene=dict(
    #                     yaxis=dict(
    #                         ticktext = ["-32","-16","0","16","32"],
    #                         tickvals = [0,64,128,192,256]),
    #                     xaxis=dict(
    #                         ticktext= ["-40","-20","0","20","40","60"],
    #                         tickvals= [0,10,20,30,40,50]),
    #                     zaxis
    #                     aspectratio=dict(x=1, y=1, z=1),
    #                     ),
            updatemenus = [
                {
                    "buttons": [
                        {
                            "args": [None, frame_args(ntfftx)],
                            "label": "&#9654;", # play symbol
                            "method": "animate",
                        },
                        {
                            "args": [[None], frame_args(0)],
                            "label": "&#9724;", # pause symbol
                            "method": "animate",
                        },
                    ],
                    "direction": "left",
                    "pad": {"r": 10, "t": 70},
                    "type": "buttons",
                    "x": 0,
                    "y": 0,
                }
            ],
        
            sliders=sliders
    )
    fig.write_html("{0}_Y.html".format(filename))






class Change:
    def __init__(self,name,plotdata):
        self.name=name
        self.plotdata=plotdata

    def arr_to_csv(self,pointcut):
        arr=self.plotdata
        arrmax=np.max(arr)
        xend=xstart+fieldx
        yend=ystart+fieldy
        f2py_module.arr2csv(arr,xstart,xend,ystart,yend,Azstart,Azend,arrmax,self.name,pointcut)


    def plot_csv(self):
        plotcsv="PLOT.csv"
        htmlname = remove_extension(self.name)

        f2py_module.csv2plot(self.plotdata,plotcsv)
        df = pd.read_csv('{0}'.format(plotcsv))

        fig = go.Figure(data=go.Scatter3d(
            x=df['x'],
            y=df['y'],
            z=df['z'],
            mode='markers',
            marker=dict(
                sizemode='diameter',
            line=dict(width=0),
                sizeref=0.3,
                size=df['size'],
                color = df['int'],
                colorscale= [[0, 'rgb(153,255,255)'],[0.2,'rgb(153,255,255)'] ,[0.2, 'navy'],[0.334,'navy'],[0.334,'green'],\
                    [0.667,'green'],[0.667,'red'],[1,'red']],
                # colorscale= [[0, 'navy'],[0.3,'navy'],[0.3,'red'],[1,'red']],
                # colorscale= [[0, 'rgb(255,255,255)'], [0.67, 'rgb(255,255,0)'],[0.8,'rgb(255,0,0)']],
                # colorscale= [[0, 'rgb(0,0,128)'],[0.1,'rgb(0,0,255)'] ,[0.2, 'rgb(0,128,128)'],
                #             [0.3, 'rgb(0,128,0)'], [0.5, 'rgb(0,255,0)'], [0.7, 'rgb(255,255,0)'],\
                #             [1, 'rgb(255,0,0)']],
                #         [0.6, 'rgb(255,241,0)'], [0.7, 'rgb(243,152,0)'], [0.8, 'red']],                # colorscale= [[0, 'rgb(29,32,136)'], [0.1, 'rgb(0,104,183)'], [0.2, 'rgb(0,160,233)'],\
                #     [0.3, 'rgb(0,158,150)'], [0.4, 'rgb(0,153,68)'], [0.5, 'rgb(143,195,31)'],\
                #         [0.6, 'rgb(255,241,0)'], [0.7, 'rgb(243,152,0)'], [0.8, 'red']],
                colorbar_title = 'Light<br>Intensity',
                opacity = 0.3,
            )
        ))


        fig.update_layout(scene=dict(
                        xaxis=dict(range=[xstart,xstart+field], autorange=False),
                        yaxis=dict(range=[ystart,ystart+field], autorange=False),
                        zaxis=dict(range=[(-1)*Azstart, (-1)*Azend], autorange=False),
                        aspectratio=dict(x=1, y=1, z=1)
                                    )
                        )
        fig.write_html("{0}.html".format(htmlname))


    def plot_csv_minus(self):
        plotcsv="PLOT_minus.csv"
        htmlname = remove_extension(self.name)

        f2py_module.csv2plot_minus(self.plotdata,plotcsv)
        df = pd.read_csv('{0}'.format(plotcsv))

        fig = go.Figure(data=go.Scatter3d(
            x=df['x'],
            y=df['y'],
            z=df['z'],
            mode='markers',
            marker=dict(
                sizemode='diameter',
            line=dict(width=0),
                sizeref=0.4,
                size=df['size'],
                color = df['int'],
                colorscale= [[0, 'rgb(0,0,128)'], [0.2, 'yellow'], [1.0, 'red']],
                colorbar_title = 'Light<br>Intensity',
                opacity = 0.7,
            )
        ))


        fig.update_layout(scene=dict(
                        xaxis=dict(range=[xstart,xstart+field], autorange=False),
                        yaxis=dict(range=[ystart,ystart+field], autorange=False),
                        zaxis=dict(range=[(-1)*Azstart, (-1)*Azend], autorange=False),
                        aspectratio=dict(x=1, y=1, z=1)
                                    )
                        )
        fig.write_html("{0}.html".format(htmlname))

    def plot_csv_plus(self):
        plotcsv="PLOT_plus.csv"
        htmlname = remove_extension(self.name)
        f2py_module.csv2plot_plus(self.plotdata,plotcsv)
        df = pd.read_csv('{0}'.format(plotcsv))

        fig = go.Figure(data=go.Scatter3d(
            x=df['x'],
            y=df['y'],
            z=df['z'],
            mode='markers',
            marker=dict(
                sizemode='diameter',
            line=dict(width=0),
                sizeref=0.4,
                size=df['size'],
                color = df['int'],
                colorscale= [[0, 'rgb(0,0,128)'], [0.2, 'yellow'], [1.0, 'red']],
                colorbar_title = 'Light<br>Intensity',
                opacity = 0.7,
            )
        ))


        fig.update_layout(scene=dict(
                        xaxis=dict(range=[xstart,xstart+field], autorange=False),
                        yaxis=dict(range=[ystart,ystart+field], autorange=False),
                        zaxis=dict(range=[(-1)*Azstart, (-1)*Azend], autorange=False),
                        aspectratio=dict(x=1, y=1, z=1)
                                    )
                        )
        fig.write_html("{0}.html".format(htmlname))




    def plot_txt(self):

        htmlname = remove_extension(self.name)
        df =  pd.read_csv('{0}'.format(self.plotdata))

        fig = go.Figure(data=go.Scatter3d(
            x=df['x'],
            y=df['y'],
            z=df['z'],
            mode='markers',
            marker=dict(
                sizemode='diameter',
                line=dict(width=0),
                sizeref=0.4,
                size=df['size'],
                color = df['int'],
                colorscale= [[0, 'rgb(0,0,128)'], [0.2, 'yellow'], [1.0, 'red']],
                colorbar_title = 'Light<br>Intensity',
                opacity = 0.7,
            )
        ))


        fig.update_layout(scene=dict(
                        xaxis=dict(range=[xstart,xstart+field], autorange=False),
                        yaxis=dict(range=[ystart,ystart+field], autorange=False),
                        zaxis=dict(range=[(-1)*Azstart, (-1)*Azend], autorange=False),
                        aspectratio=dict(x=1, y=1, z=1)
                                    )
                        )
        fig.write_html("{0}_INT.html".format(htmlname))

        fig = go.Figure(data=go.Scatter3d(
            x=df['x'],
            y=df['y'],
            z=df['z'],
            mode='markers',
            marker=dict(
                sizemode='diameter',
                line=dict(width=0),
                sizeref=0.4,
                size=df['size'],
                color = df['phase'],
                colorscale= [[0, 'rgb(0,0,128)'], [0.2, 'yellow'], [1.0, 'red']],
                colorbar_title = 'Light<br>Intensity',
                opacity = 0.7,
            )
        ))


        fig.update_layout(scene=dict(
                        xaxis=dict(range=[xstart,xstart+field], autorange=False),
                        yaxis=dict(range=[ystart,ystart+field], autorange=False),
                        zaxis=dict(range=[(-1)*Azstart, (-1)*Azend], autorange=False),
                        aspectratio=dict(x=1, y=1, z=1)
                                    )
                        )
        fig.write_html("{0}_PHASE.html".format(htmlname))




def dc(a,b):
    dd=a
    if a>=b:
        dd=b
    if a<=0:
        dd=0
    return int(dd)


class Improve:
    def __init__(self,firstseed,beforeseed,afterseed,arr,impnum,eva_csv,arr_csv):
        self.firstseed=firstseed
        self.beforeseed=beforeseed
        self.afterseed=afterseed
        self.arr=arr
        self.impnum=impnum
        self.eva_csv=eva_csv
        self.arr_csv = arr_csv
    
    def evaluation(self):
        
        xend=xstart+fieldx
        yend=ystart+fieldy
        internum=interpolatenumber
        zm=self.arr[0][0].shape
        zmp=int(mseed/(zm[0]-1))
        minus_th=improveth_minus
        plus_th=improveth_plus
        f_plus = improvefeedback_plus
        f_minus = improvefeedback_minus
        impnum = self.impnum
        focus = bion_focus
        dupnum = duplicateparamater
        patternsize = size
        sp1 = stoptrans1
        sp2 = stoptrans2
        phasereverse = phasereverseparamater
        paralist=f2py_module.output2improve(self.arr,self.firstseed,self.beforeseed,self.afterseed,xstart,xend,ystart,yend,Azstart,Azend\
                                    ,internum,zmp,minus_th,plus_th,\
                                f_plus,f_minus,impnum,focus,dupnum,patternsize,sp1,sp2,decnum,phasereverse,randomseed,\
                                paralistlen,self.eva_csv,self.arr_csv,pointcut)
            
    #     arrfirst=f2p_module.seedtxt2arr(self.firstseed,xstart,xend,intfftx+1,ystart,yend,intffty+1,Azstart,Azend,mseed+1)

    #     arrbefore=f2p_module.seedtxt2arr(self.beforeseed,xstart,xend,intfftx+1,ystart,yend,intffty+1,Azstart,Azend,mseed+1)

        
    #     arr_inter_nor=self.arr_interpolate_normalization
    #     arreee=f2p_module.arr2eva(arrfirst,arr_inter_nor,improveth_minus)
    #     paralist=f2p_module.paramaterget(arrfirst,arr_inter_nor,paralistlen,improveth_minus)
        seed_number = paralist[0]+paralist[1]
        number = paralist[2]+paralist[3]
        if paralist[4] >= abs(paralist[5]):
            gosa = paralist[4]
        if paralist[4] < abs(paralist[5]):
            gosa = paralist[5]
        siguma = paralist[6] + paralist[7]


    #     arrimp=f2p_module.arr2imp(arrfirst,arrbefore,arr_inter_nor,improveth_plus,improveth_minus,improvefeedback_plus,improvefeedback_minus,self.impnum)

    #     f2p_module.imp2txt(arrimp,xstart,xend,ystart,yend,Azstart,Azend,bion_focus,duplicateparamater,\
    #     phasereverseparamater,size,randomseeed,stoptrans1,stoptrans2,decnum,self.afterseed)

        
        result_csv="result.csv"
        with open(result_csv,'w') as re:
            re.write("seed_number,seed_number_plus,seed_number_minus\n")
            re.write("{0},{1},{2}\n".format(seed_number,paralist[0],paralist[1]))
            re.write("number,number_plus,number_minus\n")
            re.write("{0},{1},{2}\n".format(number,paralist[2],paralist[3]))
            re.write("siguma,siguma_plus,siguma_minus\n")
            re.write("{0},{1},{2}\n".format(siguma,paralist[6],paralist[7]))
            re.write("gosa,plusgosa,minusgosa\n")
            re.write("{0},{1},{2}\n".format(gosa,paralist[4],paralist[5]))   
            re.close()
    #     eva_csvname='Evaluation.csv'
    #     f2p_module.arreee2csv(arreee,xstart,xend,ystart,yend,Azstart,Azend,eva_csvname)
        
    def single(self):
        # paramater_name = data.paramatername
        paramater_number = data.paramaternumber
        # paramater_change = data.paramaterchange
        result_csv="result.csv"
        with open(result_csv,'a') as re:
            re.write("paramaternumber\n")
            re.write("{0}\n".format(paramater_number))       
            re.close()
