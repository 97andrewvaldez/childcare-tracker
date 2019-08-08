import sqlite3

# Creates a connection to the database
con = sqlite3.connect('Childcare Tracker.db')
c = con.cursor()


# Commits changes to the database
def commit():
    con.commit()


# Closes the database
def close():
    con.close()


# Returns the id of a person, given the firstName, lasName, and table. If not available returns None
def get_id(fn, ln, tbl):
    q = ""
    if tbl == "Child":
        q = """SELECT ChildId
                    FROM Child
                    WHERE cFirstName LIKE "%{}%" AND cLastName LIKE "%{}%" """.format(fn, ln)

    elif tbl == "Parent":
        q = """SELECT ParentId
                    FROM Parent
                    WHERE pFirstName LIKE "%{}%" AND pLastName LIKE "%{}%" """.format(fn, ln)

    elif tbl == "Employee":
        q = """SELECT EmployeeId
                            FROM Employee
                            WHERE eFirstName LIKE "%{}%" AND eLastName LIKE "%{}%" """.format(fn, ln)

    c.execute(q)
    id_num = c.fetchone()

    # Checks if the id value is None
    if id_num is None:
        print("No id found")
        return None

    return id_num[0]


# Returns the ID of the parent given a childs first and last name, returns none if not available
def get_parID(cfn, cln):
    q = """SELECT ParentId
                FROM Parent NATURAL JOIN DropsOff NATURAL JOIN Child 
                WHERE Child.cFirstName LIKE "%{}%" AND Child.cLastName LIKE "%{}%" """.format(cfn, cln)

    c.execute(q)
    id_num = c.fetchone()

    # Checks if the id value is None
    if id_num is None:
        print("No id found")
        return None
    return id_num[0]


# Updates the owe attribute for a parent, given a parent id as a parameter
def update_owes(p_id):
    owe_query = """UPDATE Parent
                                    SET Owes = round(Balance - (SELECT SUM(HoursWatched * Rate)
                                                    FROM Child NATURAL JOIN DropsOff
                                                    WHERE DropsOff.ParentId = {}
                                                    GROUP BY DropsOff.ParentID), 2)
                                    WHERE ParentId = {}""".format(p_id, p_id)
    c.execute(owe_query)
    commit()


# Adds a child to the database and to the drop_off table to create a relationship with the parent
def add_child(cfn, cln, cr, pfn, pln, ppn):
    # If parent is already in the database, they won't get added again
    if get_id(pfn, pln, "Parent") is None:
        parent_add = """INSERT INTO Parent (pFirstName, pLastName, pPhoneNumber, Owes, Balance)
                            VALUES ("{}", "{}", "{}", 0, 0)""".format(pfn, pln, ppn)
        c.execute(parent_add)

    child_add = """INSERT INTO Child (cFirstName, cLastName, Rate, HoursWatched)
                    VALUES ("{}", "{}", {}, 0)""".format(cfn, cln, cr)
    c.execute(child_add)
    commit()

    c_id = get_id(cfn, cln, "Child")
    p_id = get_id(pfn, pln, "Parent")

    # Insert into the drop_off table
    drop_off = """INSERT INTO DropsOff (ChildId, ParentId) 
                        VALUES ({}, {})""".format(c_id, p_id)

    c.execute(drop_off)
    commit()


# Adds an employee to the database
def add_employee(efn, eln, epn, er):
    employee_add = """INSERT INTO Employee (eFirstName, eLastName, PhoneNumber, HourlyWage, HoursWorked)
                       VALUES ("{}", "{}", "{}", {}, 0)""".format(efn, eln, epn, er)
    c.execute(employee_add)
    commit()


# Removes the child, parent and relationships given the firstName, lastName and table
def remove(fn, ln, tbl):
    id_num = get_id(fn, ln, tbl)
    if tbl is not "Employee":
        p_id = get_parID(fn, ln)

        delete = """DELETE FROM Child 
                        WHERE ChildId in (SELECT ChildId
                                            FROM DropsOff 
                                            WHERE DropsOff.ParentId = {})""".format(p_id)
        c.execute(delete)
        commit()

        del_drops = """DELETE FROM DropsOff
                            WHERE ParentId = {}""".format(p_id)
        c.execute(del_drops)
        commit()

        del_babysit = """DELETE FROM Babysits
                            WHERE ChildId = {}""".format(id_num)
        c.execute(del_babysit)
        commit()

        del_par = """DELETE FROM Parent 
                            WHERE ParentId = {}""".format(p_id)
        c.execute(del_par)
        commit()

    else:
        count_query = """SELECT COUNT(*) FROM Employee"""
        c.execute(count_query)
        count = c.fetchone()
        if count[0] > 1:
            delete = """DELETE FROM Employee 
                        WHERE EmployeeId = {} """.format(id_num)

            c.execute(delete)
            commit()


def add_hours(fn, ln, hours, date, tbl):
    id_num = get_id(fn, ln, tbl)

    #if child already exists in babysits table skip this step
    exists_query = """SELECT COUNT(*) FROM Babysits WHERE ChildId = {}""".format(id_num)
    c.execute(exists_query)
    count = c.fetchone()

    if count[0] == 0:
        date_query = """INSERT INTO Babysits (Date, ChildId, EmployeeID)
                                               VAlUES("{}", {}, (SELECT EmployeeID 
                                                                FROM Employee 
                                                                ORDER BY RANDOM() 
                                                                LIMIT 1))""".format(date, id_num)
    else:
        date_query = """UPDATE Babysits
                            SET Date = {}
                            WHERE ChildId= {}""".format(date,id_num)

    if tbl == "Child":
        p_id = get_parID(fn, ln)
        add = """UPDATE Child 
                    SET HoursWatched =  HoursWatched + {}
                    WHERE ChildId = {} """.format(hours, id_num)

        c.execute(add)
        commit()
        update_owes(p_id)
        commit()

    elif tbl == "Employee":
        add = """UPDATE Employee 
                           SET HoursWorked = HoursWorked + {}
                           WHERE EmployeeId = {} """.format(hours, id_num)

        c.execute(add)
    c.execute(date_query)
    commit()


# Adds a payment and updates the drops off table to insert a date that the parent paid
def add_pay(fn, ln, bal, date):
    id_num = get_id(fn, ln, "Parent")
    payment_query = """UPDATE Parent
                            SET Balance = round(Balance + {}, 2)
                            WHERE ParentId = {}""".format(bal, id_num)

    drop_off = """UPDATE DropsOff
                    SET DatePaid = "{}"
                    WHERE ParentId = {}""".format(date, id_num)
    c.execute(payment_query)
    c.execute(drop_off)
    commit()
    update_owes(id_num)


# Changes the rate of an employee or child, given the name, rate, and table
def change_rate(fn, ln, rate, tbl):

    if tbl == "Employee":
        rate_query = """UPDATE Employee
                            SET HourlyWage = {}
                            WHERE eFirstName LIKE "%{}%" AND eLastName LIKE "%{}%" """.format(rate, fn, ln)
        c.execute(rate_query)
        commit()

    elif tbl == "Child":
        p_id = get_parID(fn, ln)
        rate_query = """UPDATE Child
                               SET Rate = {} 
                               WHERE cFirstName LIKE "%{}%" AND cLastName LIKE "%{}%" """.format(rate, fn, ln)
        c.execute(rate_query)
        commit()
        update_owes(p_id)


# Exports an excel compatable csv file with information about children for the week
def export_table():
    with open("output_table.csv", "w+") as write_file:
        tbl_query = """SELECT MAX(Date), cFirstName, cLastName, HoursWatched,
                        Rate, pFirstName, Balance, Owes, MAX(DatePaid)
                            FROM Babysits NATURAL JOIN Child  
                            NATURAL JOIN DropsOff NATURAL JOIN Parent  
                            GROUP BY Child.ChildId
                            ORDER BY Child.cFirstName"""

        write_file.write("Date added hours, First Name, Last Name, "
                         "Hours, Rate , Parent Name, Parent Balance, Parent Owes, DatePaid\n")
        for row in c.execute(tbl_query):
            s = ', '.join(map(str, row))
            write_file.write(s + "\n")


# Returns the actual balance that has been paid, and the estimated balance for the week
# determined by the amount of hours and rates for each child
def export_balances():
    cur_bal = 0
    est_bal = 0

    bal_query = """SELECT round(Balance, 2) 
                        FROM Parent"""
    for row in c.execute(bal_query):
        cur_bal += row[0]

    est_query = """SELECT round(HoursWatched * Rate, 2)
                            FROM Child"""
    for row in c.execute(est_query):
        est_bal += row[0]

    print("Estimate Balance = {}  \n   Actual Balance = {}".format(est_bal, cur_bal))
    return "{0:.2f}".format(cur_bal), "{0:.2f}".format(est_bal)


# returns 2 lists of Strings that say how much each parent owes in the database, and how much employee made
def export_parents():
    ls = []
    els = []

    # Gets balances for parents and adds them to a list
    bal_query = """SELECT pFirstName, pLastName, Owes
                        FROM Parent"""

    for row in c.execute(bal_query):
        s = "{} {}: {}".format(row[0], row[1], "%.2f"%row[2])
        ls.append(s)

    # Gets balances for employees and adds them to a list
    emp_query = """SELECT eFirstName, eLastName, HourlyWage * HoursWorked
                        FROM Employee"""
    for row in c.execute(emp_query):
        s = "{} {}: {}".format(row[0], row[1], "%.2f"%row[2])
        els.append(s)

    return ls, els


# Clears employee hours, Child hours, and payments for the week
def clear():
    emp = """UPDATE Employee
                SET HoursWorked = 0"""
    chld = """UPDATE Child
                SET HoursWatched = 0"""
    par = """UPDATE Parent
                SET Owes = 0, Balance = 0 """
    c.execute(emp)
    c.execute(chld)
    c.execute(par)
    commit()
