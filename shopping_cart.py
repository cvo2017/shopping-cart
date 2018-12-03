import db
from business import Product, LineItem, Cart

def show_title():
    print("The Shopping Cart program")
    print()
    
def show_menu_reg():
    print("COMMAND MENU")
    print("cart     - Show the cart")
    print("add      - Add an item to the cart")
    print("del      - Delete an item from cart")
    print("mod      - Edit an item in your cart")
    print("check    - Check out")
    print("exit     - Exit the program")
    print()

def show_products(products):
    print("PRODUCTS")
    line_format1 = "{:<5s} {:<25s} {:>10s} {:>10s} {:>12s}"
    line_format2 = "{:<5d} {:<25s} {:>10.2f} {:>10s} {:>12.2f}"
    print(line_format1.format("Item", "Name", "Price",
                              "Discount", "Your Price"))
    for i in range(len(products)):
        product = products[i]
        print(line_format2.format(i+1,
              product.name,
              product.price,
              str(product.discountPercent) + "%",
              product.getDiscountPrice()))
    print()

def show_cart(username):
    if db.selectItemCount(username) == 0:
        print("There are no items in your cart.\n")
    else:
        line_format1 = "{:<5s} {:<20s} {:>12s} {:>10s} {:>10s}"
        line_format2 = "{:<5d} {:<20s} {:>12.2f} {:>10d} {:>10.2f}"
        print(line_format1.format("Item", "Name", "Your Price",
                                  "Quantity", "Total"))
        i = 0
        total = 0
        
        cart = Cart(username)
        detail = Product()
        
        for item in cart:
            detail = db.getProductDetail(item.product)
            total += item.getTotal(detail.getDiscountPrice())
            
            print(line_format2.format(i+1,
                  detail.name,
                  detail.getDiscountPrice(),
                  item.quantity,
                  item.getTotal(detail.getDiscountPrice())
                  ))
            i += 1
        print("{:>66.2f}".format(total))
        print()

def add_item(products, username):
    number = int(input("Item number: "))
    quantity = int(input("Quantity: "))
    if number < 1 or number > len(products):
        print("No product has that number.\n")
    else:
        cart = Cart(username)
        product = products[number-1]
        item = LineItem(product, quantity)
        cart.addItem(item)
        
        #put in db
        db.addItemtoCart(username, product.name, quantity)
        
        print(product.name + " was added.\n")

def remove_item(username):
    number = int(input("Item number: "))
    
    if number < 1 or number > db.selectItemCount(username):
        print("The cart does not contain an item " +
              "with that number.\n")
    else:
        cart = Cart(username)
        item = []
        item = cart.removeItem(number-1)
        
        #delete in db
        db.deleteItemCart(username,item[0].product,item[0].quantity)
        
        print("Item " + str(number) +  "was deleted.\n")


def modItem(username):
    number = int(input("Item number: "))
    cart = Cart(username)
    
    if number < 1 or number > db.selectItemCount(username):
        print("The cart does not contain an item " +
              "with that number.\n")
    else:
        mod = int(input("Modify the quantity to: "))
        if mod > 0:
            item = []
            item = cart.modItem(number-1)

            #modify in db
            db.modifyItemCart(username, item[0].product, item[0].quantity, mod)

        else:
            print("Invalid number.\n")

def checkOut(username):
    show_cart(username)
    db.checkOut(username)
    print("Confirmed! Your order has been placed.\n")
            

def showDB():
    products = db.showInventory()
    show_products(products)


def show_loginuserRegister():
    print("reg      - userRegister an account")
    print("log      - Login to your account")
    print("exit     - Exit program\n")


def userRegister():
    username            = input("Username: ")
    password            = input("Password: ")

    if db.userRegister(username,password) == 1:
        print("Account create sucessfully!\n")
        print("Please choose command 'log' to login into your account")
    else:
        print("Username already exists, please try a different username or login.\n")
    
def login():
    username            = input("Username: ")
    password            = input("Password: ")

    status = db.userLogin(username,password)
    returnValue = ""
    
    if status == 0:
        print("User does not exist!\n")
    elif status == 1:
        print("Wrong password!\n")
    else:
        print("\n\nWELCOME User\n")
        returnValue = username
    return returnValue



def main():
    db.connectDB()
    username = ""
    show_loginuserRegister()
    
    while username == "":
        command = input("Command: ")
        if command == "reg":
            userRegister()
        elif command == "log":
            username = login()
        elif command == "exit":
            print("Bye!")
            break
        else:
            print("Not a valid command. Please try again.\n") 


    if username != "":
        show_title()

        # get a list of Product objects and display them
        products = db.showInventory()
        show_products(products)

        show_menu_reg()
        while True:        
                command = input("Command: ")
                if command == "cart":
                    show_cart(username)
                elif command == "add":
                    add_item(products, username)
                elif command == "del":
                    remove_item(username)
                elif command == "mod":
                    modItem(username)
                elif command == "show":
                    showDB()
                elif command == "check":
                    checkOut(username)
                elif command == "exit":
                    print("Bye!")
                    break 
                else:
                   print("Not a valid command. Please try again.\n")
             

        
        
if __name__ == "__main__":
    main()
