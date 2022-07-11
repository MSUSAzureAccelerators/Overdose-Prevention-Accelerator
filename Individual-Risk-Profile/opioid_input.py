# Check for pandas and matplotlib
# If not installed, install using pip (REQUIRES HOST MACHINE TO HAVE PIP
#   ALREADY; can be specified as part of Python.exe command line install)
import subprocess
import sys

def import_or_install(package):
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

import_or_install("pandas")
import_or_install("matplotlib")

# Import module
#from cgitb import text
#from ipaddress import collapse_addresses
#from wsgiref import validate
import pandas as pd
import tkinter as tk
from tkinter import *
from tkinter import ttk

# Create object
root = Tk()

# Name the Window
root.title("Example Form")

# Adjust size
root.geometry("1100x810")

# Set column span for controls that utilize it
# submit button uses spanCol+1 because it doesn't have a label taking up a column
spanCol = 4

# Validate input for iralcage
def validate_iralcage(user_input):
    # check if the input is numeric
    if  user_input.isdigit():
        # Fetching minimum and maximum value of the spinbox
        minval = int(root.nametowidget(iralcage_sbx).config('from')[4])
        maxval = int(root.nametowidget(iralcage_sbx).config('to')[4]) + 1
 
        # check if the number is within the range
        if int(user_input) not in range(minval, maxval):
            return False
 
        # Printing the user input to the console
        return True
 
    # if input is blank string
    elif user_input == "":
        return True
 
    # return false is input is not numeric
    else:
        return False

#Validate input for cigage
def validate_cigage(user_input):
    # check if the input is numeric
    if  user_input.isdigit():
        # Fetching minimum and maximum value of the spinbox
        minval = int(root.nametowidget(cigage_sbx).config('from')[4])
        maxval = int(root.nametowidget(cigage_sbx).config('to')[4]) + 1
 
        # check if the number is within the range
        if int(user_input) not in range(minval, maxval):
            return False
 
        # Printing the user input to the console
        return True
 
    # if input is blank string
    elif user_input == "":
        return True
 
    # return false is input is not numeric
    else:
        return False

# Validate input for iralcfy
def validate_iralcfy(user_input):
    # check if the input is numeric
    if  user_input.isdigit():
        # Fetching minimum and maximum value of the spinbox
        minval = int(root.nametowidget(iralcfy_sbx).config('from')[4])
        maxval = int(root.nametowidget(iralcfy_sbx).config('to')[4]) + 1
 
        # check if the number is within the range
        if int(user_input) not in range(minval, maxval):
            return False
 
        # Printing the user input to the console
        return True
 
    # if input is blank string
    elif user_input == "":
        return True
 
    # return false is input is not numeric
    else:
        return False

# Validate input for irmjfy
def validate_irmjfy(user_input):
    # check if the input is numeric
    if  user_input.isdigit():
        # Fetching minimum and maximum value of the spinbox
        minval = int(root.nametowidget(irmjfy_sbx).config('from')[4])
        maxval = int(root.nametowidget(irmjfy_sbx).config('to')[4]) + 1
 
        # check if the number is within the range
        if int(user_input) not in range(minval, maxval):
            return False
 
        # Printing the user input to the console
        return True
 
    # if input is blank string
    elif user_input == "":
        return True
 
    # return false is input is not numeric
    else:
        return False

# Checkbutton command for iralcage_ckb
# disables range selector if box is checked
def iralcage_onCheck():
    if iralcage_ckb_var.get() == 1:
        iralcage_sbx.config(state=tk.DISABLED)
    elif iralcage_ckb_var.get() == 0:
        iralcage_sbx.config(state=tk.NORMAL)

# Checkbutton command for cigage_ckb
# disables range slector if box is checked
def cigage_onCheck():
    if cigage_ckb_var.get() == 1:
        cigage_sbx.config(state=tk.DISABLED)
    elif cigage_ckb_var.get() == 0:
        cigage_sbx.config(state=tk.NORMAL)

# Checkbutton commands for iralcfy_ckb1 and ifalcfy_ckb2
# disable range selector if either button is checked
def iralcfy_onCheck():
    if (iralcfy_ckb1_var.get() == 1) and (iralcfy_ckb2_var.get() == 0):
        #only 'never used' is checked
        iralcfy_sbx.config(state=tk.DISABLED)
        iralcfy_ckb2.config(state=tk.DISABLED)
    elif (iralcfy_ckb1_var.get() == 0) and (iralcfy_ckb2_var.get() == 0):
        #neither are checked
        iralcfy_sbx.config(state=tk.NORMAL)
        iralcfy_ckb1.config(state=tk.NORMAL)
        iralcfy_ckb2.config(state=tk.NORMAL)
    elif (iralcfy_ckb1_var.get() == 0) and (iralcfy_ckb2_var.get() == 1):
        #only 'did not use alcohol last year' is checked
        iralcfy_sbx.config(state=tk.DISABLED)
        iralcfy_ckb1.config(state=tk.DISABLED)

# Checkbutton commands for irmjfy_ckb1 and irmjfy_ckb2
# disable range selector if either button is checked
def irmjfy_onCheck():
    if (irmjfy_ckb1_var.get() == 1) and (irmjfy_ckb2_var.get() == 0):
        #only 'never used' is checked
        irmjfy_sbx.config(state=tk.DISABLED)
        irmjfy_ckb2.config(state=tk.DISABLED)
    elif (irmjfy_ckb1_var.get() == 0) and (irmjfy_ckb2_var.get() == 0):
        #neither are checked
        irmjfy_sbx.config(state=tk.NORMAL)
        irmjfy_ckb1.config(state=tk.NORMAL)
        irmjfy_ckb2.config(state=tk.NORMAL)
    elif (irmjfy_ckb1_var.get() == 0) and (irmjfy_ckb2_var.get() == 1):
        #only 'did not use alcohol last year' is checked
        irmjfy_sbx.config(state=tk.DISABLED)
        irmjfy_ckb1.config(state=tk.DISABLED)

# Dictionaries for dropdown menus
eduhighcat_dict = {
    1 : "Less than high school",
    2 : "High school grad",
    3 : "Some college/Associate's Degree",
    4 : "College graduate",
    5 : "12 to 17 year olds"
}

age2_dict = {
    1 : "Respondent is 12 years old",
    2 : "Respondent is 13 years old",
    3 : "Respondent is 14 years old",
    4 : "Respondent is 15 years old",
    5 : "Respondent is 16 years old",
    6 : "Respondent is 17 years old",
    7 : "Respondent is 18 years old",
    8 : "Respondent is 19 years old",
    9 : "Respondent is 20 years old",
    10 : "Respondent is 21 years old",
    11 : "Respondent is 22 or 23 years old",
    12 : "Respondent is 24 or 25 years old",
    13 : "Respondent is between 26 and 29 years old",
    14 : "Respondent is between 30 and 34 years old",
    15 : "Respondent is between 35 and 49 years old",
    16 : "Respondent is between 50 and 64 years old",
    17 : "Respondent is 65 years old or older"
}

iralcrc_dict = {
    1 : "Within the past 30 days",
    2 : "More than 30 days ago but within the past 12 mos",
    3 : "More than 12 months ago",
    9 : "Never used"
}

ircigrc_dict = {
    1 : "Within the past 30 days",
    2 : "More than 30 days ago but within the past 12 mos",
    3 : "More than 12 months ago but within the past 3 yrs",
    4 : "More than 3 years ago",
    9 : "Never smoked cigarettes"
}

irmjrc_dict = {
    1 : "Within the past 30 days",
    2 : "More than 30 days ago but within the past 12 mos",
    3 : "More than 12 months ago",
    9 : "Never used marijuana"
}

ircocrc_dict = {
    1 : "Within the past 30 days",
    2 : "More than 30 days ago but within the past 12 mos",
    3 : "More than 12 months ago",
    9 : "Never used"
}

ircrkrc_dict = {
    1 : "Within the past 30 days",
    2 : "More than 30 days ago but within the past 12 most",
    3 : "More than 12 months ago",
    9 : "Never used"
}

irherrc_dict = {
    1 : "Within the past 30 days",
    2 : "More than 30 days ago but within the past 12 mos",
    3 : "More than 12 months ago",
    9 : "Never used"
}

irhallucrec_dict = {
    1 : "Within the past 30 days",
    2 : "More than 30 days ago but within the past 12 mos",
    3 : "More than 12 months ago",
    9 : "Never used"
}

irlsdrc_dict = {
    1 : "Within the past 30 days",
    2 : "More than 30 days ago but within the past 12 mos",
    3 : "More than 12 months ago",
    9 : "Never used"
}

irecstmorec_dict = {
    1 : "Within the past 30 days",
    2 : "More than 30 days ago but within the past 12 mos",
    3 : "More than 12 months ago",
    9 : "Never used"
}

irinhalrec_dict = {
    1 : "Within the past 30 days",
    2 : "More than 30 days ago but within the past 12 mos",
    3 : "More than 12 months ago",
    9 : "Never used"
}

irmethamrec_dict = {
    1 : "Within the past 30 days",
    2 : "More than 30 days ago but within the past 12 mos",
    3 : "More than 12 months ago",
    9 : "Never used"
}

# Create lists of dictionary keys and values
global eduhighcat_keyList
global eduhighcat_valList
global age2_keyList
global age2_valList
global iralcrc_keyList
global iralcrc_valList
global ircigrc_keyList
global ircigrc_valList
global irmjrc_keyList
global irmjrc_valList
global ircocrc_keyList
global ircocrc_valList
global ircrkrc_keyList
global ircrkrc_valList
global irherrc_keyList
global irherrc_valList
global irhallucrec_keyList
global irhallucrec_valList
global irlsdrc_keyList
global irlsdrc_valList
global irecstmorec_keyList
global irecstmorec_valList
global irinhalrec_keyList
global irinhalrec_valList
global irmethamrec_keyList
global irmethamrec_valList
eduhighcat_keyList = list(eduhighcat_dict.keys())
eduhighcat_valList = list(eduhighcat_dict.values())
age2_keyList = list(age2_dict.keys())
age2_valList = list(age2_dict.values())
iralcrc_keyList = list(iralcrc_dict.keys())
iralcrc_valList = list(iralcrc_dict.values())
ircigrc_keyList = list(ircigrc_dict.keys())
ircigrc_valList = list(ircigrc_dict.values())
irmjrc_keyList = list(irmjrc_dict.keys())
irmjrc_valList = list(irmjrc_dict.values())
ircocrc_keyList = list(ircocrc_dict.keys())
ircocrc_valList = list(ircocrc_dict.values())
ircrkrc_keyList = list(ircrkrc_dict.keys())
ircrkrc_valList = list(ircrkrc_dict.values())
irherrc_keyList = list(irherrc_dict.keys())
irherrc_valList = list(irherrc_dict.values())
irhallucrec_keyList = list(irhallucrec_dict.keys())
irhallucrec_valList = list(irhallucrec_dict.values())
irlsdrc_keyList = list(irlsdrc_dict.keys())
irlsdrc_valList = list(irlsdrc_dict.values())
irecstmorec_keyList = list(irecstmorec_dict.keys())
irecstmorec_valList = list(irecstmorec_dict.values())
irinhalrec_keyList = list(irinhalrec_dict.keys())
irinhalrec_valList = list(irinhalrec_dict.values())
irmethamrec_keyList = list(irmethamrec_dict.keys())
irmethamrec_valList = list(irmethamrec_dict.values())

# Dropdown menu options
eduhighcat_options = eduhighcat_valList
age2_options = age2_valList
iralcrc_options = iralcrc_valList
ircigrc_options = ircigrc_valList
irmjrc_options = irmjrc_valList
ircocrc_options = ircocrc_valList
ircrkrc_options = ircrkrc_valList
irherrc_options = irherrc_valList
irhallucrec_options = irhallucrec_valList
irlsdrc_options = irlsdrc_valList
irecstmorec_options = irecstmorec_valList
irinhalrec_options = irinhalrec_valList
irmethamrec_options = irmethamrec_valList

# Declare variables for storing field values
eduhighcat_var = tk.StringVar(root)
age2_var = tk.StringVar(root)
irsex_var = tk.StringVar(root)
iralcage_sbx_var = tk.IntVar(root)
iralcage_ckb_var = tk.IntVar(root)
iralcrc_var = tk.StringVar(root)
iralcfy_sbx_var = tk.IntVar(root)
iralcfy_ckb1_var = tk.IntVar(root)
iralcfy_ckb2_var = tk.IntVar(root)
cabingevr_var = tk.StringVar(root)
txyrrecvd2_var = tk.StringVar(root)
txevrrcvd2_var = tk.StringVar(root)
ircigrc_var = tk.StringVar(root)
cigage_sbx_var = tk.IntVar(root)
cigage_ckb_var = tk.IntVar(root)
fucig18_var = tk.StringVar(root)
tobyr_var = tk.StringVar(root)
irmjrc_var = tk.StringVar(root)
irmjfy_sbx_var = tk.IntVar(root)
irmjfy_ckb1_var = tk.IntVar(root)
irmjfy_ckb2_var = tk.IntVar(root)
fumj18_var = tk.StringVar(root)
ircocrc_var = tk.StringVar(root)
ircrkrc_var = tk.StringVar(root)
irherrc_var = tk.StringVar(root)
irhallucrec_var = tk.StringVar(root)
irlsdrc_var = tk.StringVar(root)
irecstmorec_var = tk.StringVar(root)
irinhalrec_var = tk.StringVar(root)
irmethamrec_var = tk.StringVar(root)
addprev_var = tk.StringVar(root)
addscev_var = tk.StringVar(root)
booked_var = tk.StringVar(root)

# Set field values (when needed)
eduhighcat_var.set(eduhighcat_dict[1])
age2_var.set(age2_dict[1])
irsex_var.set("Male")
iralcage_sbx_var.set(1)
iralcrc_var.set(iralcrc_dict[1])
iralcfy_sbx_var.set(1)
cabingevr_var.set("Yes")
txyrrecvd2_var.set("No")
txevrrcvd2_var.set("No")
ircigrc_var.set(ircigrc_dict[1])
cigage_sbx_var.set(1)
fucig18_var.set("Yes")
tobyr_var.set("Did not use in the past year")
irmjrc_var.set(irmjrc_dict[1])
irmjfy_sbx_var.set(1)
fumj18_var.set("Yes")
ircocrc_var.set(ircocrc_dict[1])
ircrkrc_var.set(ircrkrc_dict[1])
irherrc_var.set(irherrc_dict[1])
irhallucrec_var.set(irhallucrec_dict[1])
irlsdrc_var.set(irlsdrc_dict[1])
irecstmorec_var.set(irecstmorec_dict[1])
irinhalrec_var.set(irinhalrec_dict[1])
irmethamrec_var.set(irmethamrec_dict[1])
addprev_var.set("Yes")
addscev_var.set("Yes")
booked_var.set("Yes")

# Setup form field labels
eduhighcat_lbl = Label(root, text="Education:", anchor=E).grid(sticky=E, row=0,
    column=0)
age2_lbl = Label(root, text="Age:", anchor=E).grid(sticky=E, row=1, column=0)
irsex_lbl = Label(root, text = "Gender:", anchor=E).grid(sticky=E, row=2, column=0)
iralcage_lbl = Label(root, text="Age at first use of alcohol:", anchor=E).grid(sticky=E,
    row=3, column=0)
iralcrc_lbl = Label(root, text="Most recent use of alcohol:", anchor=E).grid(sticky=E,
    row=4, column=0)
iralcfy_lbl = Label(root, text="Days using alcohol in the past year:", anchor=E).grid(sticky=E,
    row=5, column=0)
cabingevr_lbl = Label(root, text="Have you ever had 4/5 or more drinks on the same occasion?",
    anchor=E).grid(sticky=E, row=6, column=0)
txyrrecvd2_lbl = Label(root, text="Have you had alcohol or drug use treatment in the past year?",
    anchor=E).grid(sticky=E, row=7, column=0)
txevrrcvd2_lbl = Label(root, text="Have you ever had alcohol or drug use treatment in your life?",
    anchor=E).grid(sticky=E, row=8, column=0)
ircigrc_lbl = Label(root, text="Most recent use of cigarettes:", anchor=E).grid(sticky=E, row=9,
    column=0)
cigage_lbl = Label(root, text="Age when individual began smoking daily:", anchor=E).grid(sticky=E,
    row=10, column=0)
fucig18_lbl = Label(root, text="First use of cigarettes prior to 18?", anchor=E).grid(sticky=E,
    row=11, column=0)
tobyr_lbl = Label(root, text="Have you used any tobacco product in the past year?",
    anchor=E).grid(sticky=E, row=12, column=0)
irmjrc_lbl = Label(root, text="Most recent use of cannabis:", anchor=E).grid(sticky=E,
    row=13, column=0)
irmjfy_lbl = Label(root, text="Days using cannabis in the past year:", anchor=E).grid(sticky=E,
    row=14, column=0)
fumj18_lbl = Label(root, text="First use of cannabis prior to age 18?", anchor=E).grid(sticky=E,
    row=15, column=0)
ircocrc_lbl = Label(root, text="Most recent use of cocaine", anchor=E).grid(sticky=E,
    row=16, column=0)
ircrkrc_lbl = Label(root, text="Most recent use of crack cocaine:", anchor=E).grid(sticky=E,
    row=17, column=0)
irherrc_lbl = Label(root, text="Most recent use of crack cocaine:", anchor=E).grid(sticky=E,
    row=18, column=0)
irhallucrec_lbl = Label(root, text="Most recent use of hallucinogens:", anchor=E).grid(sticky=E,
    row=19, column=0)
irlsdrc_lbl = Label(root, text="Most recent use of LSD:", anchor=E).grid(sticky=E,
    row=20, column=0)
irecstmorec_lbl = Label(root, text="Most recent use of Ecstasy", anchor=E).grid(sticky=E,
    row=21, column=0)
irinhalrec_lbl = Label(root, text="Most recent use of inhalants:", anchor=E).grid(sticky=E,
    row=22, column=0)
irmethamrec_lbl = Label(root, text="Most recent use of methamphetamine:", anchor=E).grid(sticky=E,
    row=23, column=0)
addprev_lbl = Label(root, text="Have you felt sad, empty, or depressed for several days or longer?",
    anchor=E).grid(sticky=E, row=24, column=0)
addscev_lbl = Label(root, text="Have you felt discouraged about life for several days or longer?",
    anchor=E).grid(sticky=E, row=25, column=0)
booked_lbl = Label(root, text="Have you ever been arrested and booked in the criminal justice system?",
    anchor=E).grid(sticky=E, row=26, column=0)

# Setup actual form fields
eduhighcat_cbx = OptionMenu(root, eduhighcat_var, *eduhighcat_options).grid(sticky=EW,
    row=0, column = 1, columnspan=spanCol)
age2_cbx = OptionMenu(root, age2_var, *age2_options).grid(sticky=EW, row=1, column=1,
    columnspan=spanCol)
irsex_rbm = Radiobutton(root, text="Male", padx=5, variable=irsex_var, value="Male"
    ).grid(row=2, column=1)
irsex_rbf = Radiobutton(root, text="Female", padx=20, variable=irsex_var, value="Female"
    ).grid(row=2, column=2)
iralcage_sbx = Spinbox(root, from_=1, to=69, width=3, textvariable=iralcage_sbx_var)
iralcage_sbx.grid(row=3, column=1)
iralcage_rangeValidation = root.register(validate_iralcage)
iralcage_sbx.config(validate='key', validatecommand=(iralcage_rangeValidation, '%P'))
iralcage_ckb = Checkbutton(root, text="Never used", variable=iralcage_ckb_var,
    command=iralcage_onCheck)
iralcage_ckb.grid(row=3, column=2)
iralcrc_cbx = OptionMenu(root, iralcrc_var, *iralcrc_options).grid(sticky=EW, row=4,
    column=1, columnspan=spanCol)
iralcfy_sbx = Spinbox(root, from_=1, to=365, width=3, textvariable=iralcfy_sbx_var)
iralcfy_sbx.grid(row=5, column=1)
iralcfy_rangeValidation = root.register(validate_iralcfy)
iralcfy_sbx.config(validate='key', validatecommand=(iralcfy_rangeValidation, '%P'))
iralcfy_ckb1 = Checkbutton(root, text="Never used", variable=iralcfy_ckb1_var,
    command=iralcfy_onCheck)
iralcfy_ckb1.grid(row=5, column=2)
iralcfy_ckb2 = Checkbutton(root, text="Did not use alcohol past year",
    variable=iralcfy_ckb2_var, command=iralcfy_onCheck)
iralcfy_ckb2.grid(row=5, column=3)
cabingevr_rbYes = Radiobutton(root, text="Yes", padx=5, variable=cabingevr_var,
    value="Yes").grid(row=6, column=1)
cabingevr_rbNo = Radiobutton(root, text="No", padx=5, variable=cabingevr_var,
    value="No").grid(row=6, column=2)
cabingevr_rbNev = Radiobutton(root, text="Never used", padx=5, variable=cabingevr_var,
    value="Never used").grid(row=6, column=3)
txyrrecvd2_rbNo = Radiobutton(root, text="No", padx=5, variable=txyrrecvd2_var,
    value="No").grid(row=7, column=1)
txyrrecvd2_rbYes = Radiobutton(root, text="Yes", padx=5, variable=txyrrecvd2_var,
    value="Yes").grid(row=7, column=2)
txevrrcvd2_rbNo = Radiobutton(root, text="No", padx=5, variable=txevrrcvd2_var,
    value="No").grid(row=8, column=1)
txevrrcvd2_rbYes = Radiobutton(root, text="Yes", padx=5, variable=txevrrcvd2_var,
    value="Yes").grid(row=8, column=2)
ircigrc_cbx = OptionMenu(root, ircigrc_var, *ircigrc_options).grid(sticky=EW, row=9,
    column=1, columnspan=spanCol)
cigage_sbx = Spinbox(root, from_=1, to=79, width=3, textvariable=cigage_sbx_var)
cigage_sbx.grid(row=10, column=1)
cigage_rangeValidation = root.register(validate_cigage)
cigage_sbx.config(validate='key', validatecommand=(cigage_rangeValidation, '%P'))
cigage_ckb = Checkbutton(root, text="Never used cigarettes", variable=cigage_ckb_var,
    command=cigage_onCheck)
cigage_ckb.grid(row=10, column=2)
fucig18_rbYes = Radiobutton(root, text="Yes", padx=5, variable=fucig18_var,
    value="Yes").grid(row=11, column=1)
fucig18_rbNo = Radiobutton(root, text="No", padx=5, variable=fucig18_var, value="No"
    ).grid(row=11, column=2)
tobyr_rbNo = Radiobutton(root, text="Did not use in the past year", padx=5, variable=tobyr_var,
    value="Did not use in the past year").grid(row=12, column=1)
tobyr_rbYes = Radiobutton(root, text="Used within the past year", padx=5, variable=tobyr_var,
    value="Used within the past year").grid(row=12, column=2)
irmjrc_cbx = OptionMenu(root, irmjrc_var, *irmjrc_options).grid(sticky=EW,
    row=13, column=1, columnspan=spanCol)
irmjfy_sbx = Spinbox(root, from_=1, to=365, width=3, textvariable=irmjfy_sbx_var)
irmjfy_sbx.grid(row=14, column=1)
irmjfy_rangeValidation = root.register(validate_irmjfy)
irmjfy_sbx.config(validate='key', validatecommand=(irmjfy_rangeValidation, '%P'))
irmjfy_ckb1 = Checkbutton(root, text="Never used", variable=irmjfy_ckb1_var,
    command=irmjfy_onCheck)
irmjfy_ckb1.grid(row=14, column=2)
irmjfy_ckb2 = Checkbutton(root, text="Did not use marijuana past year",
    variable=irmjfy_ckb2_var, command=irmjfy_onCheck)
irmjfy_ckb2.grid(row=14, column=3)
fumj18_rbYes = Radiobutton(root, text="Yes", padx=5, variable=fumj18_var, value="Yes"
    ).grid(row=15, column=1)
fumj18_rbNo = Radiobutton(root, text="No", padx=5, variable=fumj18_var, value="No"
    ).grid(row=15, column=2)
ircocrc_cbx = OptionMenu(root, ircocrc_var, *ircocrc_options).grid(sticky=EW,
    row=16, column=1, columnspan=spanCol)
ircrkrc_cbx = OptionMenu(root, ircrkrc_var, *ircrkrc_options).grid(sticky=EW,
    row=17, column=1, columnspan=spanCol)
irherrc_cbx = OptionMenu(root, irherrc_var, *irherrc_options).grid(sticky=EW,
    row=18, column=1, columnspan=spanCol)
irhallucrec_cbx = OptionMenu(root, irhallucrec_var, *irhallucrec_options).grid(sticky=EW,
    row=19, column=1, columnspan=spanCol)
irlsdrc_cbx = OptionMenu(root, irlsdrc_var, *irlsdrc_options).grid(sticky=EW,
    row=20, column=1, columnspan=spanCol)
irecstmorec_cbx = OptionMenu(root, irecstmorec_var, *irecstmorec_options).grid(sticky=EW,
    row=21, column=1, columnspan=spanCol)
irinhalrec_cbx = OptionMenu(root, irinhalrec_var, *irinhalrec_options).grid(sticky=EW,
    row=22, column=1, columnspan=spanCol)
irmethamrec_cbx = OptionMenu(root, irmethamrec_var, *irmethamrec_options).grid(sticky=EW,
    row=23, column=1, columnspan=spanCol)
addprev_rbYes = Radiobutton(root, text="Yes", padx=5, variable=addprev_var,
    value="Yes").grid(row=24, column=1)
addprev_rbNo = Radiobutton(root, text="No", padx=5, variable=addprev_var,
    value="No").grid(row=24, column=2)
addprev_rbIdk = Radiobutton(root, text="Don't know", variable=addprev_var,
    value="Don't know").grid(row=24, column=3)
addscev_rbYes = Radiobutton(root, text="Yes", padx=5, variable=addscev_var,
    value="Yes").grid(row=25, column=1)
addscev_rbNo = Radiobutton(root, text="No", padx=5, variable=addscev_var,
    value="No").grid(row=25, column=2)
addscev_rbIdk = Radiobutton(root, text="Don't know", padx=5, variable=addscev_var,
    value="Don't know").grid(row=25, column=3)
booked_rbYes = Radiobutton(root, text="Yes", padx=5, variable=booked_var,
    value="Yes").grid(row=26, column=1)
booked_rbNo = Radiobutton(root, text="No", padx=5, variable=booked_var,
    value="No").grid(row=26, column=2)
booked_rbIdk = Radiobutton(root, text="Don't know", padx=5, variable=booked_var,
    value="Don't know").grid(row=26, column=3)
booked_rbRta = Radiobutton(root, text="Refuse to answer", padx=5, variable=booked_var,
    value="Refuse to answer").grid(row=26, column=4)

# Button click event
def btnClick():
   # Define global variable for the data frame to return
   global df

   # Put the field values into local variables
   # Utilize the key and value lists to get the correct dictionary number
   eduhighcat = tk.IntVar()
   eduhighcat = eduhighcat_keyList[eduhighcat_valList.index(eduhighcat_var.get())]

   # Utilize the key and value lists to get the correct dictionary number
   age2 = tk.IntVar()
   age2 = age2_keyList[age2_valList.index(age2_var.get())]

   irsex = tk.IntVar()
   if irsex_var.get() == "Male":
       irsex = 1
   elif irsex_var.get() == "Female":
       irsex = 2
       
   iralcage = tk.IntVar()
   if iralcage_ckb_var.get() == 1:
       iralcage = 991
   elif iralcage_ckb_var.get() == 0:
       iralcage = iralcage_sbx_var.get()

   # Utilize the key and value lists to get the correct dictionary number
   iralcrc = tk.IntVar()
   iralcrc = iralcrc_keyList[iralcrc_valList.index(iralcrc_var.get())]

   iralcfy = tk.IntVar()
   if (iralcfy_ckb1_var.get() == 1) and (iralcfy_ckb2_var.get() == 0):
       #only 'never used' is checked
       iralcfy = 991
   elif (iralcfy_ckb1_var.get() == 0) and (iralcfy_ckb2_var.get() == 0):
       #neither are checked
       iralcfy = iralcfy_sbx_var.get()
   elif (iralcfy_ckb1_var.get() == 0) and (iralcfy_ckb2_var.get() == 1):
       #only 'did not use alcohol last year' is checked
       iralcfy = 992

   cabingevr = tk.IntVar()
   if cabingevr_var.get() == "Yes":
       cabingevr = 1
   elif cabingevr_var.get() == "No":
       cabingevr = 2
   elif cabingevr_var.get() == "Never used":
       cabingevr = 91

   txyrrecvd2 = tk.IntVar()
   if txyrrecvd2_var.get() == "No":
       txyrrecvd2 = 0
   elif txyrrecvd2_var.get() == "Yes":
       txyrrecvd2 = 1

   txevrrcvd2 = tk.IntVar()
   if txevrrcvd2_var.get() == "No":
       txevrrcvd2 = 0
   elif txevrrcvd2_var.get() == "Yes":
       txevrrcvd2 = 1

   # Utilize the key and value lists to get the correct dictionary number
   ircigrc = tk.IntVar()
   ircigrc = ircigrc_keyList[ircigrc_valList.index(ircigrc_var.get())]

   cigage = tk.IntVar()
   if cigage_ckb_var.get() == 1:
       cigage = 991
   elif cigage_ckb_var.get() == 0:
       cigage = cigage_sbx_var.get()

   fucig18 = tk.IntVar()
   if fucig18_var.get() == "Yes":
       fucig18 = 1
   elif fucig18_var.get() == "No":
       fucig18 = 2

   tobyr = tk.IntVar()
   if tobyr_var.get() == "Did not use in the past year":
       tobyr = 0
   elif tobyr_var.get() == "Used within the past year":
       tobyr = 1

   # Utilize the key and value lists to get the correct dictionary number
   irmjrc = tk.IntVar()
   irmjrc = irmjrc_keyList[irmjrc_valList.index(irmjrc_var.get())]

   irmjfy = tk.IntVar()
   if (irmjfy_ckb1_var.get() == 1) and (irmjfy_ckb2_var.get() == 0):
       #only 'never used' is checked
       irmjfy = 991
   elif (irmjfy_ckb1_var.get() == 0) and (irmjfy_ckb2_var.get() == 0):
       #neither are checked
       irmjfy = irmjfy_sbx_var.get()
   elif (irmjfy_ckb1_var.get() == 0) and (irmjfy_ckb2_var.get() == 1):
       #only 'did not use alcohol last year' is checked
       irmjfy = 993

   fumj18 = tk.IntVar()
   if fumj18_var.get() == "Yes":
       fumj18 = 1
   elif fumj18_var.get() == "No":
       fumj18 = 2

   # Utilize the key and value lists to get the correct dictionary number
   ircocrc = tk.IntVar()
   ircocrc = ircocrc_keyList[ircocrc_valList.index(ircocrc_var.get())]

   # Utilize the key and value lists to get the correct dictionary number
   ircrkrc = tk.IntVar()
   ircrkrc = ircrkrc_keyList[ircrkrc_valList.index(ircrkrc_var.get())]

   # Utilize the key and value lists to get the correct dictionary number
   irherrc = tk.IntVar()
   irherrc = irherrc_keyList[irherrc_valList.index(irherrc_var.get())]

   # Utilize the key and value lists to get the correct dictionary number
   irhallucrec = tk.IntVar()
   irhallucrec = irhallucrec_keyList[irhallucrec_valList.index(irhallucrec_var.get())]

   # Utilize the key and value lists to get the correct dictionary number
   irlsdrc = tk.IntVar()
   irlsdrc = irlsdrc_keyList[irlsdrc_valList.index(irlsdrc_var.get())]

   # Utilize the key and value lists to get the correct dictionary number
   irecstmorec = tk.IntVar()
   irecstmorec = irecstmorec_keyList[irecstmorec_valList.index(irecstmorec_var.get())]

   # Utilize the key and value lists to get the correct dictionary number
   irinhalrec = tk.IntVar()
   irinhalrec = irinhalrec_keyList[irinhalrec_valList.index(irinhalrec_var.get())]

   # Utilize the key and value lists to get the correct dictionary number
   irmethamrec = tk.IntVar()
   irmethamrec = irmethamrec_keyList[irmethamrec_valList.index(irmethamrec_var.get())]

   addprev = tk.IntVar()
   if addprev_var.get() == "Yes":
       addprev = 1
   elif addprev_var.get() == "No":
       addprev = 2
   elif addprev_var.get() == "Don't know":
       addprev = 94

   addscev = tk.IntVar()
   if addscev_var.get() == "Yes":
       addscev = 1
   elif addscev_var.get() == "No":
       addscev = 2
   elif addscev_var.get() == "Don't know":
       addscev = 94

   booked = tk.IntVar()
   if booked_var.get() == "Yes":
       booked = 1
   elif booked_var.get() == "No":
       booked = 2
   elif booked_var.get() == "Don't know":
       booked = 94
   elif booked_var.get() == "Refuse to answer":
       booked = 97

   # Collect inputs into a DataFrame
   data = [[eduhighcat, age2, irsex, iralcage, iralcrc, iralcfy, cabingevr, txyrrecvd2,
    txevrrcvd2, ircigrc, cigage, fucig18, tobyr, irmjrc, irmjfy, fumj18, ircocrc, ircrkrc,
    irherrc, irhallucrec, irlsdrc, irecstmorec, irinhalrec, irmethamrec, addprev, addscev, booked]]
   df = pd.DataFrame(data,columns=['eduhighcat', 'age2', 'irsex', 'iralcage', 'iralcrc',
    'iralcfy', 'cabingevr', 'txyrrecvd2', 'txevrrcvd2', 'ircigrc', 'cigage', 'fucig18',
    'tobyr', 'irmjrc', 'irmjfy', 'fumj18', 'ircocrc', 'ircrkrc', 'irherrc', 'irhallucrec',
    'irlsdrc', 'irecstmorec', 'irinhalrec', 'irmethamrec', 'addprev', 'addscev', 'booked'])

   # Note: print function does not work in Power BI; print statment is for testing the script
   print (df)

   # Stop tkinter
   root.destroy()

# Add some space and set up button
Label(root,text="").grid(row=27,column=0)
btn = ttk.Button(root ,text="Submit",command=btnClick).grid(row=28, column=0, columnspan=(spanCol+1))

# Execute tkinter
root.mainloop()