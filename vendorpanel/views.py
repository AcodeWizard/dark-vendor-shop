from django.shortcuts import render
from vendorpanel.forms import ProductForm
from main.models import Product
# Create your views here.
#get current user
def getUserID(request):
    current_user = request.user
    return current_user.id

#add product
def addProduct(request):
    form=ProductForm()
    ownerID=getUserID(request)
    return render(request, 'myproducts.html', {'form': form,'ownerID':ownerID})

#save product
def saveProduct(request):
    if request.method == 'POST':
        form=ProductForm(request.POST)
        form.save()
        return listProducts(request)
    else:
        raise Exception("405")

#get list of products
def listProducts(request):
    ownerID = getUserID(request)
    products=Product.objects.filter(productOwnerID=ownerID)
    return render(request,'listProducts.html',{'products':products})
