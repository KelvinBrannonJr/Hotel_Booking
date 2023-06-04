import pandas as pd

# Read csv and use 'dtype' to convert csv number values to actual strings
df = pd.read_csv('hotels.csv', dtype={"id": str})
df_card = pd.read_csv('cards.csv', dtype=str).to_dict(orient="records")


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


# Reservation Confirmation class
class ReservationConfirmation:
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel_name = hotel_object

    def generate(self):
        content = f"""
        Thank you for your reservation!
        Here is your confirmation details:
        Name: {self.customer_name}
        Hotel name: {self.hotel_name.name}
        """
        return content


class CreditCard:
    def __init__(self, number):
        self.number = number

    def validate(self, expiration, holder, cvc):
        card_data = {"number": self.number, "expiration": expiration, "holder": holder, "cvc": cvc}

        if card_data in df_card:
            return True
        else:
            return False


if __name__ == "__main__":
    print(df)
    hotel_ID = input("Enter an id of the hotel you want to book: ")
    hotel = Hotel(hotel_ID)

    if hotel.available():
        credit_card = CreditCard(number="12345612345612")
        if credit_card.validate(expiration="12/26", holder="JOHN SMITH", cvc="123"):
            hotel.book()
            name = input("Enter your name: ")
            confirm = ReservationConfirmation(customer_name=name, hotel_object=hotel)
            print(confirm.generate())
        else:
            print("There was a problem with your payment..")

    else:
        print("Sorry hotel is not free")
