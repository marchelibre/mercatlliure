from panier import models
from django.test import TestCase, RequestFactory, Client
from models import Panier, Item
from django.contrib.auth.models import User, AnonymousUser
import datetime
from decimal import Decimal
from panier import Panier

class PanierAndItemModelsTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.request = RequestFactory()
        self.request.user = AnonymousUser()
        self.request.session = {}

    def _create_panier_in_database(self, creation_date=datetime.datetime.now(),
            checked_out=False):
        """
            Helper function so I don't repeat myself
        """
        panier = models.Panier()
        panier.creation_date = creation_date
        panier.checked_out = False
        panier.save()
        return panier

    def _create_item_in_database(self, panier, product, quantity=1, 
            unit_price=Decimal("100")):
        """
            Helper function so I don't repeat myself
        """  
        item = Item()
        item.panier = panier
        item.product = product
        item.quantity = quantity
        item.unit_price = unit_price
        item.save() 

        return item

    def _create_user_in_database(self):
        """
            Helper function so I don't repeat myself
        """ 
        user = User(username="user_for_sell", password="sold", 
                email="example@example.com")
        user.save() 
        return user

    def test_panier_creation(self):
        creation_date = datetime.datetime.now()
        panier = self._create_panier_in_database(creation_date)
        id = panier.id

        panier_from_database = models.Panier.objects.get(pk=id)
        self.assertEquals(panier, panier_from_database)
        

    def test_item_creation_and_association_with_panier(self):
        """
            This test is a little bit tricky since the Item tracks
            any model via django's content type framework. This was
            made in order to enable you to associate an item in the
            panier with your product model.
            
            As I wont make a product model here, I will assume my test
            store sells django users (django.contrib.auth.models.User) 
            (lol) so I can test that this is working.

            So if you are reading this test to understand the API,
            you just need to change the user for your product model
            in your code and you're good to go.
        """
        user = self._create_user_in_database()

        panier = self._create_panier_in_database()
        item = self._create_item_in_database(panier, user, quantity=1, unit_price=Decimal("100"))

        # get the first item in the panier
        item_in_panier = panier.item_set.all()[0]
        self.assertEquals(item_in_panier, item, 
                "First item in panier should be equal the item we created")
        self.assertEquals(item_in_panier.product, user,
                "Product associated with the first item in panier should equal the user we're selling")
        self.assertEquals(item_in_panier.unit_price, Decimal("100"), 
                "Unit price of the first item stored in the panier should equal 100")
        self.assertEquals(item_in_panier.quantity, 1, 
                "The first item in panier should have 1 in it's quantity")


    def test_total_item_price(self):
        """
        Since the unit price is a Decimal field, prefer to associate
        unit prices instantiating the Decimal class in 
        decimal.Decimal.
        """
        user = self._create_user_in_database()
        panier = self._create_panier_in_database()

        # not safe to do as the field is Decimal type. It works for integers but
        # doesn't work for float
        item_with_unit_price_as_integer = self._create_item_in_database(panier, product=user, quantity=3, unit_price=100)

        self.assertEquals(item_with_unit_price_as_integer.total_price, 300)
        
        # this is the right way to associate unit prices
        item_with_unit_price_as_decimal = self._create_item_in_database(panier,
                product=user, quantity=4, unit_price=Decimal("3.20"))
        self.assertEquals(item_with_unit_price_as_decimal.total_price, Decimal("12.80"))

    def test_update_panier(self):
        user = self._create_user_in_database()
        panier = Panier(self.request)
        panier.new(self.request)
        panier.add(product=user, quantity=3, unit_price=100)
        panier.update(product=user, quantity=2, unit_price=200)
        self.assertEquals(panier.summary(), 400)
        self.assertEquals(panier.count(), 2)

    def test_item_unicode(self):
        user = self._create_user_in_database()
        panier = self._create_panier_in_database()

        item = self._create_item_in_database(panier, product=user, quantity=3, unit_price=Decimal("100"))

        self.assertEquals(item.__unicode__(), "3 units of User")
