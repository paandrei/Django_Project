from django.shortcuts import render
import requests
import json
import os 


def transform_data(file_path=None):
    #get current directory
    module_dir = os.path.dirname(__file__)
    #add the path to currencies.json
    if file_path is None:
        file_path = os.path.join(module_dir, 'currency_info/currencies.json')
    else: 
        pass
    
    with open (file_path, 'r') as f:
        currency_data = json.loads(f.read())

    return currency_data

def save_currency_exchang():
    pass 

def show(request):
    if request.method == 'POST':
        try:
            amount = float(request.POST.get('amount'))
            currency_from = request.POST.get('currency_from')
            currency_to = request.POST.get('currency_to')
            exchange_rates = requests.get("https://openexchangerates.org/api/latest.json?app_id=75a656f72868461692765f2865ec8e85")
            rates = exchange_rates.json()['rates']
            dollar_to_currencyt_from = float(rates[currency_from])
            dollar_to_currencyt_to = float(rates[currency_to])
            rates = amount*(dollar_to_currencyt_to/dollar_to_currencyt_from)
            return render(request,"currency_converter/exchange.html", {'currency_data': transform_data(), 'result':('%.2f')%rates, 'currency_to':currency_to})
        except BaseException:
            return render(request,"currency_converter/exchange.html", {'currency_data': transform_data()})
    else:
         return render(request,"currency_converter/exchange.html", {'currency_data': transform_data()})

