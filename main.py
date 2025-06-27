from contact_manager import ContactManager
from error_handling import (
    get_error_message,
    InvalidInputError,
    DuplicateContactError,
    ContactNotFoundError,
    FileOperationError,
    ContactBookError
)

def display_menu():
    print("\n" + "=" * 20 + " MENU " + "=" * 20)
    print("1. Add Contact")
    print("2. View Contacts")
    print("3. Search Contact")
    print("4. Remove Contact")
    print("5. Exit")
    print("=" * 46)

def main():
    contact_manager = ContactManager()

    print("Welcome to the Contact Book CLI System!")
    try:
        contact_manager.load_contacts()
    except FileOperationError as e:
        print(e)
    while True:
        display_menu()
        choice = input("Enter your choice: ").strip()

        try:
            if choice == '1':
                print("\n===== Add Contact =====")
                name = input("Enter Name: ").strip()
                phone = input("Enter Phone Number: ").strip()
                email = input("Enter Email: ").strip()
                address = input("Enter Address: ").strip()
                contact_manager.add_contact(name, phone, email, address)
                print("Contact added successfully!")
            elif choice == '2':
                print("\n===== All Contacts =====")
                contact_manager.view_contacts()
            elif choice == '3':
                print("\n===== Search Contact =====")
                search_term = input("Enter search term (name/email/phone): ").strip()
                if not search_term:
                    raise InvalidInputError(get_error_message("empty_search_term"))
                results = contact_manager.search_contact(search_term)
                if results:
                    print("\nSearch Result:")
                    for i, contact in enumerate(results):
                        print(f"{i+1}. {contact}")
                        print("-" * 30)
                else:
                    print(get_error_message("contact_not_found"))
            elif choice == '4':
                print("\n===== Remove Contact =====")
                phone_to_delete = input("Enter the phone number of the contact to delete: ").strip()
                if not phone_to_delete.isdigit():
                    raise InvalidInputError(get_error_message("invalid_phone_format"))
                contact_exists = any(c.phone == phone_to_delete for c in contact_manager.contacts)
                if not contact_exists:
                    raise ContactNotFoundError(get_error_message("contact_not_found"))

                confirm = input(f"Are you sure you want to delete contact with phone number {phone_to_delete}? (y/n): ").lower()
                if confirm == 'y':
                    contact_manager.remove_contact(phone_to_delete)
                    print("Contact deleted successfully!")
                else:
                    print("Contact deletion cancelled.")
            elif choice == '5':
                print("Thank you for using the Contact Book CLI System. Goodbye!")
                break
            else:
                print(get_error_message("invalid_menu_choice"))

        except InvalidInputError as e:
            print(e)
        except DuplicateContactError as e:
            print(e)
        except ContactNotFoundError as e:
            print(e)
        except FileOperationError as e:
            print(e)
        except ContactBookError as e: 
            print(get_error_message("unknown_error", error=e))
        except Exception as e: 
            print(get_error_message("unknown_error", error=e))

if __name__ == "__main__":
    main()