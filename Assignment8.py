# ------------------------------------------------------------------------ #
# Title: Assignment 08
# Description: Working with classes

# ChangeLog (Who,When,What):
# RRoot,1.1.2030,Created started script
# RRoot,1.1.2030,Added pseudo-code to start assignment 8
# cmhas,1.2.2030,Modified code to complete assignment 8
# ------------------------------------------------------------------------ #

# Data -------------------------------------------------------------------- #
file_name = 'products.txt'
product_list = []
menu = """
Please select an option:
 1) Show Current Product List
 2) Add Product to List
 3) Remove Product from List
 4) Edit Product Entry
 5) Save and Quit
"""
user_choice = int()

################################################################################
############################ Exception Classes #################################
################################################################################

class Error(Exception):
    """Base class for custom exceptions"""
    pass

class InputError(Error):
    """Raise when user input is invalid or unexpected"""
    pass

class RangeError(InputError):
    """Raise when user menu choice is outside possible range"""
    pass

class ProdExistsError(InputError):
    """Raise when user attempts to add a new product which is already on the list"""

class PriceFormatError(InputError):
    """Raise when user enters a price that doesn't meet the nitpicky requirement being enforced"""
    pass

class BadSaveError(Error):
    """Raise when error-checking the saved file results in an inproperly formatted entry"""
    # Really shouldn't ever be raised, but you never know...
    pass

################################################################################

class Product:
    """Store data about a product:

    properties:
        product_name: (string) with the products's  name
        product_price: (float) with the products's standard price
    methods:
    changelog: (When,Who,What)
        RRoot,1.1.2030,Created Class
        cmhas,1.2.2030,Modified code to complete assignment 8
    """
    def __init__(self, name, price):
        self.product_name = name
        self.product_price = price
    
    def display(self):
        print(self.product_name, self.product_price, sep=': ')
    
    def edit(self):
        print('What about the entry do you want to edit?')
        print('(Please enter "name", "price" or "both")')
        while True:
            tmp_choice = input('> ').strip().lower()
            if tmp_choice in ['name','n','both','b']:
                print('Please enter a new name for {0}'.format(self.product_name))
                tmp = input('> ')
                self.product_name = tmp
                if tmp_choice == 'name' or tmp_choice == 'n':
                    break
            if tmp_choice in ['price','p','both','b']:
                print('Please enter a new price for {0}'.format(self.product_name))
                tmp = input('> ')
                while True:
                    try:
                        tmp = IO.check_format(tmp)
                        break
                    except PriceFormatError:
                        print('The price must be a number written in decimal form,')
                        print('with at most two digits after the decimal, and with')
                        print('a leading zero (for prices less than a dollar)')
                        print('')
                        print('Please enter the price of {0}'.format(tmp_name))
                        tmp = input('> ').strip()
                self.product_price = tmp
                break
            print('Please enter "name", "price" or "both"')
    
    # Should add property stuff, but not really needed...

# Data -------------------------------------------------------------------- #

# Processing  ------------------------------------------------------------- #
class FileProcessor:
    """Process data to and from a file and a list of product objects:

    methods:
        save_data_to_file(file_name, list_of_product_objects):

        read_data_from_file(file_name): -> (a list of product objects)

    changelog: (When,Who,What)
        RRoot,1.1.2030,Created Class
        cmhas,1.2.2030,Modified code to complete assignment 8
    """
    def save_data_to_file(name, list):
        """Save contents of product list to file"""
        file = open(name,'w')
        for entry in list:
            file.write(entry.product_name + ',' + entry.product_price + '\n')
        file.close()
    
    def read_data_from_file(name, is_error_checking):
        """Open file "name", read it and return product list"""
        tmp_list = []
        tmp_name = ''
        tmp_price = ''
        try:
            file = open(name,'r')
            split_line = []
            for line in file:
                try:
                    split_line = line.strip().split(',')
                    if len(split_line) == 2:
                        tmp_name = split_line[0]
                        tmp_price = split_line[1]
                        try:
                            tmp_price = IO.check_format(tmp_price)
                            tmp_list.append(Product(tmp_name,tmp_price))
                        except PriceFormatError:
                            raise Error
                        finally:
                            tmp_name = ''
                            tmp_price = ''
                            split_line = []
                    else:
                        raise Error
                except Error:
                    if is_error_checking:
                        file.close()
                        raise BadSaveError
                    else:
                        print('Current line in file is not properly formatted.')
                        print('Do you want to continue to the next line?')
                        print('(Note: responding with "no" will exit the program)')
                        if not IO.yes_no_choice():
                            raise SystemExit
            file.close()
            return tmp_list
        except FileNotFoundError:
            if is_error_checking:
                raise
            else:
                print('The file {0} was not opened successfully.'.format(name))
                print('If it is not supposed to exist, this is not a problem')
                print('Do you want to proceed with an empty list?')
                if IO.yes_no_choice():
                    return []
                else:
                    raise SystemExit

# Processing  ------------------------------------------------------------- #

# Presentation (Input/Output)  -------------------------------------------- #
class IO:
    """Perform various Input/Output tasks"""
    @staticmethod
    def menu_choice(max):
        """Take a choice from user and return as integer"""
        while True:
            tmp = input().strip()
            try:
                tmp = int(tmp)
                if tmp < 1 or tmp > max:
                    raise RangeError
                return tmp
            except ValueError:
                print('Please enter a number')
                print('')
                return 0
            except RangeError:
                print('Please enter a number between 1 and {0}'.format(max))
                print('')
                return 0
    
    def yes_no_choice():
        """Take user input ("yes" or "no") and return as boolean"""
        while True:
            tmp = input('> ').strip().lower()
            if tmp == 'yes' or tmp == 'y':
                return True
            elif tmp == 'no' or tmp == 'n':
                return False
            else:
                print('Please enter "yes" or "no"')
    
    @staticmethod
    def show_menu():
        """Print the menu of user options"""
        print(menu)
    
    @staticmethod
    def show_list(list):
        """Print the current product list"""
        if len(list) == 0:
            print('(The product list is currently empty)')
        else:
            print('The current product list (product: price) is:')
            print('')
            for entry in list:
                entry.display()
    
    @staticmethod
    def add_new_product():
        """Request user enter new product's name and price; then add new entry to list"""
        print('Please enter the name of the new product to add')
        tmp_name = input('> ').strip()
        for entry in product_list:
            if tmp_name == entry.product_name:
                print(entry.product_name, 'is already on the list')
                print('Do you want to edit the entry for {0}?'.format(entry.product_name))
                if IO.yes_no_choice():
                    entry.edit()
                else:
                    raise ProdExistsError()
        print('Please enter the price of {0}'.format(tmp_name))
        tmp_price = input('> ').strip()
        while True:
            try:
                tmp_price = IO.check_format(tmp_price)
                break
            except PriceFormatError:
                print('The price must be a number written in decimal form,')
                print('with at most two digits after the decimal, and with')
                print('a leading zero (for prices less than a dollar)')
                print('')
                print('Please enter the price of {0}'.format(tmp_name))
                tmp_price = input('> ').strip()
        product_list.append(Product(tmp_name, tmp_price))
    
    @staticmethod
    def edit_product():
        """Change the name or listed price of a given product"""
        print('Please enter the name of the product to edit')
        tmp_name = input('> ').strip()
        for entry in product_list:
            if entry.product_name == tmp_name:
                entry.edit()
                break
        else:
            print('That product does not appear to be on the list')
            print('Remember: product names are case-sensitive')
            print('')
    
    @staticmethod
    def del_product():
        """Remove an entry from the product list"""
        print('Please enter the name of the product to remove')
        tmp = input('> ').strip()
        for entry in product_list:
            if entry.product_name == tmp:
                print('Are you sure you want to delete product {0} with price {1}?'.format(entry.product_name, entry.product_price))
                if IO.yes_no_choice():
                    tmp = entry.product_name
                    product_list.remove(entry)
                    print(tmp, 'has been deleted')
                    print('')
                else:
                    print(entry.product_name, 'has not been deleted')
                    print('')
                break
        else:
            print('That product does not appear to be on the list')
            print('Remember: product names are case-sensitive')
            print('')
    
    @staticmethod
    def check_format(price):
        """Check formating of a price and return properly formatted string if possible."""
        tmp_split_price = price.split('.')
        if len(tmp_split_price) < 3:
            for i in tmp_split_price:
                if i.isdecimal() == False:
                    raise PriceFormatError
            if len(tmp_split_price) == 1:
                price = price + '.00'
            else:
                if len(tmp_split_price[1]) == 1:
                    price = price + '0'
                elif len(tmp_split_price[1]) > 2:
                    raise PriceFormatError
        return price

# Presentation (Input/Output)  -------------------------------------------- #

# Main Body of Script  ---------------------------------------------------- #

# Open the saved file and read in the product list.
# This also gives the user to choice to let a SystemExit
# exception be raised if the file is not opened.
product_list = FileProcessor.read_data_from_file(file_name, False) 

while True:
    IO.show_menu()
    user_choice = IO.menu_choice(5)
    # Show current list
    if user_choice == 1:
        IO.show_list(product_list)
    # Add to list
    elif user_choice == 2:
        try:
            IO.add_new_product()
        except ProdExistsError:
            continue
    # remove from list
    elif user_choice == 3:
        IO.del_product()
    # edit entry
    elif user_choice == 4:
        IO.edit_product()
    # save and quit
    elif user_choice == 5:
        print('Are you sure?')
        if IO.yes_no_choice():
            try:
                FileProcessor.save_data_to_file(file_name, product_list)
                err_check = []
                err_check = FileProcessor.read_data_from_file(file_name, True)
                if len(product_list) != len(err_check):
                    raise Error
                for i in range(len(product_list)):
                    if product_list[i].product_name != err_check[i].product_name:
                        raise Error
                    if product_list[i].product_price != err_check[i].product_price:
                        raise Error
                print('Save Successful')
                print('Are you sure you want to quit?')
                if IO.yes_no_choice():
                    break
            except FileNotFoundError:
                print('Saving was unsuccessful')
                print('No output file appears to have been created')
                print('')
                continue
            except BadSaveError:
                print('Saving was unsuccessful')
                print('The output file appears to have been incorrectly formatted')
            except Error:
                print('Saving was unsuccessful')
                print('What would you like to do?')
                print(' 1) Quit anyway')
                print(' 2) Display what was saved')
                print(' 3) Return to main menu')
                user_choice = IO.menu_choice(3)
                if user_choice == 1:
                    print('Are you sure you want to quit?')
                    if IO.yes_no_choice():
                        break
                    else:
                        err_check.clear()
                        continue
                elif user_choice == 2:
                    IO.show_list(err_check)
                    print('What would you like to do?')
                    print(' 1) Accept what was saved and quit')
                    print(' 2) Return to main menu')
                    user_choice = IO.menu_choice(2)
                    if user_choice == 1:
                        print('Are you sure you want to quit?')
                        if IO.yes_no_choice():
                            break
                        else:
                            err_check.clear()
                            continue
                    else:
                        err_check.clear()
                        continue
                else:
                    err_check.clear()
                    continue

# Main Body of Script  ---------------------------------------------------- #

