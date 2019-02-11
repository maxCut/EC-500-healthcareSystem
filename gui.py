from tkinter import *
from data import data_pull
from error_handler import Error_Handler
from error_handler import check_hr 
from error_handler import check_bo
from error_handler import check_bp
from alert_system  import page_doctor
from datastore import insertData 
import time
import random

# Time intervals for retrieving data
hr_interval = 5
bp_interval = 5
bo_interval = 5
TimeCount = 0

# Current vital statuses
heartRate = 0
bloodPressure = 0
bloodOxygen = 0

min_int = 5


# current p_id
p_id = random.randint(0,10000)

# Run the UI
def runUI():

    window = Tk()
    
    hr = IntVar()
    bp = IntVar()
    bo = IntVar()

    window.title("Patient : " + str(p_id))
    
    label1 = Label(window, text='Heart Rate')
    label1.grid(row=0, column=0)

    textBox1 = Label(window, height=2, width=10, textvariable = hr)
    textBox1.grid(row=1, column=0)
    
    label2 = Label(window, text='Blood Pressure')
    label2.grid(row=0, column=1)

    textBox2 = Label(window, height=2, width=10, textvariable = bp)
    textBox2.grid(row=1, column=1)

    label3 = Label(window, text='Blood Oxygen')
    label3.grid(row=0, column=2)

    textBox3 = Label(window, height=2, width=10, textvariable = bo)
    textBox3.grid(row=1, column=2)
    
    def dataLoop():
        getDataLoop(hr, bp, bo)
        window.after(min_int * 1000, dataLoop)
    
    window.after(min_int * 1000, dataLoop)

    window.mainloop()

# Grab data every n seconds
# Where n is minimum time interval given
def getDataLoop(hr, bp, bo):
    global TimeCount
    min_int = min(hr_interval, bp_interval, bo_interval)
    data_obj = data_pull()

    
    if(TimeCount%hr_interval==0):
        hr.set(data_obj.get("heart_rate"))
    if(TimeCount%bp_interval==0):
        bp.set(data_obj.get("blood_pressure1"))
    if(TimeCount%bo_interval==0):
        bo.set(data_obj.get("blood_oxygen"))


    #check if we need to page doc
    if(Error_Handler(data_obj)):
        page_doctor(data_obj,0x01,check_hr(data_obj))
        page_doctor(data_obj,0x02,check_bp(data_obj))
        page_doctor(data_obj,0x03,check_bo(data_obj))

    #store the data
    insertData(p_id,data_obj)

    


#def change_interval(time, type):


def main():
    runUI()

if __name__ == "__main__":
    main()
