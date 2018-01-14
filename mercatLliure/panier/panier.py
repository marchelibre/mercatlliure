import datetime
import models

PANIER_ID = 'PANIER-ID'

class ItemAlreadyExists(Exception):
    pass

class ItemDoesNotExist(Exception):
    pass

class Panier:
    def __init__(self, request):
        panier_id = request.session.get(PANIER_ID)
        if panier_id:
            try:
                panier = models.Panier.objects.get(id=panier_id, checked_out=False)
            except models.Panier.DoesNotExist:
                panier = self.new(request)
        else:
            panier = self.new(request)
        self.panier = panier

    def __iter__(self):
        for item in self.panier.item_set.all():
            yield item

    def new(self, request):
        panier = models.Panier(creation_date=datetime.datetime.now())
        panier.save()
        request.session[PANIER_ID] = panier.id
        return panier

    def add(self, product, unit_price, quantity=1):
        try:
            item = models.Item.objects.get(
                panier=self.panier,
                product=product,
            )
        except models.Item.DoesNotExist:
            item = models.Item()
            item.panier = self.panier
            item.product = product
            item.unit_price = unit_price
            item.quantity = quantity
            item.save()
        else: #ItemAlreadyExists
            item.unit_price = unit_price
            item.quantity += int(quantity)
            item.save()

    def remove(self, product):
        try:
            item = models.Item.objects.get(
                panier=self.panier,
                product=product,
            )
        except models.Item.DoesNotExist:
            raise ItemDoesNotExist
        else:
            item.delete()

    def update(self, product, quantity, unit_price=None):
        try:
            item = models.Item.objects.get(
                panier=self.panier,
                product=product,
            )
        except models.Item.DoesNotExist:
            raise ItemDoesNotExist
        else: #ItemAlreadyExists
            if quantity == 0:
                item.delete()
            else:
                item.unit_price = unit_price
                item.quantity = int(quantity)
                item.save()

    def count(self):
        result = 0
        for item in self.panier.item_set.all():
            result += 1 * item.quantity
        return result
        
    def summary(self):
        result = 0
        for item in self.panier.item_set.all():
            result += item.total_price
        return result

    def clear(self):
        for item in self.panier.item_set.all():
            item.delete()

