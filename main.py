def load_users():
    users = []
    try:
        with open("users.txt", "r") as file:
            for line in file:
                name, username, password, role = line.strip().split(",")
                users.append({
                    "name": name,
                    "username": username,
                    "password": password,
                    "role": role
                })
    except  FileNotFoundError:
        print("No users.txt file found. Creating a new one.")
        open("users.txt", "w")
    return users


def login():
    users = load_users()
    print("=== Login ===")
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    for user in users:
        if user["username"] == username and user["password"] == password:
            print(f"Welcome, {user['name']}! Role: {user['role'].capitalize()}")
            return user

    print(" Incorrect username or password.")
    return None

def register():
    print("--- User Registration ---")

    full_name = input("Full name: ")
    username = input("Username: ")
    password = input("Password: ")

    print("Available roles: customer, manager, cashier, chef")
    role = input("Role: ").strip().lower()

    if role not in ['customer', 'manager', 'cashier', 'chef']:
        print(" Invalid role. Registration failed.")
        return

    try:
        with open("users.txt", "r") as file:
            for line in file:
                _, existing_username, _, _ = line.strip().split(",")
                if username == existing_username:
                    print(" Username already exists.")
                    return
    except FileNotFoundError:
        pass

    with open("users.txt", "a") as file:
        file.write(f"{full_name},{username},{password},{role}\n")

    print("Registration successful.")


# Customer

def customer_menu(user):
    print("--- Customer Menu ---")
    print("1. View Menu")
    print("2. Manage Cart")
    print("3. Track Orders")
    print("4. Provide feedback")
    print("5. Update Personal Information")
    print("6. Logout")

    choice = input("Make and option: ")

    if choice == "1":
        food_menu(user)
    elif choice == "2":
        manage_cart(user)
    elif choice == "3":
        track_order(user)
    elif choice == "4":
        give_feedback(user)
    elif choice == "5":
        update_info(user)
    elif choice == "6":
        main()
    else:
        print("Invalid choice!")
        customer_menu(user)


def food_menu(user):
    menu = {
        "1": ("Sandwich", 7),
        "2": ("Salads", 7),
        "3": ("Fried noodle", 7),
        "4": ("Pasta", 10),
        "5": ("French fries", 9),
        "6": ("Burger", 11),
        "7": ("Pizza", 12),
        "8": ("Fried rice", 7),
        "9": ("Orange juice", 8),
        "10": ("Watermelon juice", 5),
        "11": ("Coke", 5),
        "12": ("Sprite", 7),
        "13": ("Ice lemon tea", 6),
        "14": ("Coffee", 7),
        "15": ("Plain water", 1)
    }

    print("=== Here is the Menu ===")
    for key in menu:
        print(f"{key}. {menu[key][0]} - RM{menu[key][1]}")
    print("0. Exit")
    print("=== Please make your choice ===")

    username = user["username"]
    choices = input("Enter your choices (comma-separated): ").split(",")

    if len(choices) == 1 and choices[0].strip() == "0":
        print("Exiting menu. Goodbye!")
        customer_menu(user)

    found = False
    for choice in choices:
        choice = choice.strip()

        if choice in menu:
            item_name, item_price = menu[choice]
            with open("cart.txt", "a") as file:
                file.write(f"{username},{item_name},RM{item_price}\n")
            print(f"{item_name} - RM{item_price}")
            found = True
        else:
            print(f"Invalid menu choice: {choice}")

    if found:
        print("Items added to cart.")
        manage_cart(user)
    else:
        print("No valid items added.")
        retry = input("Do you want to try again? (y/n): ").strip().lower()
        if retry == 'y':
            food_menu(user)
        else:
            customer_menu(menu)


def manage_cart(user):
    print("\n=== Manage Cart ===")
    print("1. Add More Items")
    print("2. Delete Item")
    print("3. Place Order")
    choice = input("Enter your choice: ").strip()

    if choice == "1":
        food_menu(user)

    elif choice == "2":
        delete_from_cart(user)

    elif choice == "3":
        place_order(user)

    else:
        print("Invalid option.")

    customer_menu(user)


def delete_from_cart(user):
    username = user["username"]
    print("\n=== Your Cart ===")

    with open("cart.txt", "r") as file:
        lines = file.readlines()

    user_cart = []
    other_cart = []

    for line in lines:
        parts = line.strip().split(",")
        if len(parts) != 3:
            continue
        line_username, item_name, item_price = parts
        if line_username == username:
            user_cart.append((line_username, item_name, item_price))
        else:
            other_cart.append(line)

    if not user_cart:
        print("No items in your cart.")
        return

    for idx, (_, item_name, item_price) in enumerate(user_cart, 1):
        print(f"{idx}. {item_name} ({item_price})")

    try:
        input_str = input("Enter the numbers of the items to remove (comma or space separated, e.g., 1 3 5): ")
        selected_indices = set()

        for part in input_str.replace(",", " ").split():
            if part.isdigit():
                index = int(part)
                if 1 <= index <= len(user_cart):
                    selected_indices.add(index - 1)
                else:
                    print(f"Skipping invalid item number: {index}")
            else:
                print(f"Ignoring invalid input: '{part}'")

        if not selected_indices:
            print("No valid items selected.")
            return

        user_cart = [item for i, item in enumerate(user_cart) if i not in selected_indices]

    except Exception as e:
        print(f"Error: {e}")
        return

    updated_lines = other_cart + [
        f"{username},{item_name},{item_price}\n" for (username, item_name, item_price) in user_cart
    ]

    with open("cart.txt", "w") as file:
        file.writelines(updated_lines)

    print("Selected item(s) removed from cart.")
    manage_cart(user)



def place_order(user):
    username = user["username"]

    with open("cart.txt", "r") as file:
        lines = file.readlines()

    user_orders = []
    remaining_cart = []

    for line in lines:
        parts = line.strip().split(",")
        if len(parts) != 3:
            continue
        line_username, item_name, item_price = parts
        if line_username == username:
            user_orders.append(line)
        else:
            remaining_cart.append(line)

    if not user_orders:
        print("No items to place order.")
        return

    with open("orders.txt", "a") as orders_file:
        orders_file.writelines(user_orders)

    with open("cart.txt", "w") as cart_file:
        cart_file.writelines(remaining_cart)

    print("Order placed successfully!")
    customer_menu(user)


def track_order(user):
    username = user["username"]
    print(f"Orders for {username}")
    try:
        with open("orders.txt") as file:
            found = False
            for line in file:
                parts = line.strip().split(",")
                if len(parts) != 3:
                    continue
                line_username, item_name, item_price = parts
                if line_username == username:
                    print(f"- {item_name} ({item_price})")
                    found = True
            if not found:
                print("No orders found")
    except FileNotFoundError:
        print("No orders in history")

    customer_menu(user)

def give_feedback(user):
    username = user["username"]
    feedback = input("Enter your feedback: ")
    with open("feedback.txt", "w") as file:
        file.write(f"{username} : {feedback}")

    customer_menu(user)

def update_info(user):
    with open("users.txt", "r") as f:
        lines = f.readlines()

    updated_lines = []
    found = False

    for line in lines:
        name, username, password, role = line.strip().split(",")
        if name.strip().lower() == user["name"].strip().lower() and role == "customer":
            found = True
            print(f"Current username: {username}")
            print(f"Current password: {password}")
            new_username = input("Enter new username (or press Enter to keep current): ").strip()
            new_password = input("Enter new password (or press Enter to keep current): ").strip()
            if new_username == "":
                new_username = username
            if new_password == "":
                new_password = password
            updated_line = f"{name},{new_username},{new_password},{role}\n"
        else:
            updated_line = line
        updated_lines.append(updated_line)

    if found:
        with open("users.txt", "w") as f:
            f.writelines(updated_lines)
        print("Account updated successfully.")
    else:
        print("No matching customer found.")

    customer_menu(user)




# Manager

def manager_menu(user):
    print("--- Manager Menu ---")
    print("1. Financial Overview")
    print("2. View Orders")
    print("3. View Customer Feedback")
    print("4. Manage User")
    print("5. Inventory Control")
    print("6. Logout")

    choice = input("Please select an option: ")

    if choice == "1":
        financial_management(user)
    elif choice == "2":
        view_orders(user)
    elif choice == "3":
        view_feedback(user)
    elif choice == "4":
        manage_user(user)
    elif choice == "5":
        inventory_control(user)
    elif choice == "6":
        main()
    else:
        print("Invalid choice!")

    manager_menu(user)

def financial_management(user):
    print("\n--- Financial Management ---")
    print("1. Track income (customer order)")
    print("2. Add expense")
    print("3. View financial summary")
    print("4. Back to manager menu")

    choice = input("Choose an option (1-4): ")

    if choice == "1":
        get_income(user)
    elif choice == "2":
        add_expense(user)
    elif choice == "3":
        view_summary(user)
    elif choice == "4":
        manager_menu(user)
    else:
        print("Invalid choice. Try again.")
        financial_management(user)


def get_income(user):
    total_income = 0.0

    with open("receipts.txt", "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("Total: RM"):
                parts = line.split("RM")
                if len(parts) == 2:
                    amount_str = parts[1].strip()
                    amount = float(amount_str)
                    total_income += amount

    with open("income.txt", "w") as f:
        f.write(f"Total income from receipts: RM{total_income:.2f}\n")

    print(f"Total income: RM{total_income:.2f}")

    financial_management(user)


def add_expense(user):
    expense_item = input("Enter expense description (e.g., Rent, Ingredients): ")
    try:
        amount = float(input("Enter amount spent (RM): "))

        with open("expenses.txt", "a") as file:
            file.write(f"{expense_item},{amount}\n")

        print(f"Recorded expense: {expense_item}, Amount = RM{amount:.2f}")
    except ValueError:
        print("Error: Please enter a valid number.")

    financial_management(user)


def view_summary(user):
    total_income = 0.0
    total_expenses = 0.0

    with open("income.txt", "r") as income_file:
        for line in income_file:
            line = line.strip()
            if line.startswith("Total income from receipts: RM"):
                amount_str = line.split("RM")[1].strip()
                total_income = float(amount_str)
                break

    with open("expenses.txt", "r") as expense_file:
        for line in expense_file:
            parts = line.strip().split(",")
            if len(parts) == 2:
                try:
                    total_expenses += float(parts[-1])
                except ValueError:
                    continue

    profit = total_income - total_expenses

    print("\n--- Financial Summary ---")
    print(f"Total Income: RM{total_income:.2f}")
    print(f"Total Expenses: RM{total_expenses:.2f}")
    print(f"Net Profit: RM{profit:.2f}")

    financial_management(user)


def view_orders(user):
    print("--- All Orders ---")
    with open("orders.txt", "r") as file:
        lines = [line.strip() for line in file if line.strip()]
    if lines:
        for line in lines:
            print(line)
    else:
        print("No orders found.")

    manager_menu(user)


def view_feedback(user):
    print("--- Customer Feedback ---")
    with open("feedback.txt", "r") as file:
        lines = [line.strip() for line in file if line.strip()]
    if lines:
        for line in lines:
            print(line)
    else:
        print("No feedback found.")

    manager_menu(user)



def manage_user(user):
    while True:
        print("\n--- User Management ---")
        print("1. View all users")
        print("2. Delete a user")
        print("3. Back to manager menu")
        choice = input("Choose an option: ")

        if choice == "1":
            with open("users.txt") as file:
                print("\nRegistered Users:")
                for line in file:
                    print(line.strip())

        elif choice == "2":
            username_to_delete = input("Enter the username to delete: ").strip()

            if username_to_delete == user["username"]:
                print("You cannot delete yourself.")
                continue

            with open("users.txt", "r") as file:
                lines = file.readlines()

            user_found = False
            updated_users = []

            for line in lines:
                parts = line.strip().split(",")
                if len(parts) != 4:
                    continue
                fullname, username, password, role = parts
                if username != username_to_delete:
                    updated_users.append(f"{fullname},{username},{password},{role}")
                else:
                    user_found = True

            if user_found:
                with open("users.txt", "w") as file:
                    for user_line in updated_users:
                        file.write(user_line + "\n")
                print(f"User '{username_to_delete}' has been deleted.")
            else:
                print("User not found.")

        elif choice == "3":
            print("Returning to manager menu...")
            manager_menu(user)

        else:
            print("Invalid choice. Please try again.")

        manage_user(user)

def inventory_control(user):
    while True:
        print("\n--- Inventory Control ---")
        print("1. View inventory")
        print("2. Add new item")
        print("3. Update item")
        print("4. Delete item")
        print("5. Back to menu")
        choice = input("Choose an option: ")

        if choice == "1":
            with open("inventory.txt", "r") as file:
                lines = file.readlines()
                if lines:
                    for line in file:
                        print("\nInventory List:")
                        print(line.strip())
                else:
                    print("No inventory found!")

        elif choice == "2":
            name = input("Enter item name: ").strip()
            item_type = input("Enter type (product/ingredient): ").strip().lower()
            quantity = input("Enter quantity: ").strip()

            with open("inventory.txt", "a") as file:
                file.write(f"{name},{item_type},{quantity}\n")
            print("Item added successfully.")

        elif choice == "3":
            name = input("Enter the name of item to update: ").strip()
            updated_lines = []
            found = False

            with open("inventory.txt", "r") as file:
                lines = file.readlines()

            for line in lines:
                parts = line.strip().split(",")
                if len(parts) != 3:
                    continue
                item_name, item_type, quantity = parts
                if item_name == name:
                    print(f"Current: {line.strip()}")
                    new_quantity = input("Enter new quantity: ").strip()
                    updated_lines.append(f"{item_name},{item_type},{new_quantity}\n")
                    found = True
                else:
                    updated_lines.append(line)

            if found:
                with open("inventory.txt", "w") as file:
                    file.writelines(updated_lines)
                print("Item updated.")
            else:
                print("Item not found.")

        elif choice == "4":
            name = input("Enter the name of item to delete: ").strip()
            updated_lines = []
            found = False

            with open("inventory.txt", "r") as file:
                lines = file.readlines()

            for line in lines:
                parts = line.strip().split(",")
                if len(parts) != 3:
                    continue
                item_name = parts[0]
                if item_name.lower() != name.lower():
                    updated_lines.append(line)
                else:
                    found = True

            if found:
                with open("inventory.txt", "w") as file:
                    file.writelines(updated_lines)
                print("Item deleted.")
            else:
                print("Item not found.")

        elif choice == "5":
            manager_menu(user)

        else:
            print("Invalid choice. Try again.")


# Cashier

def cashier_menu(user):
    print("--- Cashier Menu ---")
    print("1. View Products")
    print("2. Manage Discounts")
    print("3. Generate Receipt")
    print("4. Generate Sales Report")
    print("5. Logout")

    choice = input("Please select an option: ")

    if choice == "1":
        view_products(user)
    elif choice == "2":
        manage_discount(user)
    elif choice == "3":
        generate_receipt(user)
    elif choice == "4":
        generate_sales_report(user)
    elif choice == "5":
        main()
    else:
        print("Invalid choice.")

    cashier_menu(user)

def view_products(user):
    products = {
        "1": ("Sandwich", 7),
        "2": ("Salads", 7),
        "3": ("Fried noodle", 7),
        "4": ("Pasta", 10),
        "5": ("French fries", 9),
        "6": ("Burger", 11),
        "7": ("Pizza", 12),
        "8": ("Fried rice", 7),
        "9": ("Orange juice", 8),
        "10": ("Watermelon juice", 5),
        "11": ("Coke", 5),
        "12": ("Sprite", 7),
        "13": ("Ice lemon tea", 6),
        "14": ("Coffee", 7),
        "15": ("Plain water", 1)
    }

    print("\n--- Product List ---")
    for key, (name, price) in products.items():
        print(f"{key}. {name} - RM {price:.2f}")

    cashier_menu(user)

def manage_discount(user):
    while True:
        print("\n--- Discount Manager ---")
        print("1. View Discounts")
        print("2. Add Discount")
        print("3. Modify Discount")
        print("4. Delete Discount")
        print("5. Back to Menu")

        choice = input("Choose an option (1-5): ")

        if choice == "1":
            print("\n--- Current Discounts ---")
            with open("discount.txt", "r") as file:
                discounts = file.readlines()
                if discounts:
                    for idx, line in enumerate(discounts, start=1):
                        print(f"{idx}. {line.strip()}")
                else:
                    print("No discounts found.")

        elif choice == "2":
            item = input("Enter item name: ")
            discount = input("Enter discount: ")
            with open("discount.txt", "a") as file:
                file.write(f"{item} - {discount}%\n")
            print("Discount added.")

        elif choice == "3":
            with open("discount.txt", "r") as file:
                discounts = file.readlines()
            if not discounts:
                print("No discounts to modify.")
                continue

            print("\n--- Discounts ---")

            for idx, line in enumerate(discounts, start=1):
                print(f"{idx}. {line.strip()}")

            mod_index = input("Enter the number of the discount to modify: ")
            if mod_index.isdigit():
                mod_index = int(mod_index)
                if 1 <= mod_index <= len(discounts):
                    current_line = discounts[mod_index - 1].strip()
                    item_name, previous_discount = current_line.split(" - ")
                    new_discount = input(f"Enter new discount for '{item_name}': ")
                    discounts[mod_index - 1] = f"{item_name} - {new_discount}%\n"
                    with open("discount.txt", "w") as file:
                        file.writelines(discounts)
                    print("Discount updated.")
                else:
                    print("Invalid number.")
            else:
                print("Please enter a valid number.")

        elif choice == "4":
            with open("discount.txt", "r") as file:
                discounts = file.readlines()

            if not discounts:
                print("No discounts to delete.")
                continue

            print("\n--- Discounts ---")
            for idx, line in enumerate(discounts, start=1):
                print(f"{idx}. {line.strip()}")

            del_index = input("Enter the number of the discount to delete: ")
            if del_index.isdigit():
                del_index = int(del_index)
                if 1 <= del_index <= len(discounts):
                    removed = discounts.pop(del_index - 1)
                    with open("discount.txt", "w") as file:
                        file.writelines(discounts)
                    print(f"Deleted: {removed.strip()}")
                else:
                    print("Invalid number.")
            else:
                print("Please enter a valid number.")

        elif choice == "5":
            cashier_menu(user)

        else:
            print("Invalid choice. Please select 1 to 5.")




def generate_receipt(user):
    username = input("Enter customer username: ").strip()
    date = input("Enter receipt date (e.g. 2025-06-13): ").strip()

    receipt_lines = []
    subtotal = 0
    total_discount = 0

    discount_dict = {}
    with open("discount.txt", "r") as file:
        for line in file:
            if "-" in line:
                parts = line.strip().split(" - ")
                if len(parts) == 2:
                    item_name = parts[0].strip().lower()
                    discount_percent = float(parts[1].replace("%", "").strip())
                    discount_dict[item_name] = discount_percent

    with open("orders.txt", "r") as file:
        all_orders = file.readlines()

    user_orders = []
    remaining_orders = []
    for line in all_orders:
        parts = line.strip().split(",")
        if len(parts) != 3:
            continue
        order_username, item_name, item_price = parts
        if order_username.strip() == username:
            user_orders.append((item_name.strip(), item_price.strip()))
        else:
            remaining_orders.append(line.strip())

    if not user_orders:
        print("No orders found for this user.")
        return

    receipt_lines.append("=== Restaurant Receipt ===")
    receipt_lines.append(f"Date: {date}")
    receipt_lines.append(f"Customer: {username}")
    receipt_lines.append("--------------------------")

    for item_name, item_price in user_orders:
        item_name_lower = item_name.lower()
        price = float(item_price.replace("RM", "").strip())
        discount_percent = discount_dict.get(item_name_lower, 0)

        if discount_percent > 0:
            discount_amount = price * (discount_percent / 100)
            final_price = price - discount_amount
            receipt_lines.append(f"{item_name} - RM {price:.2f} (-{discount_percent:.0f}% -> RM {final_price:.2f})")
            total_discount += discount_amount
            subtotal += price
        else:
            receipt_lines.append(f"{item_name} - RM {price:.2f}")
            subtotal += price

    total = subtotal - total_discount

    receipt_lines.append("--------------------------")
    receipt_lines.append(f"Subtotal: RM {subtotal:.2f}")
    if total_discount > 0:
        receipt_lines.append(f"Discounts Applied: -RM {total_discount:.2f}")
    receipt_lines.append(f"Total: RM {total:.2f}")
    receipt_lines.append("==========================")

    for line in receipt_lines:
        print(line)

    with open("receipts.txt", "a") as receipt_file:
        for line in receipt_lines:
            receipt_file.write(line + "\n")
        receipt_file.write("\n")

    with open("orders.txt", "w") as file:
        for order_line in remaining_orders:
            file.write(order_line + "\n")

    cashier_menu(user)




def generate_sales_report(user):
    total_sales = 0
    item_count = {}

    with open("receipts.txt", "r") as file:
        for line in file:
            line = line.strip()

            if line.startswith("Total: RM"):
                price_str = line.replace("Total: RM", "").strip()
                total_sales += float(price_str)

            elif " - RM" in line and not line.startswith("Subtotal"):
                item_name = line.split(" - RM")[0].strip()
                item_count[item_name] = item_count.get(item_name, 0) + 1

    print("\n Sales Report ")
    print(f"Total Sales: RM {total_sales:.2f}")

    if item_count:
        print("\nItem Sales Count:")
        for item, count in item_count.items():
            print(f"- {item}: {count} sold")

        max_count = max(item_count.values())
        popular_items = [item for item, count in item_count.items() if count == max_count]

        if len(popular_items) == 1:
            print(f"\nMost Popular Item: {popular_items[0]} ({max_count} sold)")
        else:
            items_str = ", ".join(popular_items)
            print(f"\nMost Popular Items (tied): {items_str} ({max_count} each)")
    else:
        print("No items sold yet.")

    cashier_menu(user)


# Chef

def chef_menu(user):
    print("--- Chef Menu ---")
    print("1. Manage Recipes")
    print("2. Equipment Management")
    print("3. View Inventory")
    print("4. Logout")

    choice = input("Please select an option: ")

    if choice == "1":
        manage_recipes(user)
    elif choice == "2":
        equipment_management(user)
    elif choice == "3":
        check_inventory(user)
    elif choice == "4":
        main()
    else:
        print("Invalid choice.")

    chef_menu(user)

def manage_recipes(user):
    while True:
        print("\n--- Recipe Manager ---")
        print("1. View Recipes")
        print("2. Add Recipe")
        print("3. Delete a Recipe")
        print("4. Back to Menu")

        choice = input("Choose an option (1-4): ")

        if choice == "1":
            print("\n--- Recipes List ---")
            with open("recipes.txt", "r") as file:
                recipes = file.readlines()
                if recipes:
                    for idx, recipe in enumerate(recipes, start=1):
                        print(f"{idx}. {recipe.strip()}")
                else:
                    print("No recipes found.")

        elif choice == "2":
            new_recipe = input("Enter the new recipe: ")
            with open("recipes.txt", "a") as file:
                file.write(new_recipe.strip() + "\n")
            print("New recipe added.")

        elif choice == "3":
            with open("recipes.txt", "r") as file:
                recipes = file.readlines()

            if not recipes:
                print("No recipes to delete.")
                continue

            print("\n--- Recipes ---")
            for idx, recipe in enumerate(recipes, start=1):
                print(f"{idx}. {recipe.strip()}")

            delete_index = input("Enter the number of the recipe to delete: ")
            if delete_index.isdigit():
                delete_index = int(delete_index)
                if 1 <= delete_index <= len(recipes):
                    removed = recipes.pop(delete_index - 1)
                    with open("recipes.txt", "w") as file:
                        file.writelines(recipes)
                    print(f"Deleted: {removed.strip()}")
                else:
                    print("Invalid number.")
            else:
                print("Please enter a valid number.")

        elif choice == "4":
            chef_menu(user)
            break
        else:
            print("Invalid choice.")




def equipment_management(user):
    while True:
        print("\n--- Equipment Management ---")
        print("1. View reported equipment issues")
        print("2. Report a new issue")
        print("3. Delete reported issue")
        print("4. Back to menu")
        choice = input("Choose an option: ")

        if choice == "1":
            with open("equipment_report.txt", "r") as file:
                lines = file.readlines()

            if lines:
                print("\nReported Equipment Issues:")
                for line in lines:
                    print(line.strip())
            else:
                print("No equipment reports found.")


        elif choice == "2":
            equipment_name = input("Enter equipment name: ").strip()
            issue_description = input("Describe the issue or maintenance need: ").strip()
            reporter = user.get("username")

            with open("equipment_report.txt", "a") as file:
                file.write(f"{equipment_name} - {issue_description} (Reported by: {reporter})\n")
            print("Issue reported successfully.")

        elif choice == "3":
            with open("equipment_report.txt", "r") as file:
                reports = file.readlines()

            if not reports:
                print("No reports to delete.")
            else:
                print("\nReported Equipment Issues:")
                for i, report in enumerate(reports, start=1):
                    print(f"{i}. {report.strip()}")

                to_delete = input("Enter the number of the report to delete (or 'c' to cancel): ").strip()
                if to_delete.lower() == 'c':
                    print("Deletion cancelled.")
                elif not to_delete.isdigit():
                    print("Invalid input. Please enter a number.")
                else:
                    index = int(to_delete)
                    if index < 1 or index > len(reports):
                        print("Invalid number.")
                    else:
                        deleted_report = reports.pop(index - 1)
                        with open("equipment_report.txt", "w") as file:
                            file.writelines(reports)
                        print(f"Deleted: {deleted_report.strip()}")

        elif choice == "4":
            print("Returning to menu...")
            chef_menu(user)

        else:
            print("Invalid choice. Try again.")
            equipment_management(user)

def check_inventory(user):
    with open("inventory.txt", "r") as file:
        lines = [line.strip() for line in file if line.strip()]

    if lines:
        print("\nInventory List:")
        for idx, line in enumerate(lines, 1):
            print(f"{idx}. {line}")
    else:
        print("No inventory found!")

    chef_menu(user)


# Main menu
def main():
    print("=== Welcome to Restaurant System ===")

    while True:
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            user = login()
            if user:
                role = user["role"]
                if role == "manager":
                    manager_menu(user)
                elif role == "customer":
                    customer_menu(user)
                elif role == "cashier":
                    cashier_menu(user)
                elif role == "chef":
                    chef_menu(user)
                else:
                    print(" Unknown role!")
        elif choice == "2":
            register()
        elif choice == "3":
            exit()
        else:
            print("Invalid choice.")




if __name__ == "__main__":
    main()
