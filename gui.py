# Class to make the widgets for the graphical user interface
# Author: Andrew Valdez

from tkinter import *
import database_controller as db
import sqlite3


# connect to database
con = sqlite3.connect('Childcare Tracker.db')
con.row_factory = lambda cursor, row: row[0] + " " + row[1]
c = con.cursor()


# commits changes to the database
def commit():
    con.commit()


# closes the database
def close():
    con.close()


# Basic queries that are called to make lists of children, parents, and employees
parent_query = """SELECT pFirstName, pLastName
               FROM Parent
               ORDER BY pLastName ASC"""


child_query = """SELECT cFirstName, cLastName
               FROM Child
               ORDER BY cLastName ASC"""


employee_query = """SELECT eFirstName, eLastName
               FROM Employee
               ORDER BY eLastName ASC"""

parent_list = c.execute(parent_query).fetchall()
child_list = c.execute(child_query).fetchall()
employee_list = c.execute(employee_query).fetchall()
object_list = child_list + parent_list + employee_list
object_list.sort()
commit()


# returns most current version of employee list
def update_emp():
    return c.execute(employee_query).fetchall()


# returns most current version of parent list
def update_par():
    return c.execute(parent_query).fetchall()


# returns most current version of child list
def update_chld():
    return c.execute(child_query).fetchall()


# Checks what table a person is in
def check_tbl(person):
    e_list = update_emp()
    p_list = update_par()
    c_list = update_chld()

    if person in e_list:
        return "Employee"
    elif person in p_list:
        return "Parent"
    elif person in c_list:
        return "Child"


# Returns a full list of parents children and employees
def update_list():
    par_list = c.execute(parent_query).fetchall()
    chld_list = c.execute(child_query).fetchall()
    emp_list = c.execute(employee_query).fetchall()
    return chld_list + par_list + emp_list

def error_msg(txt):
    top = Toplevel
    Error(top)


# creates main window that opens first when the program is run
class MainWindow:
    def __init__(self, master):
        self.master = master

        # Creates buttons
        self.add_button = Button(master, text="Add child or employee", command=self.add_window)
        self.remove_button = Button(master, text="Remove a child or employee", command=self.remove_window)
        self.hour_button = Button(master, text="Add hours", command=self.hours_window)
        self.payment_button = Button(master, text="Add payment", command=self.payment_window)
        self.rate_button = Button(master, text="Change rate", command=self.rate_window)
        self.export_button = Button(master, text="Export excel file", command=self.export_window)
        self.parent_button = Button(master, text="Which parents owe/employee funds", command=self.parent_window)
        self.balance_button = Button(master, text="View balance", command=self.balance_window)
        self.reset_button = Button(master, text="Reset hours and payments", command=self.reset_window)

        self.add_button.place(relx=0.5, rely=.1, anchor=CENTER, width=250)
        self.remove_button.place(relx=0.5, rely=.17, anchor=CENTER, width=250)
        self.hour_button.place(relx=0.5, rely=.24, anchor=CENTER, width=250)
        self.payment_button.place(relx=0.5, rely=.31, anchor=CENTER, width=250)
        self.parent_button.place(relx=0.5, rely=.38, anchor=CENTER, width=250)
        self.balance_button.place(relx=0.5, rely=.45, anchor=CENTER, width=250)
        self.export_button.place(relx=0.5, rely=.52, anchor=CENTER, width=250)
        self.rate_button.place(relx=0.5, rely=.59, anchor=CENTER, width=250)
        self.reset_button.place(relx=0.5, rely=.66, anchor=CENTER, width=250)

    def add_window(self):
        top = Toplevel()
        Add(top)

    def remove_window(self):
        top = Toplevel()
        Remove(top)

    def hours_window(self):
        top = Toplevel()
        AddHours(top)

    def payment_window(self):
        top = Toplevel()
        AddPayment(top)

    def rate_window(self):
        top = Toplevel()
        ChangeRate(top)

    def export_window(self):
        top = Toplevel()
        Export(top)

    def parent_window(self):
        top = Toplevel()
        PrintParents(top)

    def balance_window(self):
        top = Toplevel()
        ViewBalance(top)

    def reset_window(self):
        top = Toplevel()
        ResetHours(top)


# TopLevel gui window to add either a child or employee
class Add:
    def __init__(self, master):
        self.master = master

        # creates labels for adding a child
        self.add_label = Label(master, text='Add Child:')
        self.cfn_label = Label(master, text="Child First Name:")
        self.cln_label = Label(master, text="Child Last Name:")
        self.cr_label = Label(master, text='Child Rate:')
        self.pln_label = Label(master, text="Parent Last Name:")
        self.pfn_label = Label(master, text='Parent First Name:')
        self.ppn_label = Label(master, text='Parent Phone Number:')

        # gives variables to user inputs
        self.cfn = StringVar()
        self.cln = StringVar()
        self.cr = StringVar()
        self.pfn = StringVar()
        self.pln = StringVar()
        self.ppn = StringVar()

        # text boxes to get input from user
        self.cfn_entry = Entry(master, textvariable=self.cfn)
        self.cln_entry = Entry(master, textvariable=self.cln)
        self.cr_entry = Entry(master, textvariable=self.cr)
        self.pfn_entry = Entry(master, textvariable=self.pfn)
        self.pln_entry = Entry(master, textvariable=self.pln)
        self.ppn_entry = Entry(master, textvariable=self.ppn)

        # labels to add an employee
        self.employee_add = Label(master, text='Add Employee:')
        self.efn_label = Label(master, text="Employee First Name:")
        self.eln_label = Label(master, text='Employee Last Name:')
        self.epn_label = Label(master, text='Employee Phone Number:')
        self.er_label = Label(master, text='Employee Rate:')

        # gives variables to user inputs for employees
        self.efn = StringVar()
        self.eln = StringVar()
        self.epn = StringVar()
        self.er = StringVar()

        # text boxes to get input for employees
        self.efn_entry = Entry(master, textvariable=self.efn)
        self.eln_entry = Entry(master, textvariable=self.eln)
        self.epn_entry = Entry(master, textvariable=self.epn)
        self.er_entry = Entry(master, textvariable=self.er)

        # format labels and buttons
        self.add_label.grid(row=1, column=1)
        self.cfn_label.grid(row=2, column=1)
        self.cln_label.grid(row=3, column=1)
        self.cr_label.grid(row=4, column=1)
        self.pfn_label.grid(row=5, column=1)
        self.pln_label.grid(row=6, column=1)
        self.ppn_label.grid(row=7, column=1)

        self.cfn_entry.grid(row=2, column=2)
        self.cln_entry.grid(row=3, column=2)
        self.cr_entry.grid(row=4, column=2)
        self.pfn_entry.grid(row=5, column=2)
        self.pln_entry.grid(row=6, column=2)
        self.ppn_entry.grid(row=7, column=2)

        self.or_label = Label(master, text='Or')
        self.or_label.grid(row=1, column=3)

        self.employee_add.grid(row=1, column=4)
        self.efn_label.grid(row=2, column=4)
        self.eln_label.grid(row=3, column=4)
        self.epn_label.grid(row=4, column=4)
        self.er_label.grid(row=5, column=4)

        self.efn_entry.grid(row=2, column=5)
        self.eln_entry.grid(row=3, column=5)
        self.epn_entry.grid(row=4, column=5)
        self.er_entry.grid(row=5, column=5)

        # buttons to press when all of the data is entered
        self.add_cbutton = Button(master, text='Add Child', command=self.add_child)
        self.add_ebutton = Button(master, text='Add Employee', command=self.add_employee)
        self.add_cbutton.grid(row=8, column=2)
        self.add_ebutton.grid(row=8, column=5)

    # sends in the user input to the database_controller file and adds a child to the database
    def add_child(self):
        db.add_child(self.cfn.get(), self.cln.get(), self.cr.get(), self.pfn.get(), self.pln.get(), self.ppn.get())
        self.master.destroy()

    # sends in the user input to the database_controller file and adds an employee
    def add_employee(self):
        db.add_employee(self.efn.get(), self.eln.get(), self.epn.get(), self.er.get())
        self.master.destroy()


# Gui window to remove a child or employee object
class Remove:
    def __init__(self, master):

        self.master = master

        self.remove_label = Label(master, text='Child or employee to remove:')
        self.remove_button = Button(master, text='Remove', command=self.remove_object)

        # list of employees/children
        chld_list = update_chld()
        emp_list = update_emp()
        menu_list = chld_list + emp_list

        # Creates dropdown menu with object_list
        self.obj = StringVar()
        self.obj.set(menu_list[0])
        self.menu = OptionMenu(master, self.obj, *menu_list)

        # position widgets
        self.remove_label.grid(row=1, column=1)
        self.remove_button.grid(row=1, column=3)
        self.menu.grid(row=1, column=2)

    # calls the database_controller remove function, passing in the child/employee selected
    def remove_object(self):
        person = (self.obj.get())
        split = person.split()
        tbl = check_tbl(person)
        db.remove(split[0], split[1], tbl)
        self.master.destroy()


# gui TopLevel window to add hours for either an employee or child
class AddHours:
    def __init__(self, master):
        self.master = master

        self.date_label = Label(master, text='Date: ')
        self.date = StringVar()
        self.date_box = Entry(master, textvariable=self.date)

        self.hours = StringVar()
        self.hour_box = Entry(master, textvariable=self.hours)

        # list of employees/children
        chld_list = update_chld()
        emp_list = update_emp()
        menu_list = chld_list+emp_list

        # menu with list containing all employees and children
        self.person = StringVar()
        self.person.set(menu_list[0])
        self.menu = OptionMenu(master, self.person, *menu_list)

        self.hour_label = Label(master, text='Hours to add (negative if removing):')
        self.person_label = Label(master, text='Child/Employee to add hours for')
        self.add_button = Button(master, text='Add', command=self.add_hours)

        self.hour_label.grid(row=1, column=1)
        self.hour_box.grid(row=1, column=2)
        self.person_label.grid(row=3, column=1)
        self.menu.grid(row=3, column=2)
        self.add_button.grid(row=1, column=3)
        self.date_label.grid(row=2, column=1)
        self.date_box.grid(row=2, column=2)

    # calls to the database_controller add_hours method, passing in the person, and amount of hours
    def add_hours(self):

        person = (self.person.get())
        split = person.split()
        tbl = check_tbl(person)
        db.add_hours(split[0], split[1], self.hours.get(), self.date.get(), tbl)
        self.master.destroy()


# TopLevel window to display and collect information from the gui
class ChangeRate:
    def __init__(self, master):
        self.master = master

        self.rate = StringVar()
        self.rate_box = Entry(master, textvariable=self.rate)

        # list of employees/children
        chld_list = update_chld()
        emp_list = update_emp()
        menu_list = chld_list + emp_list

        # menu with list containing all employees and children
        self.person = StringVar()
        self.person.set(menu_list[0])
        self.menu = OptionMenu(master, self.person, *menu_list)

        self.rate_label = Label(master, text='New Rate: ')
        self.person_label = Label(master, text='Child/Employee to change rate for')
        self.change_button = Button(master, text='Change', command=self.change_rate)

        self.rate_label.grid(row=1, column=1)
        self.rate_box.grid(row=1, column=2)
        self.person_label.grid(row=2, column=1)
        self.menu.grid(row=2, column=2)
        self.change_button.grid(row=1, column=3)

    # Calls to the database controller to change the rate of a child or employee
    def change_rate(self):
        person = (self.person.get())
        split = person.split()
        tbl = check_tbl(person)
        db.change_rate(split[0], split[1], self.rate.get(), tbl)
        self.master.destroy()


# Toplevel gui window to add payments for a parent
class AddPayment:
    def __init__(self, master):

        self.master = master
        self.add_label = Label(master, text='How much is the payment for?')
        self.par_label = Label(master, text='Parent to add payment for:')
        self.add_button = Button(master, text='Add', command=self.add_payment)
        par_list = update_par()

        self.date_label = Label(master, text='Date: ')
        self.date = StringVar()
        self.date_box = Entry(master, textvariable=self.date)

        # payment box
        self.pay = StringVar()
        self.pay_box = Entry(master, textvariable=self.pay)

        # creates dropdown menu of parents
        self.par = StringVar()
        self.par.set(par_list[0])
        self.menu = OptionMenu(master, self.par, *par_list)

        # position widgets
        self.pay_box.grid(row=1, column=2)
        self.add_label.grid(row=1, column=1)
        self.add_button.grid(row=1, column=3)
        self.menu.grid(row=2, column=2)
        self.par_label.grid(row=2, column=1)
        self.date_label.grid(row=3, column=1)
        self.date_box.grid(row=3, column=2)

    # calls to the database add_payment method
    def add_payment(self):
        person = (self.par.get())
        split = person.split()
        db.add_pay(split[0], split[1], self.pay.get(), self.date.get())
        self.master.destroy()


# Class to recieve 2 lists from the database and print them to the gui
class PrintParents:
    def __init__(self, master):
        self.master = master
        ls, els = db.export_parents()
        emp_list = "\n".join(els)
        par_list = "\n".join(ls)
        output = "Negative Values: are how much the parent owes\n " \
                 "Positive Values: parent overpaid\n" + par_list + \
                 "\nHow much each employee will make given hours and rate: \n" + emp_list

        self.label = Label(master, text=output)
        self.label.pack()


# Class to print out the estimated and actual balances to the gui
class ViewBalance:
    def __init__(self, master):
        cur_bal, est_bal = db.export_balances()
        var = StringVar()
        var.set("Estimate Balance = {} \nActual Balance = {}".format(est_bal, cur_bal))

        self.master = master
        self.label = Label(master, textvariable=var)
        self.label.pack()


# Prints a label saying the hours were reset and calls the database clear method
class ResetHours:
    def __init__(self, master):
        self.master = master
        self.lbl = Label(master, text="Hours and payments have been successfully cleared for the week")
        self.lbl.grid(row=1, column=1)
        db.clear()


# Prints a label saying the file was exported and calls the database export_table
class Export:
    def __init__(self, master):
        self.master = master
        self.lbl = Label(master, text="File exported")
        self.lbl.pack()
        db.export_table()

# Prints an error message if something unexpected happens, not finished yet.  Next thing to be worked on
class Error:
    def __init__(self, master, txt):
        self.master = master
        self.lbl = Label(master, text=txt)
        self.lbl.pack()


# main method to keep the window running
def main():
    root = Tk()
    MainWindow(root)
    root.title("Babysitting tracker")
    root.geometry("400x400+100+100")
    root.mainloop()


if __name__ == '__main__':
    main()
