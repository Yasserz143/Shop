def exit_shop():
    print("Exiting the shop. Goodbye!")
    exit()
 
def add_balance(balance):
    try:
        amount = float(input("Enter amount to add to your balance: "))
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return balance
    balance += amount
    print(f"Balance updated. New balance: ${balance}")
    return balance 

def products(items, prices):
    if not items:
        print("No products available.")
        return
    print("Available Products:")
    for index, item in enumerate(items):
        print(f"{index + 1}. {item} - ${prices[index]}")   
 
def buy_product(items, prices, balance, cart):
    if not items:
        print("No products available to buy.")
        return balance
    try:
        item_number = int(input("Enter the product number you wish to buy: ")) - 1
    except ValueError:
        print("Invalid input.")
        return balance

    if item_number < 0 or item_number >= len(items):
        print("Invalid product number.")
        return balance
    item_price = prices[item_number]
    if balance >= item_price:
        cart.append(items[item_number])
        balance -= item_price
        print(f"You have purchased {items[item_number]} for ${item_price}. Remaining balance: ${balance}")
    else:
        print("Insufficient balance to purchase this product.")
    return balance

def add_items_and_prices():
    items = [it.strip() for it in input("Enter the Products, separated by commas: ").split(",") if it.strip()]
    prices_input = [p.strip() for p in input("Enter the price of the Products, separated by commas: ").split(",") if p.strip()]
    if len(items) != len(prices_input):
        print("The number of products and prices must match.")
        return [], []
    try:
        prices = [float(price) for price in prices_input]
    except ValueError:
        print("Invalid price entered. Please enter numeric prices.")
        return [], []
    return items, prices

def view_your_cart(cart, items, prices):
    if len(cart) == 0:
        print("Your cart is empty.")
        return
    print("Products in your cart:")
    total_cost = 0
    for index, item in enumerate(cart):
        # find the price via the index in items list; guard if item missing
        if item in items:
            item_price = prices[items.index(item)]
        else:
            # If item not found (shouldn't happen normally), treat price 0
            item_price = 0
        total_cost += item_price
        print(f"{index + 1}. {item} - ${item_price}")
    print(f"Total cost of Products in cart: ${total_cost}")
    
def delete_item_from_cart(cart, items, prices):
    if len(cart) == 0:
        print("Your cart is empty. No Products to delete.")
        return
    print("Products in your cart:")
    for index, item in enumerate(cart):
        print(f"{index + 1}. {item}")
    try:
        item_number = int(input("Enter the Product number you wish to delete from your cart: ")) - 1
    except ValueError:
        print("Invalid input.")
        return
    if item_number < 0 or item_number >= len(cart):
        print("Invalid Product number.")
        return
    removed_item = cart.pop(item_number)
    print(f"{removed_item} has been removed from your cart.") 
    
def confirm_purchase():
    confirmation = input("Do you want to confirm your purchase? (yes/no): ").strip().lower()
    if confirmation == 'yes':
        print("Purchase confirmed!")
        return True
    elif confirmation == 'no':
        print("Purchase cancelled.")
        return False
    else:
        print("Invalid input. Please enter 'yes' or 'no'.")
        return confirm_purchase()  # ask again until valid

def inventory_display(inventory, items, prices):
    if not inventory:
        print("Your inventory is empty.")
        return
    print("Your inventory:")
    total_cost = 0
    for index, item in enumerate(inventory):
        if item in items:
            item_price = prices[items.index(item)]
        else:
            item_price = 0
        total_cost += item_price
        print(f"{index + 1}. {item} - ${item_price}")
    print(f"Total cost/value of inventory: ${total_cost}")

def buyable_items(balance, items, prices):
    print("Products you can buy with your current balance:")
    can_buy = False
    for index, price in enumerate(prices):
        if price <= balance:
            print(f"{index + 1}. {items[index]} - ${price}")
            can_buy = True
    if not can_buy:
        print("No products available within your budget.")
    
shop_options = {
    1: add_balance,
    2: add_items_and_prices,
    3: products,
    4: buy_product,
    5: view_your_cart,
    6: delete_item_from_cart,
    7: confirm_purchase,
    8: inventory_display,
    9: buyable_items,
    10: exit_shop
}
shop_option_descriptions = {
    1: "Add balance",
    2: "Add products and prices",
    3: "View products",
    4: "Buy a product",
    5: "View cart",
    6: "Delete Product from cart",
    7: "Confirm purchase",
    8: "View inventory",
    9: "What can I buy with my budget?",
    10: "Exit shop"
}
    
def show_shop_options():
    print("\nPlease choose an option:")
    for key in sorted(shop_options.keys()):
        print(f"{key}. {shop_option_descriptions[key]}")
    

def shop_program():
    balance = 0.0
    items = []
    cart = []
    prices = []
    inventory = []   # <-- persistent inventory list

    print("Welcome to the Shop!")
    show_shop_options()
    
    while True:
        try:
            choice = int(input("\nEnter your choice: "))
        except ValueError:
            print("Please enter a number corresponding to an option.")
            continue

        if choice in shop_options:
            if choice == 1:
                balance = shop_options[choice](balance)
            elif choice == 2:
                items, prices = shop_options[choice]()    
            elif choice == 3:
                shop_options[choice](items, prices)
            elif choice == 4:
                balance = shop_options[choice](items, prices, balance, cart)
            elif choice == 5:
                shop_options[choice](cart, items, prices)
            elif choice == 6:
                shop_options[choice](cart, items, prices)
            elif choice == 7:
                # Confirm purchase: if confirmed, move cart items to inventory and clear cart
                confirmed = shop_options[choice]()  # confirm_purchase()
                if confirmed:
                    if not cart:
                        print("Your cart is empty. Nothing to confirm.")
                    else:
                        # show a small receipt and move items to inventory
                        print("Processing purchase... Here is your receipt:")
                        total = 0
                        for idx, it in enumerate(cart):
                            price = prices[items.index(it)] if it in items else 0
                            print(f"{idx + 1}. {it} - ${price}")
                            total += price
                        print(f"Total paid: ${total}")
                        # transfer to inventory
                        inventory.extend(cart)
                        cart.clear()
                        print("Items moved to inventory.")
                # if not confirmed, nothing changes
            elif choice == 8:
                shop_options[choice](inventory, items, prices)
            elif choice == 9:
                shop_options[choice](balance, items, prices)
            elif choice == 10:
                shop_options[choice]()
        else:
            print("Invalid choice. Please try again.")
            show_shop_options()


if __name__ == "__main__":
    shop_program()
