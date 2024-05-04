import streamlit as st
from datetime import datetime, timedelta
from streamlit.hashing._CodeHasher import _CodeHasher


class Locker:
    def __init__(self, number, size):
        self.number = number
        self.size = size
        self.available = True
        self.reserved = False
        self.weight = 0
        self.check_in_time = None
        self.check_out_time = None
        self.customer_name = None
        self.duration = None

class LockerRoom:
    def __init__(self, capacity):
        self.capacity = capacity
        self.lockers = [Locker(i, size) for i, size in enumerate(capacity)]

    def check_availability(self):
        available_lockers = [locker.number for locker in self.lockers if locker.available]
        return available_lockers

    def reserve_locker(self, locker_number, name):
        locker = self.lockers[locker_number]
        if not locker.reserved and locker.available:
            locker.reserved = True
            locker.customer_name = name
            return True
        return False

    def check_in(self, locker_number, weight, check_in_time, duration_hours):
        locker = self.lockers[locker_number]
        if locker.reserved and locker.available:
            choice = st.radio("This locker is already reserved. Do you want to extend the reservation?", ("Yes", "No"))
            if choice == "Yes":
                # Extend reservation
                locker.duration += duration_hours
                locker.check_out_time += timedelta(hours=duration_hours)
                return True, "Reservation extended successfully."
            else:
                return False, "Reservation not extended."
        if check_in_time <= datetime.now():
            return False, "Error: Check-in time must be in the future."
        check_out_time = check_in_time + timedelta(hours=duration_hours)
        locker.available = False
        locker.reserved = True
        locker.weight = weight
        locker.check_in_time = check_in_time
        locker.duration = duration_hours  # Store the duration along with the check-in time
        locker.check_out_time = check_out_time
        return True, "Goods pre-booked successfully."

    def check_out(self, locker_number):
        locker = self.lockers[locker_number]
        if not locker.available:
            locker.available = True
            locker.check_out_time = datetime.now()
            locker.customer_name = None
            locker.duration = None
            return True, "Checked out successfully."
        return False, "Error: The locker is already available."

    def space_availability(self):
        available_space = sum(1 for locker in self.lockers if locker.available)
        return available_space

    def total_weight_stored(self):
        total_weight = sum(locker.weight for locker in self.lockers if not locker.available)
        return total_weight

    def calculate_price(self, weight):
        # Example pricing logic: $2 per kg
        return weight * 2

def main():
    locker_capacity = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]  # Example locker room with 3 different sizes of lockers
    locker_room = LockerRoom(locker_capacity)

    st.title("Locker Room Management System")

    state = _CodeHasher('locker-room')  # Creating a session state

    choice = st.sidebar.selectbox("Select an option", ["Check availability", "Reserve a locker", "Check in", "Space availability", "Total weight of goods stored", "Price for goods weight", "Check out"])

    if choice == "Check availability":
        st.write("Available lockers:", locker_room.check_availability())
    elif choice == "Reserve a locker":
        locker_number = st.number_input("Enter locker number to reserve:", min_value=0, max_value=len(locker_room.lockers)-1)
        name = st.text_input("Enter customer name:")
        if st.button("Reserve Locker"):
            if locker_room.reserve_locker(locker_number, name):
                st.success("Locker reserved successfully.")
            else:
                st.error("Unable to reserve locker.")
    elif choice == "Check in":
        locker_number = st.number_input("Enter locker number to check in:", min_value=0, max_value=len(locker_room.lockers)-1)
        weight = st.number_input("Enter weight of goods:")
        check_in_date = st.date_input("Enter check-in date:")
        check_in_time = st.time_input("Enter check-in time:")
        duration_hours = st.number_input("Enter duration in hours:", min_value=1, step=1)
        if st.button("Check In"):
            check_in_datetime = datetime.combine(check_in_date, check_in_time)
            success, message = locker_room.check_in(locker_number, weight, check_in_datetime, duration_hours)
            if success:
                state.locker_number = locker_number  # Store the locker number in session state
                st.success(message)
            else:
                st.error(message)
    elif choice == "Space availability":
        st.write("Available space in locker room:", locker_room.space_availability())
    elif choice == "Total weight of goods stored":
        st.write("Total weight of goods stored:", locker_room.total_weight_stored())
    elif choice == "Price for goods weight":
        weight = st.number_input("Enter weight of goods:")
        price = locker_room.calculate_price(weight)
        st.write("Price for goods weight:", price)
    elif choice == "Check out":
        if hasattr(state, 'locker_number'):  # Check if locker number is stored in session state
            locker_number = state.locker_number
            success, message = locker_room.check_out(locker_number)
            if success:
                st.success(message)
                del state.locker_number  # Remove the stored locker number from session state after checkout
            else:
                st.error(message)
        else:
            st.warning("Please check in first before checking out.")

if __name__ == "__main__":
    main()
