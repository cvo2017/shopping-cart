import db
class Product:
    def __init__(self, name="", price=0.0, discountPercent=0):
            self.name = name
            self.price = price
            self.discountPercent = discountPercent

    def getDiscountAmount(self):
        discountAmount = self.price * self.discountPercent / 100
        return round(discountAmount, 2)

    def getDiscountPrice(self):
        discountPrice = self.price - self.getDiscountAmount()
        return round(discountPrice, 2)

class LineItem:
    def __init__(self, product=None, quantity=1):
            self.product = product
            self.quantity = quantity


    #change from getTotalItem to getTotal
    def getTotal(self, price):
        total = price * self.quantity
        return total

class Cart:
    def __init__(self, username):
        if db.selectItemCount(username) == 0:
            self.__lineItems = []
        else:
            self.__lineItems = db.getCart(username)

    def addItem(self, item):
        self.__lineItems.append(item)

    def removeItem(self, index):
        i = [index]
        dbDetail = [self.__lineItems[x] for x in i]
        self.__lineItems.pop(index)
        return dbDetail

    def modItem(self,index):
        i = [index]
        return [self.__lineItems[x] for x in i]

    def getItemCount(self):
        return len(self.__lineItems)  
    
    def __iter__(self):
        self.__index = -1
        return self

    def __next__(self):
        if self.__index == len(self.__lineItems)-1:
            raise StopIteration         
        self.__index += 1
        lineItem = self.__lineItems[self.__index]
        return lineItem
