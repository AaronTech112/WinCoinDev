from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm,  ProfileForm
from .models import InvestmentPlan, Transaction, CustomUser
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

def home(request):
    packages = InvestmentPlan.objects.all()
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        pass
    return render(request, 'WinCoinDevApp/index.html', {'packages':packages})

def login_user(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == "POST":
            email = request.POST["email"]
            password = request.POST["password"]
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                error_message = "Invalid Username or Password"
                return render(request, 'WinCoinDevApp/login.html', {"error_message": error_message})

    return render(request, 'WinCoinDevApp/login.html')

def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.status = 'investor'
                user.save()  # Save the user before authenticating
                login(request, user)
                messages.success(request, f'Account created for {user.username}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Error creating account. Please check the form.')
        else:
            form = RegisterForm()
    return render(request, 'WinCoinDevApp/register.html', {'form': form})


@login_required(login_url='/login_user')
def packages(request):
    packages = InvestmentPlan.objects.all()
    context = {'packages': packages}  # Corrected line
    return render(request, 'WinCoinDevApp/dashboard/packages.html', context)


def transaction_history(request):
    transactions = Transaction.objects.filter(user=request.user)
    context = {'transactions': transactions}  # Corrected line
    return render(request, 'WinCoinDevApp/dashboard/transaction_history.html', context)
    

def logout_user(request):
    logout(request)
    return redirect('home')

from decimal import Decimal, ROUND_HALF_UP

def update_balance(request):
    # Retrieve all users with active investment plans
    user = request.user
    investment_id = user.investment_plan.id
    investment_plan = InvestmentPlan.objects.get(id=investment_id)
    if investment_plan:
        # Calculate the daily return based on the investment plan
        increament_per_4_seconds = (4 * investment_plan.increament_rate_per_day) / 86400
        
        # Round the result to three decimal places
        increament_per_4_seconds = Decimal(str(increament_per_4_seconds)).quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)
        
        # Update the user's balance
        user.balance += increament_per_4_seconds
        user.save()

    return JsonResponse({'status': 'success'})

@login_required(login_url='/login_user')
def dashboard(request):
    user = request.user
    try:
        recent_deposit = Transaction.objects.filter(transaction_type='deposit').order_by('-transaction_date').first()
        if recent_deposit.transaction_status == 'approved':
            update_balance(request)
            package = user.investment_plan.amount 
            return render(request, 'WinCoinDevApp/dashboard/index_2.html',{'package':package, })
        else:
            package = 'None'
            user.balance = 0
            user.save()
            return render(request, 'WinCoinDevApp/dashboard/index_2.html',{'package':package})
    except Exception as e:
        package = 'None'
        user.balance = 0
        user.save()
        return render(request, 'WinCoinDevApp/dashboard/index_2.html',{'package':package})
    # Save the user instance after updating the balance

               
@login_required(login_url='/login_user')
def deposit(request,package):
    user = request.user
    if user.investment_plan is not None:
        return redirect('dashboard')
    else:
        package = InvestmentPlan.objects.get(name = package)
        amount = package.amount
        context = {'amount': amount,'package':package}
    return render(request, 'WinCoinDevApp/dashboard/PayOut.html',context)

@login_required(login_url='/login_user')
def pending(request,):
    return render(request, 'WinCoinDevApp/dashboard/pending.html')

@login_required(login_url='/login_user')
def pending_withdrawal(request,):

    return render(request, 'WinCoinDevApp/dashboard/pending_withdrawal.html')

@login_required(login_url='/login_user')
def insufficient_funds(request,):

    return render(request, 'WinCoinDevApp/dashboard/insufficient_funds.html')

@login_required(login_url='/login_user')
def withdraw(request):
    user = request.user
    if request.method == 'POST':
        amount = int(request.POST['amount'])
        wallet_address = request.POST['wallet_address']      
        if user.balance >= amount:
            user.balance -= amount  # Deduct the amount from the user's balance
            user.save()          
            transaction = Transaction.objects.create(
                user=user,
                amount=amount,
                wallet_address=wallet_address,  # Use the wallet_address from the form
                transaction_type='withdrawal',
                transaction_status='pending',
            )
            transaction.save()
            
            messages.success(request, 'Withdrawal request submitted successfully.')
            return redirect('pending_withdrawal')
        else:
            messages.error(request, 'You do not have enough balance to withdraw.')
            return redirect('insufficient_funds')
    try:
        recent_deposit = Transaction.objects.filter(transaction_type='deposit').order_by('-transaction_date').first()
        if recent_deposit.transaction_status == 'approved':
            update_balance(request)
        else:
            user.balance = 0
            user.save()
            return render(request, 'WinCoinDevApp/dashboard/withdraw.html')
    except Exception as e:
        user.balance = 0
        user.save()
        return render(request, 'WinCoinDevApp/dashboard/withdraw.html')

    return render(request, 'WinCoinDevApp/dashboard/withdraw.html',)

@login_required(login_url='/login_user')
def upload_proof(request,package):
    investment_plan = get_object_or_404(InvestmentPlan, name = package)
    plan = InvestmentPlan.objects.get(name = package)
    user = request.user
    if request.method == 'POST' and request.FILES['proof_of_payment']:
        proof_of_payment = request.FILES['proof_of_payment']    
        if user.investment_plan is None:
            user.investment_plan = investment_plan
            user.balance = investment_plan.amount
            user.save()

            transaction = Transaction.objects.create(
            user=user,
            amount= investment_plan.amount,
            transaction_type= 'deposit',
            transaction_status='pending',
            proof_of_payment=proof_of_payment  
        )
            transaction.save()
            return redirect('pending')
        else:
            messages.error(request, 'You already have an investment plan.')
            return redirect('dashboard')
        
       
    
    return render(request, 'WinCoinDevApp/dashboard/upload_proof.html',{'package':package})


def profile_page(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProfileForm(instance=request.user)  
    return render(request, 'WinCoinDevApp/dashboard/profile_page.html',{'form':form})




def earnings(request):
    return render(request, 'WinCoinDevApp/dashboard/Earning.html')

def investment_plans(request):
    return render(request, 'WinCoinDevApp/plan.html')

def about(request):
    return render(request, 'WinCoinDevApp/about.html')

def contact(request):
    return render(request, 'WinCoinDevApp/contact.html')

def blogs(request):
    return render(request, 'WinCoinDevApp/blogs.html')

# Add more views as needed
