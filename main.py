import pandas as pd

# Read csv and use 'dtype' to convert csv number values to actual strings
df = pd.read_csv('hotels.csv', dtype={"id": str})


# Hotel class
class Hotel:
    def __init__(self, local_hotel_id):
        self.local_hotel_id = local_hotel_id

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
        pass

    def generate(self):
        pass


if __name__ == "__main__":
    print(df)
    hotel_id = input("Enter an id of the hotel you want to book: ")
    hotel = Hotel(hotel_id)
    if hotel.available():
        hotel.book()
        name = input("Enter your name: ")
        confirm = ReservationConfirmation(name, hotel)
        print(confirm.generate())

    else:
        print("Sorry hotel is not free")
