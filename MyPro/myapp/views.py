from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import DatabaseError, connection

# Create your views here.
def Home(request):
    if request.method == "GET":

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM employee")
        columns = [column[0] for column in cursor.description]
        empList = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return render(request, "home.html", {"data": empList})
    else:
        pass

def Create(request):
    if request.method == "GET":
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM department")
        columns = [column[0] for column in cursor.description]
        deptList = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return render(request, "create.html", {'data': deptList})
    else:
        if request.POST.get("Register") == "Register":
            # Insert the data : 
                try:
                    Ename = request.POST.get('txtEname')
                    Password = request.POST.get('txtPwd')
                    Gender = request.POST.get('Gender')
                    Phone = request.POST.get('txtPhone')
                    Email = request.POST.get('txtEmail')
                    DOB = request.POST.get('txtDOB')
                    Salary = request.POST.get('txtSalary')
                    Address = request.POST.get('txtAddress')
                    DeptNo = int(request.POST.get('ddlDeptNo'))

                    with connection.cursor() as cursor:
                        cursor.execute("""INSERT INTO Employee
                        (Ename, Password, Gender, Phone, Email, DOB, Salary, Address, DeptNo)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """, [Ename, Password, Gender, Phone, Email, DOB, Salary, Address, DeptNo])

                    return redirect("homepage")
                except (TypeError, ValueError, DatabaseError):
                    messages.error(request, "Unable to register the employee. Check the entered data.")
                    return render(request, "create.html", {"ErrorMessage" : "Unable to register the employee. Check the entered data."})
        else:
            return redirect("homepage")

def Edit(request, empid):
    if request.method == "GET":
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM employee WHERE EmpId = %s", [empid])
        emp = cursor.fetchone()

        cursor.execute("SELECT * FROM department")
        columns = [column[0] for column in cursor.description]
        deptList = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return render(request, "edit.html", { "data": deptList, "emp" : emp})
    else:
        if request.POST.get("Update") == "Update":
            # Update data :
            try:
                EmpId = empid
                Ename = request.POST.get('txtEname')
                Password = request.POST.get('txtPwd')
                Gender = request.POST.get('Gender')
                Phone = request.POST.get('txtPhone')
                Email = request.POST.get('txtEmail')
                DOB = request.POST.get('txtDOB') or None
                salary_value = request.POST.get('txtSalary', '').strip()
                Salary = int(salary_value) if salary_value else None
                Address = request.POST.get('txtAddress')
                dept_value = request.POST.get('ddlDeptNo')
                DeptNo = int(dept_value) if dept_value and dept_value != '0' else None
                
                with connection.cursor() as cursor:
                    cursor.execute("""
                    UPDATE employee
                    SET Ename = %s, Password = %s, Gender = %s,
                        Phone = %s, Email = %s, DOB = %s, Salary = %s,
                        Address = %s, DeptNo = %s
                        WHERE EmpId = %s
                        """, [Ename, Password, Gender, Phone, Email, DOB, Salary, Address, DeptNo, empid])
                
                return redirect("homepage")
            except (TypeError, ValueError, DatabaseError):
                messages.error(request, "Unable to update the employee. Check the entered data.")
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM employee WHERE EmpId = %s", [empid])
                emp = cursor.fetchone()
                cursor.execute("SELECT * FROM department")
                columns = [column[0] for column in cursor.description]
                deptList = [dict(zip(columns, row)) for row in cursor.fetchall()]
                return render(request, "edit.html", {
                    "ErrorMessage": "Unable to update the employee. Check the entered data.",
                    "data": deptList,
                    "emp": emp,
                })
        else:
            return redirect("homepage")

def Delete(request, empid):
    if request.method == "GET":
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM employee WHERE EmpId = %s", [empid])
            emp = cursor.fetchone()
    
            cursor.execute("SELECT * FROM department")
            columns = [column[0] for column in cursor.description]
            deptList = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return render(request, "delete.html", { "data": deptList, "emp" : emp})
    else:
        if request.POST.get("Delete") == "Do you really want to delete...!":
            # Delete data :
            try:
                cursor = connection.cursor()
                cursor.execute("Delete from employee WHERE EmpId = %s", [empid])
                
                return redirect("homepage")
            except (TypeError, ValueError, DatabaseError):
                  pass
        else:
            return redirect("homepage")