import csv
import os
from contact import Contact
from error_handling import (
    get_error_message,
    FileOperationError,
    DuplicateContactError,
    ContactNotFoundError,
    InvalidInputError
)

class ContactManager:
    def __init__(self, file_path='data/contact.csv'):
        self.file_path = file_path
        self.contacts = [] 
        self._ensure_data_directory_exists()

    def _ensure_data_directory_exists(self):
        data_dir = os.path.dirname(self.file_path)
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

    def load_contacts(self):
        self.contacts = [] 
        if not os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Name', 'Phone', 'Email', 'Address']) 
                print("Loading contacts from contacts.csv... Done! (New file created)")
                return
            except Exception as e:
                raise FileOperationError(get_error_message("file_load_error", error=e))

        try:
            with open(self.file_path, 'r', newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        self.contacts.append(Contact.from_dict(row))
                    except ValueError as e:
                        print(f"Warning: Skipping malformed contact in file - {row}. Error: {e}")
            print("Loading contacts from contact.csv... Done!")
        except Exception as e:
            raise FileOperationError(get_error_message("file_load_error", error=e))

    def save_contacts(self):
        try:
            with open(self.file_path, 'w', newline='') as f:
                fieldnames = ['Name', 'Phone', 'Email', 'Address']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows([contact.to_dict() for contact in self.contacts])
        except Exception as e:
            raise FileOperationError(get_error_message("file_save_error", error=e))

    def _is_phone_number_duplicate(self, phone_number):
        return any(contact.phone == phone_number for contact in self.contacts)

    def add_contact(self, name, phone, email, address):
        if self._is_phone_number_duplicate(phone):
            raise DuplicateContactError(get_error_message("duplicate_phone"))
        try:
            new_contact = Contact(name, phone, email, address)
            self.contacts.append(new_contact)
            self.save_contacts() 
        except ValueError as e:
            if "Name cannot be empty" in str(e):
                raise InvalidInputError(get_error_message("invalid_name"))
            elif "Phone number must contain only digits" in str(e):
                raise InvalidInputError(get_error_message("invalid_phone_format"))
            else:
                raise InvalidInputError(str(e)) 

    def view_contacts(self):
        if not self.contacts:
            print("No contacts available.")
            return

        for i, contact in enumerate(self.contacts):
            print(f"\n{i+1}. {contact}") 
            print("-" * 30)

    def search_contact(self, search_term):
        search_term_lower = search_term.lower()
        results = [
            contact for contact in self.contacts
            if search_term_lower in contact.name.lower() or
               search_term_lower in contact.phone.lower() or
               search_term_lower in contact.email.lower()
        ]
        return results

    def remove_contact(self, phone_number):
        original_count = len(self.contacts)
        self.contacts = [contact for contact in self.contacts if contact.phone != phone_number]
        if len(self.contacts) == original_count:
            raise ContactNotFoundError(get_error_message("contact_not_found"))
        self.save_contacts() 