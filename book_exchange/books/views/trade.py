from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from books.models import Trade
from books.forms import TradeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required()
def user_trades(request: HttpRequest, user_id: int) -> HttpResponse:
    trades = Trade.objects.filter(receiver=user_id)
    context = {'trades': trades}
    return render(request, 'trade_detail.html', context)


@login_required()
def trade_create(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    trade_form = TradeForm(request.POST or None)
    if request.method == 'POST':
        if trade_form.is_valid():
            trade = trade_form.save(commit=False)
            trade.sender = request.user
            trade.receiver = trade_form.cleaned_data['to_book'].owner
            trade.save()
            messages.success(
                request,
                ('Ви успішно запропонували книгу на обмін!'),
            )
            return redirect('trade_create')
    else:
        trade_form = TradeForm(user=request.user)
    context = {'trade_form': trade_form}
    return render(request, 'trade.html', context)


@login_required()
def trade_delete(request: HttpRequest, trade_id: int) -> HttpResponse:
    trade = Trade.objects.get(pk=trade_id)
    if request.user.id == trade.receiver.id:
        trade.delete()
        messages.success(request, ('Ви успішно відмовили в обміні!'))
        return redirect('user_trades', request.user.id)
    else:
        return redirect('user_trades', request.user.id)


@login_required()
def trade_confirm(request: HttpRequest) -> HttpResponse:
    pass