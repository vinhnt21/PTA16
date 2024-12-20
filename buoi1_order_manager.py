orders = []


def add_order(product, quantity, price):
    orders.append([product, quantity, price])


def remove_order(index):
    orders.pop(index)


def update_order(index, product, quantity, price):
    orders[index] = [product, quantity, price]


def show_order():
    for order in orders:
        print(order)


def total_price():
    total = 0
    for order in orders:
        total += order[1] * order[2]
    print("Dạ của đại ka là: ", total)


while True:
    print(
        """1. Add order
2. Remove order
3. Update order
4. Show order
5. Show total price
0. Exit
=================="""
    )

    choice = int(input("Enter your choice: "))

    if choice == 1:
        # Add order
        print("Enter order information:")
        product = input("Product: ")
        quantity = int(input("Quantity: "))
        price = float(input("Price: "))
        add_order(product, quantity, price)
    elif choice == 2:
        # Remove order
        show_order()
        print("Enter order index to remove:")
        index = int(input())
        if 1 <= index <= len(orders):
            remove_order(index - 1)
        else:
            print("Invalid index")
    elif choice == 3:
        # Update order
        print("Enter order information:")
        show_order()
        index = int(input("Enter order index to update: "))
        if 1 <= index <= len(orders):
            product = input("Product: ")
            quantity = int(input("Quantity: "))
            price = float(input("Price: "))
            update_order(index - 1, product, quantity, price)
        else:
            print("Invalid index")
    elif choice == 4:
        # Show order
        show_order()
    elif choice == 5:
        total_price()
    elif choice == 0:
        break
    else:
        print("Invalid choice")
