class ContactBookError(Exception):
    pass

class InvalidInputError(ContactBookError):
    pass

class DuplicateContactError(ContactBookError):
    pass

class ContactNotFoundError(ContactBookError):
    pass

class FileOperationError(ContactBookError):
    pass

# Centralized error messages
ERROR_MESSAGES = {
    "invalid_menu_choice": "Invalid choice. Please enter a number from 1 to 5.",
    "invalid_name": "Error: The contact's name must be a non-empty string. Please provide a valid name.",
    "invalid_phone_format": "Error: The phone number must consist only of digits. Please enter a valid phone number.",
    "duplicate_phone": "Error: A contact with this phone number already exists.",
    "empty_search_term": "Search term cannot be empty. Please enter a name, email, or phone number to search.",
    "contact_not_found": "No contact found with the provided details.",
    "unknown_error": "An unexpected error occurred: {error}. Please try again or contact support."
}

def get_error_message(error_code, **kwargs):
    message = ERROR_MESSAGES.get(error_code, ERROR_MESSAGES["unknown_error"]).format(**kwargs)
    return message