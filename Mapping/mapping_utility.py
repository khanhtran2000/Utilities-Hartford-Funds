from tkinter import *             
import pyodbc 
import pandas as pd
import numpy as np
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

dw_tables = pd.read_sql_query('SELECT TABLE_NAME FROM MFDW.INFORMATION_SCHEMA.TABLES', conn_dw) # Import SQL table with DW table names
dw_tables_list = list(dw_tables['TABLE_NAME'].tolist()) # Turn it into a list

ods_tables = pd.read_sql_query('SELECT TABLE_NAME FROM MFODS.INFORMATION_SCHEMA.TABLES', conn_ods) # Import SQL table with ODS table names
ods_tables_list = list(ods_tables['TABLE_NAME'].tolist()) # Turn it into a list


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
        for F in (StartPage, PageOne):
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

            # This is to make sure the tables put in are correct
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
            
            frame = Frame(self)
            frame.pack()

            dw_columns = pd.read_sql_query("SELECT COLUMN_NAME FROM MFDW.INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='{}'".format(dw_entry.upper()), conn_dw)
            ods_columns = pd.read_sql_query("SELECT COLUMN_NAME FROM MFODS.INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='{}'".format(ods_entry.upper()), conn_ods)
            
            dw_columns_list = list(dw_columns['COLUMN_NAME'].tolist())
            ods_columns_list = list(ods_columns['COLUMN_NAME'].tolist())

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

        def submit(): # the function that runs the SQL query, import the SQL table into Python
            sql_query_table = pd.read_sql_query('''SELECT ISNULL(LEFT(CU.CONSTRAINT_NAME,2),'') AS [Key Value]
              , C.TABLE_NAME AS [Target Table Name]
              , CASE WHEN C.DATA_TYPE IN ('BIGINT','BIT','DATE','DATETIME','DECIMAL','FLOAT','INT','NUMERIC','SMALLINT','TIMESTAMP','UNIQUEIDENTIFIER') THEN UPPER(C.DATA_TYPE) 
                     ELSE UPPER(C.DATA_TYPE) + '(' + CONVERT(VARCHAR(4),CHARACTER_MAXIMUM_LENGTH) + ')' END AS [Data Type]
              , C.IS_NULLABLE AS [Nullable (Y/N)]
FROM [Ad1hfddbwl1c1\MUTUALFUNDS].MFODS.INFORMATION_SCHEMA.COLUMNS AS C
LEFT OUTER JOIN [Ad1hfddbwl1c1\MUTUALFUNDS].MFODS.INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE AS CU ON C.TABLE_NAME = CU.TABLE_NAME AND C.COLUMN_NAME = CU.COLUMN_NAME
WHERE C.TABLE_NAME = '{0}'
'''.format(ods_entry), conn_ods) # C.TABLE_NAME = the ODS table that we put in earlier

            # create a dictionary with 4 columns, the first one has the DW column names, the second one has the DW table that we put in earlier
            newcolumn = {
                'Source field':dw_in_the_table,
                'Source table':dw_entry.upper(),
                'Column definition':np.nan,
                'Mapping Type':np.nan
            }

            target_column = pd.DataFrame(ods_in_the_table) # Create a column (or a dataframe with one column) with the values of ODS columns we put in ealier
            newcolumns = pd.DataFrame(newcolumn) # Make our 'newcolumn' dictionary into a dataframe

            new_df = pd.concat([sql_query_table[['Key Value','Target Table Name','Data Type']], newcolumns, sql_query_table[['Nullable (Y/N)']]], axis=1) # Concatenate the two dataframes 'sql_query_table' and 'newcolumns'
            new_df.insert(2, 'Target Column Name', target_column) # insert the 'target_column'
            new_df = new_df.iloc[:len(ods_in_the_table)] # Trim out the unnecessary parts of the final table
        
            new_df.to_excel(r'C:\Users\KT97777\Desktop\mapping_file.xlsx') # Export the final table to excel

        Label(self, text='').pack() # Just make a blank line
        Label(self, text='').pack() # Another blank line
        Label(self, text='Pick the columns that you want to compare.').pack()
        quit_button = Button(self, text="Quit Program",
                            command=lambda: controller.quit())
        submit_button = Button(self, text="Submit",
                            command=submit)
        back_button = Button(self, text="Back",
                            command=lambda: controller.show_frame("StartPage"))
        show_button = Button(self, text='Show',
                            command=show)

        Label(self, text='').pack()
        show_button.pack()

        #Placing the buttons        
        quit_button.place(relx=0.98, rely=0.98, anchor=SE)
        back_button.place(relx=0.761, rely=0.98, anchor=SE)
        submit_button.place(relx=0.8465, rely=0.98, anchor=SE)


if __name__ == "__main__":
    root = Validation_Tool()
    root.geometry('640x530')
    root.title("Validation Tool")
    root.iconbitmap('H:\Python_files\hf.ico')
    root.mainloop()
