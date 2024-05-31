import random
import string

from authentication.models import Person

def generate_tempno(medical, profile_id):
    temp_no = "Something Wrong"
    try:
    
        first_letter = medical[0].upper() if len(medical) != "" or None else 'X'
        
        # Get the second letter of the medicalname (if available, otherwise use a placeholder)
        second_letter = medical[1].upper() if len(medical) > 1 else 'Y'
        
        last_letter = medical[-1].upper() if len(medical) > 1 else 'Z'
        
        # Get the user ID
        medical_id = profile_id
        
        # Generate a random 2-digit number
        random_number = ''.join(random.choices(string.digits, k=2))
        
        # Construct the temporary number
        temp_no = f"{first_letter}0{medical_id}0{second_letter}R0{random_number}0{last_letter}"
    
        return temp_no
    except Exception as e:
        return temp_no

def RegisterUserTempNo(user):
    
    temp_no = "Something Wrong"
    
    try:
        # Get the first two letters of the username
        first_two_letters = user.username[:2].upper()
        
        # Get the last two letters of the username
        last_two_letters = user.username[-2:].upper()
        
        # Get the user ID
        user_id = user.id
        
        # Get the user join date (formatted as YYYYMMDD)
        join_date = user.date_joined.strftime('%Y%m%d')
        
        # Construct the temporary number
        temp_no = f"{first_two_letters}-{user_id}-L{last_two_letters}-D{join_date}"
        
        return temp_no
    except Exception as e:
        return temp_no
