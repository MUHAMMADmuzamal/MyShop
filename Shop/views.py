from django.shortcuts import render,HttpResponse,redirect
from .models import Product, Contact, Orders, OrderUpdate
from math import ceil
import json
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import  authenticate,login,logout
# Create your views here.



def index(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds':allProds}
    return render(request, 'shop/index.html', params)

def searchMatch(query, item):
    '''return true only if query matches the item'''
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]

        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg": ""}
    if len(allProds) == 0 or len(query)<4:
        params = {'msg': "Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', params)


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    thank = False
    if request.method=="POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank = True
    return render(request, 'shop/contact.html', {'thank': thank})


def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status":"success", "updates": updates, "itemsJson": order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')

    return render(request, 'shop/tracker.html')


def productView(request, myid):

    # Fetch the product using the id
    product = Product.objects.filter(id=myid)
    return render(request, 'shop/prodView.html', {'product':product[0]})


def checkout(request):
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Orders(items_json=items_json, name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone, amount=amount)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
    return render(request, 'shop/checkout.html')

#-----------------------------------------User authentication-------------------------
def handleSignup(request):
     if request.method == 'POST':
         username = request.POST['username']
         firstname = request.POST['firstname']
         lastname = request.POST['lastname']
         email = request.POST['email']
         pass1 = request.POST['pass1']
         pass2 = request.POST['pass2']

         #check for errorneous inputs
         if len(username) > 10:
            messages.error(request, 'Username must be under 10 Characters and Username must b uniqe.')
            return redirect('ShopHome')
         if pass1 != pass2:
            messages.error(request, 'Password do not match.')
            return redirect('ShopHome')
         if not username.isalnum():
            messages.error(request, 'Username should only contain letters and numbers.')
            return redirect('ShopHome')
         #create the user
         myuser = User.objects.create_user(username,email,pass1)
         myuser.first_name = firstname
         myuser.last_name = lastname
         myuser.save()
         messages.success(request,"Your iCoder account has been successfully created")
         return redirect('/')
     else:  
        return HttpResponse('404 - Not Found')
def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpass = request.POST['loginpass']
        
        user = authenticate(username=loginusername,password=loginpass)
        if user is not None:
            login(request,user)
            messages.success(request,"Successfully Logged In")
            return redirect('ShopHome')
        else:
            messages.error(request,"Invalid Credentials Please try again")
            return redirect('ShopHome')
def handleLogout(request):
   # if request.method == 'POST':
    logout(request)
    messages.success(request,"Successfully Logged Out")
    return redirect('ShopHome')


