from datetime import datetime, timedelta

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
       
    def check_in(self, locker_number, weight, check_in_time, duration_hours):
        locker = self.lockers[locker_number]
        if locker.reserved and locker.available:
            choice = input("This locker is already reserved. Do you want to extend the reservation? (yes/no): ")
            if choice == "yes":
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
        locker.reserved = False
        locker.weight = weight
        locker.check_in_time = check_in_time
        locker.duration = duration_hours  # Store the duration along with the check-in time
        locker.check_out_time = check_out_time
        return True, "Goods pre-booked successfully."
        return False
    

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

if __name__ == "__main__":
    locker_capacity = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]  # Example locker room with 3 different sizes of lockers
    locker_room = LockerRoom(locker_capacity)

    while True:
        print("\nLocker Room Management System")
        print("1. Check availability")
        print("2. Reserve a locker")
        print("3. Check in (show time and date)")
        print("4. Space availability")
        print("5. Total weight of goods stored")
        print("6. Price for goods weight")
        print("7. Check out")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            print("Available lockers:", locker_room.check_availability())
        elif choice == "2":
            locker_number = int(input("Enter locker number to reserve: "))
            name = input("Enter customer name: ")
            if locker_room.reserve_locker(locker_number, name):
                print("Locker reserved successfully.")
            else:
                print("Unable to reserve locker.")
        elif choice == "3":
            locker_number = int(input("Enter locker number to check in: "))
            weight = float(input("Enter weight of goods: "))
            check_in_date = input("Enter check-in date (YYYY-MM-DD): ")
            check_in_time = input("Enter check-in time (HH:MM): ")
            duration_hours = int(input("Enter duration in hours: "))
            
            try:
                check_in_datetime = datetime.strptime(check_in_date + " " + check_in_time, "%Y-%m-%d %H:%M")
                success, message = locker_room.check_in(locker_number, weight, check_in_datetime, duration_hours)
                if success:
                    print(message)
                else:
                    print(message)
            except ValueError:
                print("Invalid date or time format. Please enter in the format YYYY-MM-DD HH:MM.")
        elif choice == "4":
            print("Available space in locker room:", locker_room.space_availability())
        elif choice == "5":
            print("Total weight of goods stored:", locker_room.total_weight_stored())
        elif choice == "6":
            weight = float(input("Enter weight of goods: "))
            price = locker_room.calculate_price(weight)
            print("Price for goods weight:", price)
        elif choice == "7":
            locker_number = int(input("Enter locker number to check out: "))
            success, message = locker_room.check_out(locker_number)
            if success:
                print(message)
            else:
                print(message)
        elif choice == "8":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")