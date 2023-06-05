import pandas as pd

# Read csv and use 'dtype' to convert csv number values to actual strings
df = pd.read_csv('hotels.csv', dtype={"id": str})
df_card = pd.read_csv('cards.csv', dtype=str).to_dict(orient="records")
df_secure_card = pd.read_csv('card_security.csv', dtype=str)


# Hotel class
class Hotel:
    def __init__(self, local_hotel_id):
        self.local_hotel_id = local_hotel_id
        self.name = df.loc[df['id'] == self.local_hotel_id, 'name'].squeeze()

    # Use row of dataframe column 'id' to assign value of 'no' to availability
    def book(self):
        df.loc[df['id'] == self.local_hotel_id, 'available'] = "no"
        # write to change availability in csv file
        df.to_csv("hotels.csv", index=False)

    # Check if status in dataframe 'available' column is yes or no
    def available(self):
        availability = df.loc[df['id'] == self.local_hotel_id, 'available'].squeeze()
        if availability == "yes":
            return True

        else:
            return False


# Spa package class
class Spa(Hotel):
    def book_spa_package(self):
        pass


# Hotel Reservation Confirmation class
class ReservationConfirmation:
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel_name = hotel_object

    # Generate message after hotel is booked
    def generate(self):
        content = f"""
        Thank you for your reservation!
        Here is your confirmation details:
        Name: {self.customer_name}
        Hotel name: {self.hotel_name.name}
        """
        return content


# Spa package confirmation
class SpaReservationConfirmation:
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel_name = hotel_object

    # Generate message when bonus Spa package is accepted
    def generate(self):
        content = f"""
        Thank you for your SPA reservation!
        Here is your SPA confirmation details:
        Name: {self.customer_name}
        Hotel name: {self.hotel_name.name}
        """
        return content


# Credit card class
class CreditCard:
    # Card number constructed when object is instantiated
    def __init__(self, number):
        self.number = number

    # Validate if card info is match from cards.csv
    def validate(self, expiration, holder, cvc):
        card_data = {"number": self.number, "expiration": expiration, "holder": holder, "cvc": cvc}

        # Conditional for user input card data compared to dataframe data
        if card_data in df_card:
            return True
        else:
            return False


# SecureCreditCard class is a child class inheriting from CreditCard
class SecureCreditCard(CreditCard):
    def authenticate(self, given_password):
        password = df_secure_card.loc[df_secure_card["number"] == self.number, "password"].squeeze()
        if password == given_password:
            return True
        else:
            return False


if __name__ == "__main__":
    print(df)
    hotel_ID = input("Enter an id of the hotel you want to book: ")
    hotel = Hotel(hotel_ID)

    if hotel.available():
        credit_card = SecureCreditCard(number="1234567890123456")
        if credit_card.validate(expiration="12/26", holder="JOHN SMITH", cvc="123"):
            if credit_card.authenticate(given_password="mypass"):
                hotel.book()
                name = input("Enter your name: ")
                confirm = ReservationConfirmation(customer_name=name, hotel_object=hotel)
                print(confirm.generate())
                book_spa = input("Would you like to book a spa package? Yes or No: ")
                if book_spa == "Yes":
                    spa = Spa(hotel_ID)
                    spa.book_spa_package()
                    confirm_spa = SpaReservationConfirmation(customer_name=name, hotel_object=hotel)
                    print(confirm_spa.generate())
                else:
                    print("Ok no spa today, maybe next visit.")

            else:
                print("Credit card authentication failed.")
        else:
            print("There was a problem with your payment..")
    else:
        print("Sorry hotel is not free")
