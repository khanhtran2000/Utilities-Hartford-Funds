from tkinter import *             
import pyodbc 
import pandas as pd
from tkinter import ttk
from tkinter.font import Font

conn_ods = pyodbc.connect('Driver={SQL Server};'
                          'Server=Ad1hfddbwl1c1\MUTUALFUNDS;' 
                          'Database=MFODS;'
                          'Trusted_Connection=yes;')   # Connect to the MFODS 

conn_dw = pyodbc.connect('Driver={SQL Server};'
                         'Server=Ad1hfddbwl002\MUTUALFUNDS;'
                         'Database=MFDW;'
                         'Trusted_Connection=yes;')    # Connect to the MFDW

cursor = conn_ods.cursor()

dw_entry = ''
ods_entry = ''

dw_compare = ''
ods_compare = ''

dw_tables = pd.read_sql_query('SELECT TABLE_NAME FROM MFDW.INFORMATION_SCHEMA.TABLES', conn_dw)
dw_tables_list = list(dw_tables['TABLE_NAME'].tolist())

ods_tables = pd.read_sql_query('SELECT TABLE_NAME FROM MFODS.INFORMATION_SCHEMA.TABLES', conn_ods)
ods_tables_list = list(ods_tables['TABLE_NAME'].tolist())


class Validation_Tool(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.comboboxes_dw = []  # Comboboxes created. 
        self.combobox_vars_dw = [] # Vars for Comboboxes.

        self.comboboxes_ods = []  # Comboboxes created. 
        self.combobox_vars_ods = [] # Vars for Comboboxes.

        self.comboboxes_etl = []  # Comboboxes created. 
        self.combobox_vars_etl = [] # Vars for Comboboxes.

        self.comboboxes_group = []  # Comboboxes created. 
        self.combobox_vars_group = [] # Vars for Comboboxes.

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")


    def show_frame(self, page_name):
        #Show a frame for the given page name
        frame = self.frames[page_name]
        frame.tkraise()
    
    # Show a new frame with default text (used for PageTwo to PageThree)
    def show_frame_with_default_text(self, page_name, a_list):
        frame = self.frames[page_name]

        entry_list = [
                      frame.entry_name, frame.entry_worksheet,frame.entry_purpose, frame.entry_sub_type,
                      frame.entry_calendar, frame.entry_connection, frame.entry_message,
                      frame.entry_recipient, frame.entry_threshold, 
                      frame.entry_powershell, frame.entry_col_1, frame.entry_col_2
                     ]
        
        for index, entry in enumerate(entry_list):
            entry.delete(0, END)
            entry.insert(0, a_list[index])
        
        frame.tkraise()

    def quit(self):
        self.destroy()


class StartPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent

        def check_ods(): #Check ODS table function
            global ods_entry
            ods_entry = self.entry_ods.get()

            if ods_entry == '':
                label_none = Label(self)
                label_none['text'] = 'The entry box is blank'
                label_none['fg'] = 'red'
                label_none.grid(row=6, column=2, sticky=NSEW)
            elif ods_entry.upper() not in ods_tables_list:
                label_no = Label(self)
                label_no["text"] = "Not in the MFODS. Please try again."
                label_no['fg'] = 'red'
                label_no.grid(row=6, column=2, sticky=NSEW)
            elif ods_entry.upper() in ods_tables_list:
                label_yes = Label(self)
                label_yes['text'] = "Available"
                label_yes['fg'] = 'green'
                label_yes.grid(row=6, column=2, sticky=NSEW)

        def check_dw(): #Check DW table function
            global dw_entry
            dw_entry = self.entry_dw.get() 

            if dw_entry == '':
                label_none = Label(self)
                label_none['text'] = 'The entry box is blank.' 
                label_none['fg'] = 'red'
                label_none.grid(row=3, column=2, sticky=NSEW)
            elif dw_entry.upper() not in dw_tables_list:
                label_no = Label(self)
                label_no["text"] = "Not in the MFDW. Please try again."
                label_no['fg'] = 'red'
                label_no.grid(row=3, column=2, sticky=NSEW)
            elif dw_entry.upper() in dw_tables_list:
                label_yes = Label(self)
                label_yes['text'] = "Available"
                label_yes['fg'] = 'green'
                label_yes.grid(row=3, column=2, sticky=NSEW)

        def next_or_not(): #function for the NEXT button
            global ods_entry
            global dw_entry
            ods_entry = self.entry_ods.get()
            dw_entry = self.entry_dw.get()

            if (ods_entry.upper() not in ods_tables_list) or (dw_entry.upper() not in dw_tables_list):
                label = Label(self, text='Please recheck the tables.', fg='red')
                label.grid(row=7, column=1, columnspan=2, sticky=W)
            elif (ods_entry.upper() in ods_tables_list) or (dw_entry.upper() in dw_tables_list):
                controller.show_frame("PageOne")

        label_1 = Label(self, text="Enter an DW table")
        label_2 = Label(self, text="Enter a ODS table")
        label_3 = Label(self, text="")
        self.entry_ods = Entry(self, width=39)
        self.entry_dw = Entry(self, width=39)

        button_check_dw = Button(self, text="Check DW table", command=check_dw)
        button_check_ods = Button(self, text="Check ODS table", command=check_ods)
        quit_button = Button(self, text="Quit Program",
                            command=lambda: controller.quit())
        next_button = Button(self, text="Next",
                            command=next_or_not)

        label_3.grid(row=1, column=1) # make the label appear on screen
        label_1.grid(row=2, column=1, sticky=W) # make the label appear on screen
        self.entry_dw.grid(row=2, column=2, sticky=W) # make the entry box appear on screen
        button_check_dw.grid(row=3, column=1, sticky=W, pady=4) # make the button appear on screen
        label_2.grid(row=4, column=1, sticky=W)
        self.entry_ods.grid(row=4, column=2, sticky=W)

        #Placing the buttons 
        button_check_ods.grid(row=6, column=1, sticky=W, pady=4)
        quit_button.place(relx=0.98, rely=0.98, anchor=SE) # quit button
        next_button.place(relx=0.8465, rely=0.98, anchor=SE) # next button

dw_in_the_table = [] #list of DW columns that will be included in the query
ods_in_the_table = [] #list of ODS columns that will be included in the query


class PageOne(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller   

        # Combobox event handler.
        def selected_dw(event, var):
            dw_in_the_table.append(var.get()) # Append Combobox option selected.

        # Combobox event handler.
        def selected_ods(event, var):
            ods_in_the_table.append(var.get()) # Append Combobox option selected.
        
        def show():
            dw_columns = pd.read_sql_query("SELECT COLUMN_NAME FROM MFDW.INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='{}'".format(dw_entry.upper()), conn_dw)
            ods_columns = pd.read_sql_query("SELECT COLUMN_NAME FROM MFODS.INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='{}'".format(ods_entry.upper()), conn_ods)
            
            dw_columns_list = list(dw_columns['COLUMN_NAME'].tolist())
            ods_columns_list = list(ods_columns['COLUMN_NAME'].tolist())

            frame = Frame(self) #create a new frame for every button click
            frame.place(in_=self, anchor='c', relx=.5, rely=.5)

            label_dw = Label(frame, text='DW Columns')
            label_dw.grid(row=0, column=0)

            combobox_var_dw = StringVar()
            combobox_var_ods = StringVar()

            options_dw = ttk.Combobox(frame, values=dw_columns_list, textvar=combobox_var_dw) #Combobox for DW columns
            options_dw.grid(row=1, column=0)
            options_dw.bind('<<ComboboxSelected>>',  # Bind event handler.           
                        lambda event, var=combobox_var_dw: selected_dw(event, var))
                
            self.controller.comboboxes_dw.append(options_dw)         
            self.controller.combobox_vars_dw.append(combobox_var_dw) 

            label_ods = Label(frame, text='ODS Columns')
            label_ods.grid(row=0, column=1)

            options_ods = ttk.Combobox(frame, values=ods_columns_list, textvar=combobox_var_ods) #Combobox for ODS columns
            options_ods.grid(row=1, column=1) 
            options_ods.bind('<<ComboboxSelected>>',  # Bind event handler.           
                        lambda event, var=combobox_var_ods: selected_ods(event, var))
                
            self.controller.comboboxes_ods.append(options_ods) # add the chosen option to the list        
            self.controller.combobox_vars_ods.append(combobox_var_ods) # add the chosen option to the list
            
        Label(self, text='').pack()
        Label(self, text='').pack()
        Label(self, text='Pick the columns that you want to compare.').pack()
        quit_button = Button(self, text="Quit Program",
                            command=lambda: controller.quit())
        next_button = Button(self, text="Next",
                            command=lambda: controller.show_frame("PageTwo"))
        back_button = Button(self, text="Back",
                            command=lambda: controller.show_frame("StartPage"))
        show_button = Button(self, text='Show',
                            command=show)

        Label(self, text='').pack()
        show_button.pack()

        #Placing the buttons        
        quit_button.place(relx=0.98, rely=0.98, anchor=SE)
        back_button.place(relx=0.787, rely=0.98, anchor=SE)
        next_button.place(relx=0.8465, rely=0.98, anchor=SE)


sql_query = ''

name = ''
worksheet_name = ''
validation_group = []
purpose = ''
etl = []
validation_sub_type = 'Record Check'
calendar_query = 'N/A'
connection = 'MFDW'
email_message = ''
email_recipient = 'MFDataAnalytics@thehartford.com'
threshold = 0
powershell_command = 'N/A'

col_1_desc = 'DW_FIELD'
col_2_desc = 'ODS_FIELD'


class PageTwo(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller 

        self.text = Text(self)
        
        def show_button(): #Show the query. Haven't figured out the way to show the query without clicking on a button.
            text_dw = dw_in_the_table[-1]
            text_ods = ods_in_the_table[-1]

            query = '''USE MFDW

BEGIN
SELECT 
    DW.{0} AS DW_FIELD
    ODS.{1} AS ODS_FIELD
FROM [MFDW].[DBO].[{2}] AS DW WITH (NOLOCK)
JOIN [AD1HFDDBWL1C1\MUTUALFUNDS].MFODS.DBO.{3} AS ODS WITH (NOLOCK) 
ON  = 
WHERE  
    DW.{0} <> ODS.{1} 
END;'''.format(text_dw, text_ods, dw_entry.upper(), ods_entry.upper())

            self.text.delete('1.0', END)
            self.text.insert(END, query)
            self.text.pack()
        
        def save_and_next(): #function for the next button. Moving to the next page and fetching the new content of the query box at the same time.
            global sql_query
            #'1.0' = start from first character in the text widget
            #'end-1c' = delete the last character that Text creates every time
            sql_query = self.text.get("1.0", 'end-1c') 
            controller.show_frame_with_default_text("PageThree", 
                                                    ['ODS DW - Checking {0} to {1}'.format(dw_in_the_table[-1], ods_in_the_table[-1]),
                                                    '{0}_{1}_CHECK'.format(dw_entry.upper(), dw_in_the_table[-1]),
                                                    'To assure the {0} matches between ODS and DW.'.format(dw_entry.upper()),
                                                    validation_sub_type, calendar_query, connection,
                                                    'The attached file has a list of values which does not reconcile between ODS and DW for {}'.format(dw_entry.upper()),
                                                    email_recipient, threshold, powershell_command, col_1_desc, col_2_desc
                                                    ])

        quit_button = Button(self, text="Quit Program",
                            command=lambda: controller.quit())
        next_button = Button(self, text="Next",
                            command=save_and_next)
        back_button = Button(self, text="Back",
                            command=lambda: controller.show_frame("PageOne"))
        button = Button(self, text='Show query', command=show_button)
        button.pack()
        Label(self, text='').pack()

        quit_button.place(relx=0.98, rely=0.98, anchor=SE)
        back_button.place(relx=0.787, rely=0.98, anchor=SE)
        next_button.place(relx=0.8465, rely=0.98, anchor=SE)


class PageThree(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller 

        # Combobox event handler for etl_batch_job drop down menu
        def selected_etl(event, var):
            etl.append(var.get()) # Append Combobox option selected

        # Create Combobox for etl_batch_job and how to assign the user's choice to the global variable
        etl_read = pd.read_sql("SELECT a.NM from ETL_BATCH_JOB a order by a.NM desc", conn_ods)

        etl_list = list(etl_read['NM'].tolist())

        combobox_var_etl = StringVar()

        options_etl = ttk.Combobox(self, values=etl_list, textvar=combobox_var_etl) # Combobox for etl_batch_job

        options_etl.bind('<<ComboboxSelected>>', # Bind event handler.
                    lambda event, var=combobox_var_etl: selected_etl(event, var))

        self.controller.comboboxes_etl.append(options_etl)
        self.controller.combobox_vars_etl.append(combobox_var_etl)

        # Combobox event handler for validation_group drop down menu
        def selected_group(event, var):
            validation_group.append(var.get()) # Append Combobox option selected.

        # Create Combobox for validation_group and how to assign the user's choice to the global variable
        validation_group_read = pd.read_sql_query("SELECT GRP_NM from VALIDATION_GROUP", conn_ods)

        validation_group_list = list(validation_group_read['GRP_NM'].tolist())

        combobox_var_group = StringVar()

        options_group = ttk.Combobox(self, values=validation_group_list, textvar=combobox_var_group) #Combobox for validation groups

        options_group.bind('<<ComboboxSelected>>',  # Bind event handler.           
                      lambda event, var=combobox_var_group: selected_group(event, var))

        self.controller.comboboxes_group.append(options_group)         
        self.controller.combobox_vars_group.append(combobox_var_group)

        # Setting labels and entries
        label_name = Label(self, text='Enter a valid name')
        self.entry_name = Entry(self, width=73)
        label_group = Label(self, text='Select a validation group')
        label_purpose = Label(self, text='Enter the purpose')
        self.entry_purpose = Entry(self, width=73)
        label_etl = Label(self, text='Select an ETL batch job')
        label_sub_type = Label(self, text='Enter the validation sub type')
        self.entry_sub_type = Entry(self, width=73)
        label_calendar = Label(self, text='Enter the calendar query')
        self.entry_calendar = Entry(self, width=73)
        label_connection = Label(self, text='Enter the connection')
        self.entry_connection = Entry(self, width=73)
        label_message = Label(self, text='Enter the email message')
        self.entry_message = Entry(self, width=73)
        label_recipient = Label(self, text='Enter an email recipient')
        self.entry_recipient = Entry(self, width=73)
        label_threshold = Label(self, text='Enter a threshold')
        self.entry_threshold = Entry(self, width=73)
        label_worksheet = Label(self, text='Enter the worksheet name')
        self.entry_worksheet = Entry(self, width=73)
        label_powershell = Label(self, text='Enter the powershell command')
        self.entry_powershell = Entry(self, width=73)    

        #Setting the labels and entries for columns description
        label_col_1 = Label(self, text="COL 1 DESC")
        self.entry_col_1 = Entry(self, width=73)
        label_col_2 = Label(self, text="COL 2 DESC")
        self.entry_col_2 = Entry(self, width=73)

        # Placing the entries for id, name, etl, purpose, and message
        Label(self, text='').grid(row=1, column=1) 
        label_name.grid(row=2, column=1, sticky=W, pady=5) 
        self.entry_name.grid(row=2, column=2, columnspan=4, sticky=W, pady=5) 
        label_group.grid(row=4, column=1, sticky=W, pady=5)
        options_group.grid(row=4, column=2, columnspan=4, sticky=W, pady=5)
        label_purpose.grid(row=5, column=1, sticky=W, pady=5)
        self.entry_purpose.grid(row=5, column=2, columnspan=4, sticky=W, pady=5)
        label_etl.grid(row=6, column=1, sticky=W, pady=5)
        options_etl.grid(row=6, column=2, sticky=W, pady=5)
        label_sub_type.grid(row=7, column=1, sticky=W, pady=5)
        self.entry_sub_type.grid(row=7, column=2, columnspan=4, sticky=W, pady=5)
        label_calendar.grid(row=8, column=1, sticky=W, pady=5)
        self.entry_calendar.grid(row=8, column=2, columnspan=4, sticky=W, pady=5)
        label_connection.grid(row=9, column=1, sticky=W, pady=5)
        self.entry_connection.grid(row=9, column=2, columnspan=4, stick=W, pady=5)
        label_message.grid(row=10, column=1, sticky=W, pady=5)
        self.entry_message.grid(row=10, column=2, columnspan=4, sticky=W, pady=5)
        label_recipient.grid(row=11, column=1, sticky=W, pady=5)
        self.entry_recipient.grid(row=11, column=2, columnspan=4, stick=W, pady=5)
        label_threshold.grid(row=12, column=1, sticky=W, pady=5)
        self.entry_threshold.grid(row=12, column=2, columnspan=4, sticky=W, pady=5)
        label_worksheet.grid(row=13, column=1, sticky=W, pady=5)
        self.entry_worksheet.grid(row=13, column=2, columnspan=4, sticky=W, pady=5)
        label_powershell.grid(row=14, column=1, sticky=W, pady=5)
        self.entry_powershell.grid(row=14, column=2, columnspan=4, stick=W, pady=5)

        # Placing the entries for the columns description
        label_col_1.grid(row=15, column=1, sticky=W, pady=5)
        self.entry_col_1.grid(row=15, column=2, columnspan=4, stick=W, pady=5)
        label_col_2.grid(row=16, column=1, sticky=W, pady=5)
        self.entry_col_2.grid(row=16, column=2, columnspan=4, stick=W, pady=5)

            
        def save_and_submit(): 
            # pass the input in the local entry boxes in this frame to the global variables so that
            # these values can be used in the next frame.                
            global name
            global purpose
            global validation_sub_type
            global calendar_query
            global connection
            global email_message
            global email_recipient
            global threshold
            global worksheet_name
            global powershell_command

            global col_1_desc
            global col_2_desc

            name = self.entry_name.get()
            purpose = self.entry_purpose.get()
            validation_sub_type = self.entry_sub_type.get()
            calendar_query = self.entry_calendar.get()
            connection = self.entry_connection.get()
            email_message = self.entry_message.get()
            email_recipient = self.entry_recipient.get()
            threshold = self.entry_threshold.get()
            worksheet_name = self.entry_worksheet.get()
            powershell_command = self.entry_powershell.get()

            col_1_desc = self.entry_col_1.get()
            col_2_desc = self.entry_col_2.get()

            #the query that is used to create a new row in the VALIDATION table in the ODS
            insert_query = '''USE [MFODS] 
GO

INSERT INTO [dbo].[VALIDATION]
           ([NM]
           ,[ETL_BATCH_JOB_ID]
           ,[VALID_SUB_TYP_ID]
           ,[PRPSE]
           ,[CAL_DT]
           ,[VALID_QUERY]
           ,[THRSH]
           ,[EMAIL_MSG]
           ,[EMAIL_RECIP]
           ,[WKSHT_NM]
           ,[POWERSHELL_COMMAND]
           ,[COL_1_DESC]
           ,[COL_2_DESC]
           ,[COL_3_DESC]
           ,[COL_4_DESC]
           ,[COL_5_DESC]
           ,[COL_6_DESC]
           ,[COL_7_DESC]
           ,[COL_8_DESC]
           ,[COL_9_DESC]
           ,[COL_10_DESC]
           ,[COL_11_DESC]
           ,[COL_12_DESC]
           ,[COL_13_DESC]
           ,[COL_14_DESC]
           ,[COL_15_DESC]
           ,[COL_16_DESC]
           ,[COL_17_DESC]
           ,[COL_18_DESC]
           ,[COL_19_DESC]
           ,[COL_20_DESC]
           ,[ADD_DT_TIME]
           ,[LAST_MAINT_DT_TIME]
           ,[LAST_MAINT_OPER_ID]
           ,[VALID_CONNECTIONS_ID])
     VALUES
           ('test',
		   'test',
		   'test',
		   'test',
		   'test',
		   'test',
		   'test',
		   'test',
		   'test',
		   'test',
		   'test',
		   'test',
		   'test',
		   'test',
		   'test',
		   'test',
		   'test',
		   'test',
		   'test',
		   'test',
		   'test',
		   'test',
		   'test',
		   'test',
		   'test',
		   'test',
		   'test',
		   'test',
		   'test',
		   'test',
		   'test',
		   'test',
		   'test',
		   'test',
		   'test')
GO                      '''
            cursor.execute(insert_query) # excecute SQL query in a Python script
            cursor.commit() # must have cursor.commit() or the execution won't make any change in the SQL Server database

        quit_button = Button(self, text="Quit Program",
                            command=lambda: controller.quit())
        submit_button = Button(self, text="Submit",
                            command=save_and_submit)
        back_button = Button(self, text="Back",
                            command=lambda: controller.show_frame("PageTwo"))
        
        quit_button.place(relx=0.98, rely=0.98, anchor=SE)
        back_button.place(relx=0.7657, rely=0.98, anchor=SE)
        submit_button.place(relx=0.8465, rely=0.98, anchor=SE)


if __name__ == "__main__":
    root = Validation_Tool()
    root.geometry('640x530')
    root.title("Validation Tool")
    root.iconbitmap('H:\Python_files\hf.ico')
    root.mainloop()
