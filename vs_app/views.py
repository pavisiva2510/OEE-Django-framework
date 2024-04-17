
from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from rest_framework import viewsets
from .models import Machine, ProductionLog
from .serializers import MachineSerializer, ProductionLogSerializer
from django.db.models import Sum
from rest_framework.response import Response
from decimal import Decimal


class MachinesViewSet(viewsets.ModelViewSet):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer


class ProductionLogViewSet(viewsets.ModelViewSet):
    queryset = ProductionLog.objects.all()
    serializer_class = ProductionLogSerializer

    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        
        results = []
        for log in queryset:
            machine = log.machine
            logs = ProductionLog.objects.filter(machine=machine)
            available_time = 3 * 8 * 60 

            actual_output = logs.aggregate(Sum('duration'))['duration__sum']or Decimal('0')
            good_products = logs.count() 
            total_products = len(logs)

            
            ideal_cycle_time = 0.083

            available_operating_time = total_products * ideal_cycle_time
            unplanned_downtime = available_time - available_operating_time

            
            availability = ((available_time - unplanned_downtime) / available_time) * 100
            performance = (ideal_cycle_time * actual_output / available_operating_time) * 100
            quality = (good_products / total_products) * 100

            oee = availability * performance * quality / 10000

            results.append({
                'machine': machine.machine_name,
                'oee': oee,
                'availability': availability,
                'performance': performance,
                'quality': quality,
            })
        return render(request, 'create_mission.html', {'results': results})


def calculate_oee(request):
    production_logs = ProductionLog.objects.all()
    results = []
    
    for log in production_logs:
        machine = log.machine
        logs = ProductionLog.objects.filter(machine=machine)
        available_time = Decimal(3 * 8 * 60)  
        actual_output = logs.aggregate(Sum('duration'))['duration__sum'] or Decimal(0) 
        good_products = logs.count()  
        total_products = Decimal(len(logs))  

        ideal_cycle_time = Decimal('0.083') 

        available_operating_time = total_products * ideal_cycle_time
        unplanned_downtime = available_time - available_operating_time

        availability = ((available_time - unplanned_downtime) / available_time) * Decimal(100)  # Ensure 100 is Decimal
        performance = (ideal_cycle_time * actual_output / available_operating_time) * Decimal(100)  # Ensure 100 is Decimal
        quality = (good_products / total_products) * Decimal(100) 
        oee = availability * performance * quality / Decimal(10000) 

        results.append({
            'machine': machine.machine_name,
            'oee': oee,
            'availability': availability,
            'performance': performance,
            'quality': quality,
        })
    
    return render(request, 'create_mission.html', {'results': results})

def SignupPage(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password_repeat = request.POST['password_repeat']
        if password!=password_repeat:
            return HttpResponse("Your password and comfort password are not same")
        else:
            my_user=User.objects.create_user(username, email, password)
            my_user.save()
        
            return redirect('login') 

    return render(request, 'signup.html')
def  LoginPage(request):
    if request. method == "POST":
        username = request. POST['username']
        password = request. POST['password']
    
        user=authenticate(request,username=username, password=password)
        if user is not None:
            login(request,user)

            return redirect('calculate_oee')
        else:
            return redirect('signup')
    return render(request,'login.html', {'error': 'Invalid credentials'})
