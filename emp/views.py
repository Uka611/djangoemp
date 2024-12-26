from django.shortcuts import render, HttpResponse
from emp.models import Emp, Role, Depart
from datetime import datetime
from django.db.models import Q

# Create your views here.
def index(request):
    return render(request, 'index.html')

def all_emp(request):
    emps = Emp.objects.all()
    context = {
        'emps': emps
    }
    return render(request, 'all.html', context)

def add(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        salary = int(request.POST['salary'])
        bonus = int(request.POST['bonus'])
        phone = int(request.POST['phone'])
        dept = int(request.POST['dept'])  # Corrected field name and ensuring it's an integer id
        role = int(request.POST['role'])  # Corrected field name and ensuring it's an integer id
        new_emp = Emp(first_name=first_name, last_name=last_name, salary=salary, bonus=bonus, phone=phone, dept_id=dept, role_id=role, hire_date=datetime.now())
        new_emp.save()
        return HttpResponse('Employee added successfully')
    elif request.method == 'GET':
        departments = Depart.objects.all()
        roles = Role.objects.all()
        context = {
            'departments': departments,
            'roles': roles
        }
        return render(request, 'add.html', context)
    else:
        return HttpResponse('Error')

def remove(request,emp_id=0):
    if emp_id:
        try:
            emp_to_be_removed=Emp.objects.get(id=emp_id)
            emp_to_be_removed.delete()
            return HttpResponse("Emp REmoved Successful")
        except:
            return HttpResponse("not valid id")
        
    emps = Emp.objects.all()
    context={
        'emps':emps
    }
    return render(request, 'remove.html',context)

def filter(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        dept = request.POST.get('dept', 'all')
        role = request.POST.get('role', 'all')

        emps = Emp.objects.all()

        # Filter employees whose names contain the given input
        if name:
            emps = emps.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))

        # Filter by department if not 'All'
        if dept != 'all':
            emps = emps.filter(dept_id=dept)

        # Filter by role if not 'All'
        if role != 'all':
            emps = emps.filter(role_id=role)

        departments = Depart.objects.all()
        roles = Role.objects.all()
        context = {
            'emps': emps,
            'departments': departments,
            'roles': roles
        }
        return render(request, 'filter.html', context)
    elif request.method == 'GET':
        departments = Depart.objects.all()
        roles = Role.objects.all()
        context = {
            'departments': departments,
            'roles': roles
        }
        return render(request, 'filter.html', context)
    else:
        return HttpResponse('Error')
