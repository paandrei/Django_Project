from django.shortcuts import render, redirect
import bcrypt 
import random
from Bank import models
from Bank import database as db
from currency_converter import views as w_c
from datetime import datetime

def homepage(request):
    #if the user is not logged, he cant access /LogIn/User
    request.session['logged'] = False
    return render(request,'Bank/Homepage.html')

def feedback(request):
    if request.method == 'POST':
        name = request.POST.get('Name')
        email = request.POST.get('Email')
        subject = request.POST.get('Subject')
        the_request = request.POST.get('the_request')
        print(name, '-------')
        if name != '' and email != '' and subject != '' and the_request != '':
            models.Feedback.objects.create( 
                                    name = name,
                                    email = email,
                                    subject = subject,
                                    the_request = the_request)
            return redirect('/')
        else:
            return redirect('/')  
    else: 
        return redirect('/')

def password_constrains_verification(password):

    """ The password will be verified to meet all the criteria
        len(password)>8
        number of uppercase > 0
        number of lowercase > 0 
        number of digits    > 0
        number of symbols   > 0 
    """
    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
     
    lc = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
          'm', 'n', 'o', 'p', 'q',
          'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    uc = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
          'I', 'J', 'K', 'M', 'N', 'O', 'p', 'Q',
          'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
     
    sym = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|',
           '~', '>', '*', '<', '!']
        
    #number of specific characters
    no_digits = 0
    no_lc = 0
    no_uc = 0
    no_sym = 0
    #password verification
    if len(password) < 8:
        return False 
    else:
        for _ in password:
            if _ in digits:
                no_digits +=1
            elif _ in lc:
                no_lc += 1 
            elif _ in uc:
                no_uc +=1
            elif _ in sym:
                no_sym += 1 
        #verify if password has all the requests
        if no_digits > 0 and no_lc > 0 and no_uc > 0 and no_sym > 0: 
            return True
        else:
            return False
    
def SignUp(request):

 # details of user at registration
    request.session['logged'] = False
    details = {
        'FirstName':False, 
        'LastName':False, 
        'DateOfBirth':False, 
        'Country':False, 
        'City':False, 
        'PostalCode':False, 
        'Email':False, 
        'Phone':False, 
        'Username':False, 
        'Password':False, 
        'Currency': False,
        'Photo':False,
        'IBAN': False
        }
    
    a =False 

    if request.method == 'POST':
        for key in details.keys():
            if key == 'Password':
                detail = request.POST.get(key)
                if detail == '':
                    details[key] = ''
                else :
                    if password_constrains_verification(detail):
                        # converting to a corresponding array of bytes
                        byte_password = detail.encode('utf-8')
                        #generate the salt for the password to make the hash unic
                        password_salt = bcrypt.gensalt()
                        #hashing password 
                        hash_password = bcrypt.hashpw(byte_password,password_salt)
                        hash_password = hash_password.decode('utf-8')
                        details[key]=hash_password
                    else:
                        details[key] = 'inccorect_password'
                        return render(
                            request, 
                            'Bank/signUp.html', 
                            {
                                'text': 'You have missed some information', 
                                'details':details, 
                                'password_incorect': 'The password does not meet all the criteria', 
                                'currency_data': w_c.transform_data()
                                }
                                )
            elif key == 'Photo':
                pass
            elif key == 'IBAN':
                nr = random.randint(1000,9999)
                nr2 = random.randint(10000,99999)
                IBAN  = f'{details["Country"][0:2].upper()}{str(details["PostalCode"])[0:3]}{nr}{nr2}'
                details[key]=IBAN    
            else:
                detail = request.POST.get(key)
                details[key]=detail 
        for value in details.values():
                if value == "" :
                    a = True
        if a is True:
            return render(
                request, 
                'Bank/signUp.html', 
                {
                    'text': 'You have missed some information', 
                    'details':details, 
                    'currency_data': w_c.transform_data()
                    }
                    )
        else:
            try:
                models.Account.objects.create(
                    first_name = details['FirstName'],
                    last_name = details['LastName'],
                    date_of_birth = details['DateOfBirth'],
                    country = details['Country'],
                    city = details['City'],
                    postal_code = details['PostalCode'],
                    email = details['Email'],
                    phone = details['Phone'],
                    username = details['Username'],
                    password = details['Password'],
                    iban = details['IBAN'],
                    currency = details['Currency']
                )
                # create a register for each account
                
            
            except BaseException:
                return render(
                            request, 
                            'Bank/signUp.html', 
                            { 
                                'details':details, 
                                'username_incorect': 'You have to change the username.', 
                                'currency_data': w_c.transform_data()
                                }
                                )
            try:
                register_db = db.AccountRegister(f'''..\Project\Bank\RegisterAccount\{details['FirstName']}_{details['LastName']}.db''')
                register_db.create_table()
            except BaseException as e: 
                return render(
                            request, 
                            'Bank/signUp.html', 
                            { 
                                'details':details, 
                                'text': 'Please contact the Bank by sending a form.', 
                                'currency_data': w_c.transform_data()
                                }
                                )

        return render(
            request, 
            'Bank/signUp.html',
            {
                'details':details, 
                'currency_data': w_c.transform_data(),
                'valid_signup': True 
                }
                )
    else:
        
        return render(
            request, 
            'Bank/signUp.html',
            { 
                'details':details, 
                'currency_data': w_c.transform_data(),
                }
                )

def LogIn(request):

    if request.method == 'POST':
        """take user input infromation"""
        db_username = request.POST.get('Username')
        password = request.POST.get('Password')
        """encode the string password to bytes """
        data_base = db.AccouuntDatabase()
        """read the password for the user input username"""
        try:                   #password from database
            db_password = data_base.read_password_from_db(db_username)[0][0]
        except BaseException: #if the password db_username do not exist
                db_password = False 
        
        if db_password is not False:
            db_password =db_password.encode('utf-8')
            #bytes password
            b_password = password.encode('utf-8')
            
            if bcrypt.checkpw(b_password, db_password):
                request.session['username'] = db_username #store the username for account logged to be used in deposit 
                account = models.Account.objects.get(pk = db_username)
                try:
                    account = models.Balance.objects.get(pk = account.iban)
                except BaseException:
                    models.Balance.objects.create(
                            iban = account.iban,
                            username = models.Account.objects.get(pk = db_username),
                        )
                request.session['errors'] = {}
                request.session['text'] = None 
                request.session['Action'] = False
                request.session['logged'] = True 
                request.session['iban'] = account.iban
                return redirect('/LogIn-Active')
            else:
                request.session['logged'] = False
                return render(request,'Bank/LogIn.html', {'wrong_password':True})
        else:
            request.session['logged'] = False
            return render(request,'Bank/LogIn.html',{'miss_information':True})
    else:
        request.session['logged'] = False
        return render(request,'Bank/LogIn.html')

def login_active(request):
    """ this will return the mainpage of login url (/LogIn-Active)"""

    logged = request.session['logged']   # store data between requests - keep the user logged 
    action = request.session['Action'] # retrive data from sesion 'Action' form different functions
    text = request.session['text'] # retrive data from sesion 'text' form different functions
    o_username = request.session['username'] # retrive the logged username  form different functions
    iban = request.session['iban'] # retrive the iban entered or transmited from another function/request  
    errors = request.session['errors'] # retrive the errors from another function/request  

    acc_b = models.Balance.objects.get(pk = iban) # it is created an object from database that has primary key = iban
    if logged:
        return render(request, 'Bank/logged.html',
                        {
                        'currency_data': w_c.transform_data(), 
                        'username':o_username, 
                        'first_name': acc_b.username.first_name,
                        'last_name':acc_b.username.last_name, 
                        'IBAN': iban,
                        'balance':acc_b.balance,
                        'account_currency':acc_b.username.currency,
                        'currency_data': w_c.transform_data(),
                        'Action': action,
                        'text':text,
                        'errors': errors
                        })
    else: 
        return redirect('/')         
            
def deposit(request):

    user_log = request.session['logged'] #it is verified is user is connected 
    request.session['errors'] = {}
    iban = request.session['iban']

    if user_log:
        o_username = request.session['username']
        account = models.Account.objects.get(pk = o_username)

        if request.method == 'POST' and 'Deposit' in request.POST:
            
            currency = request.POST.get('Currency')
            amount_to_deposit = request.POST.get('initial_deposit')

            if amount_to_deposit == '':
                request.session['Action'] = False
                request.session['errors']['Attention : Amount is 0'] = True
                return redirect('/LogIn-Active')
            else:
                if amount_to_deposit.isdigit():
                    amount_to_deposit = float(amount_to_deposit)
                    if currency == account.currency: 
                        record = models.Balance.objects.get(pk = iban)
                        record.balance += amount_to_deposit
                        record.save(update_fields=['balance'])
                        request.session['Action'] = True 
                        request.session['text'] = 'Your deposit action has been a succes.'

                        #save the action in the account register
                        register_db = db.AccountRegister(f'''..\Project\Bank\RegisterAccount\{account.first_name}_{account.last_name}.db''')
                        register_db.create_table()
                        register_db.write_in_database('DEPOSIT',amount_to_deposit, account.currency, datetime.now())

                        return redirect('/LogIn-Active')
                    else:
                        request.session['Action'] = False
                        request.session['errors']['Currency does not match'] = True
                        return redirect('/LogIn-Active')
                else:
                    request.session['Action'] = False
                    request.session['errors']['Amount is not digit'] = True
                    return redirect('/LogIn-Active')
        elif 'Withdraw' in request.POST: 
            return withdraw(request)
        else:
            return transfer(request)
    else:
        return render(request,'Bank/LogIn.html')
    
def withdraw(request):
    o_username = request.session['username']
    account = models.Account.objects.get(pk = o_username)
    iban = request.session['iban']
    user_log = request.session['logged']
    request.session['errors'] = {}
    
    if user_log:
        if request.method == 'POST' and 'Withdraw' in request.POST:
            amount_to_withdraw = request.POST.get('withdraw')

            if amount_to_withdraw == '':
                request.session['Action'] = False
                request.session['errors']['Amount is 0'] = True
                return redirect('/LogIn-Active')
            else:
                if amount_to_withdraw.isdigit():
                    amount_to_withdraw = float(amount_to_withdraw)
                    record = models.Balance.objects.get(pk = iban)
                    if amount_to_withdraw <= record.balance:
                        record.balance -= amount_to_withdraw
                        record.save(update_fields=['balance'])
                        request.session['Action'] = True
                        request.session['text'] = 'Your withdraw action has been a succes.'
                        #save the action in the account register

                        register_db = db.AccountRegister(f'''..\Project\Bank\RegisterAccount\{account.first_name}_{account.last_name}.db''')
                        register_db.create_table()
                        register_db.write_in_database('WITHDRAW',amount_to_withdraw, account.currency, datetime.now())

                        return redirect('/LogIn-Active')
                    else:
                        request.session['Action'] = False
                        request.session['errors']["You don't have enough money."] = True
                        return redirect('/LogIn-Active')
                else:
                    request.session['Action'] = False
                    request.session['errors']['Amount is not digit'] = True
                    return redirect('/LogIn-Active')
        else:
            return redirect('/LogIn-Active')
    else:
        return render(request,'Bank/Homepage.html')
    
def transfer(request):
    # you can make more details regardin the currency of the account, if it is acceptable to transfer from one currency to another 
    iban = request.session['iban']
    user_log = request.session['logged']
    request.session['errors'] = {}
    o_username = request.session['username']
    account = models.Account.objects.get(pk = o_username)
    if user_log:
        if request.method == 'POST' and 'Transfer' in request.POST:

            amount_to_transfer = request.POST.get('amount')
            input_iban = request.POST.get('iban')

            from_iban = models.Balance.objects.get(pk = iban)
            try:
                to_iban = models.Balance.objects.get(pk = input_iban)
                to_iban_currency = to_iban.username.currency

            except BaseException:
                request.session['Action'] = False
                request.session['errors']['Inccorect IBAN'] = True
                return redirect('/LogIn-Active')

            if amount_to_transfer == '' or amount_to_transfer.isalpha():
                request.session['Action'] = False
                request.session['errors']['Inccorect Amount'] = True
                return redirect('/LogIn-Active')
            elif to_iban_currency != from_iban.username.currency:
                request.session['Action'] = False
                request.session['errors']['The account you want to transfer has different currency'] = True
                return redirect('/LogIn-Active')
            elif float(amount_to_transfer) <= from_iban.balance:
                to_iban.balance += float(amount_to_transfer)
                to_iban.save(update_fields=['balance'])

                from_iban.balance -= float(amount_to_transfer)
                from_iban.save(update_fields=['balance'])

                request.session['Action'] = True
                request.session['text'] = 'Your transfer action has been a succes.'

                from_register_db = db.AccountRegister(f'''..\Project\Bank\RegisterAccount\{account.first_name}_{account.last_name}.db''')
                from_register_db.create_table()
                from_register_db.write_in_database('-TRANSFER',amount_to_transfer, account.currency, datetime.now())

                to_register_db = db.AccountRegister(f'''..\Project\Bank\RegisterAccount\{to_iban.username.first_name}_{to_iban.username.last_name}.db''')
                to_register_db.create_table()
                to_register_db.write_in_database('+TRANSFER',amount_to_transfer, account.currency, datetime.now())
                return redirect('/LogIn-Active')
            else:
                request.session['Action'] = False
                request.session['errors']["You don't have enough money."] = True
                return redirect('/LogIn-Active')
        else:
            return redirect('/LogIn-Active')
        
def register(request):
    o_username = request.session['username']
    account = models.Account.objects.get(pk = o_username)
    logged = request.session['logged']
    if request == 'POST':
        pass
    else:
        if logged:
            register_db = db.AccountRegister(f'''..\Project\Bank\RegisterAccount\{account.first_name}_{account.last_name}.db''')
            transactions = register_db.read_from_database()
            return render(request,'Bank/Register.html', {'transactions':transactions})
