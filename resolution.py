import bion_resolution as bion
# bion.csv_to_np()
# bion.csv_to_np_Analog()

arrdata=bion.load_np()
arrdata_A=bion.load_np_Analog()
# arrnor=bion.np_normalization(arrdata)
# arrnor_A=bion.np_normalization(arrdata_A)
# arrinter=bion.interpolate(arrdata)
# arrinter_A=bion.interpolate(arrdata_A)
# arrdata_A=arrinter_A
# arrdata=arrinter
seedfirstname="SEED"
seedbeforename="Sbase"
arr_csv = "Graphic_inter.csv"
arr_html = "Graphic_inter.html"
arr_html_A = "Graphic_inter_A.html"

#sild_Graphic

slid_html_name="Graphic_slid.html"
slidcut=10

bion.plot_slid(arrdata,slid_html_name,slidcut)

bion.plot_slid_x(arrdata,slid_html_name,slidcut)
bion.plot_slid_y(arrdata,slid_html_name,slidcut)

slid_html_name="Graphic_slid_A.html"
slidcut=10

bion.plot_slid(arrdata_A,slid_html_name,slidcut)

bion.plot_slid_x(arrdata_A,slid_html_name,slidcut)
bion.plot_slid_y(arrdata_A,slid_html_name,slidcut)



pointcut=10
arr_csv="plot_D.csv"
bion.arr_to_csv(arrdata,arr_csv,pointcut)
plot=bion.Change(arr_html,arr_csv)
plot.plot_csv()

arr_csv="plot_A.csv"
bion.arr_to_csv(arrdata_A,arr_csv,pointcut)
plot=bion.Change(arr_html_A,arr_csv)
plot.plot_csv()

