# Create your views here.
from panier.panier import Panier
from myproducts.models import Product

def add_to_panier(request, product_id, quantity):
    product = Product.objects.get(id=product_id)
    panier = Panier(request)
    panier.add(product, product.unit_price, quantity)

def remove_from_panier(request, product_id):
    product = Product.objects.get(id=product_id)
    panier = Panier(request)
    panier.remove(product)

def get_panier(request):
    return render_to_response('panier.html', dict(panier=Panier(request)))