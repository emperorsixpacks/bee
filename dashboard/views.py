from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Withdraws, Wallet, Deposits, DailyPayout
from django.contrib import messages
from decimal import Decimal
from .forms import WithdrawForm, DepositForm
from accounts.views import login_required_active
from accounts.models import RefPayouts, UserProfile
from home.models import Settings, WalletAddress

settings = Settings.objects.get(id=1)
charge =settings.charge_in_percentage
deposit_text =settings.deposit_text
withdraw_text =settings.withdrawal_text
address = WalletAddress.objects.all()


@login_required_active()
@login_required(login_url='login')
def dashboard(request):
    withdraws = Withdraws.objects.filter(user=request.user)[:5]
    deposit = Deposits.objects.filter(user=request.user)[:5]
    referrals = UserProfile.objects.get(user=request.user)
    first_gen_referrals = referrals.first_gen.all()
    second_gen_referrals = referrals.second_gen.all()
    ref_earn = RefPayouts.objects.filter(user=request.user)[:10]
    context = {
        'withdraws': withdraws,
        'deposit': deposit,
        'first_gen': first_gen_referrals,
        'second_gen': second_gen_referrals,
        'ref': ref_earn,

    }
    template = 'dashboard.html'
    return render(request, template, context)


@login_required_active()
@login_required(login_url='login')
def withdraw(request):
    table = Withdraws.objects.filter(user=request.user)
    if request.method == 'POST':
        wallet = Wallet.objects.get(user=request.user)
        form = WithdrawForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            percent = obj.amount * charge
            obj.amount += percent
            if Decimal(obj.amount) > wallet.balance:
                messages.error(request, 'Insufficient funds')
                return redirect('withdraw')
            elif obj.amount < 5:
                messages.error(request, 'Invalid amount')
            elif obj.amount <= 0:
                messages.error(request, 'Invalid amount')
                return redirect('withdraw')
            if len(obj.wallet_address) < 34 > 34:
                messages.error(request, 'Invalid wallet address')
                return redirect('withdraw')
            else:
                obj.save()
                messages.success(request, 'Withdrawal successful')
                return redirect('withdraw')
        else:
            return form.errors
    else:
        form = WithdrawForm()
    template = 'withdraw.html'
    return render(request, template, {'form': form, 'table': table, 'text': withdraw_text})


@login_required_active()
@login_required(login_url='login')
def deposits(request):
    table = Deposits.objects.filter(user=request.user)
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            if obj.amount <= 0:
                messages.error(request, 'Invalid amount')
                return redirect('withdraw')
            elif len(obj.wallet_address) < 34:
                messages.error(request, 'Invalid wallet address')
                return redirect('deposits')
            else:
                obj.user = request.user
                obj.save()
                messages.success(request, 'Deposit successful, Pending approval')
                return redirect('deposits')
        else:
            return form.errors
    else:
        form = DepositForm()
    template = 'deposit.html'
    return render(request, template, {'form': form, 'table': table, 'text': deposit_text, 'address': address})




@login_required_active()
@login_required(login_url='login')
def earnings_dashboard(request):
    user = Wallet.objects.get(user=request.user)
    payout = DailyPayout.objects.filter(wallet=user)
    refpayout = RefPayouts.objects.filter(user=request.user)
    referrals = UserProfile.objects.get(user=request.user)
    first_gen_referrals = referrals.first_gen.all()
    second_gen_referrals = referrals.second_gen.all()
    sum_balance = 0
    payout_sum = 0
    for i in payout:
        payout_sum += i.amount
    for i in refpayout:
        sum_balance += i.amount

    context = {
        'payout': payout,
        'ref': refpayout,
        'first_gen': first_gen_referrals,
        'second_gen': second_gen_referrals,
        'total_ref_gain': sum_balance,
        'payout_total': payout_sum,
    }
    template = 'earnings_dashboard.html'
    return render(request, template, context)
