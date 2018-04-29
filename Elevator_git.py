class Elevator: 
    default_max_floor = 11 
    default_min_floor = 0
     
    def __init__(self, max_floor = default_max_floor, 
                min_floor = default_min_floor):
        self.maxFloor = max_floor                                                                                    
        self.minFloor = min_floor

    def get_top_floor(self):
        return self.maxFloor

    def get_bottom_floor(self):
        return self.minFloor

class Car(Elevator):
    default_starting_floor = 0
     
    def __init__(self, max_floor = Elevator.default_max_floor, 
            min_floor = Elevator.default_min_floor, 
            starting_floor = default_starting_floor, name = "Car 0"):
        Elevator.__init__(self, max_floor, min_floor)
        self.startingFloor = starting_floor
        self.currentFloor = self.startingFloor
        self.doorsOpen = False
        self.moving = False
        self.heading = 0
        self.passengerSet = set()
        self.name = name

    def get_floor(self):
        return self.currentFloor

    def get_heading(self):
        if self.heading == 0:
            return "Neutral"
        elif self.heading > 0:
            return "Up"
        else:
            return "Down"

    def get_door_opened_status(self):
        return self.doorsOpen

    def get_name(self):
        return self.name

    def get_passenger_set(self):
        return self.passengerSet

    def get_motion_status(self):
        return self.moving

    def open_doors(self):
        if (self.doorsOpen == False and self.moving == False and 
                int(self.currentFloor)==self.currentFloor):
            self.doorsOpen = True
            print("The doors of "+self.get_name()+" have opened.")
        else:
            print("Cannot open doors at this time.")

    def close_doors(self):
        self.doorsOpen = False
        print("The doors of", self.get_name(), "are now closed.")

    def add_passenger(self, P):
        #if P.isinstance(Passenger):
            self.passengerSet.add(P)
        #else:
        #    print("Invalid; must use a Passenger as parameter")

    def passenger_leave(self, Q):
        if Q in self.passengerSet:
            self.passengerSet.remove(Q)
        else:
            print("Referenced Passenger not found on this Elevator Car")

    def arrive(self, floorNo):
        self.currentFloor = floorNo
        print(self.get_name(), "has arrived on floor", floorNo)
        self.moving = False
        for passen in self.get_passenger_set():
            passen.elevatorPositionSync()
        self.open_doors()

    def goToFloor(self, floorNo):
        if self.get_floor() == floorNo:
            print("""Elevator has quickly reached the floor it was 
                already on.""")
        else:
            if floorNo > self.get_floor():
                self.heading = 1
            if floorNo < self.get_floor():
                self.heading = -1
            if self.get_door_opened_status() == True:
                self.close_doors()
            self.moving = True
            print("Elevator is moving", self.get_heading())
            self.arrive(floorNo)

class Passenger:
    default_entry_floor = 0

    def __init__(self, entry_floor = default_entry_floor, 
            name = "Passenger 0"):
        self.entryFloor = entry_floor
        self.isInElevator = False
        self.currentFloor = self.entryFloor
        self.name = name
        self.elevatorIn = None

    def get_location(self):
        return self.currentFloor

    def get_name(self):
        return self.name

    def board(self, C):
        """Puts this passenger on board Car C"""
        if (C.get_door_opened_status() == True and 
                C.get_floor() == self.get_location()):
            self.isInElevator = True
            C.add_passenger(self)
            self.elevatorIn = C
        else: 
            print("""That elevator car is not on this floor or its 
            doors are not open. It might come if you press a button, 
            or wait if one has already been pressed.""") 

    def disembark(self, C):
        """Takes this passenger off car C"""
        if (C.get_door_opened_status() == True and 
                self.isInElevator == True and 
                self in C.get_passenger_set()):
            self.isInElevator = False
            C.passenger_leave(self)
            self.elevatorIn = None
        else: 
            print("""Passenger cannot leave elevator car. Either the 
            passenger is not on that elevator, or the doors are 
            closed.""") 

    def press_open_button(self, C):
        """Opens the doors on car C"""
        if (self.isInElevator == True and self in C.get_passenger_set()):
            C.open_doors()

    def press_close_button(self, C):
        """Closes the doors on car C"""
        if (self.isInElevator == True and self in C.get_passenger_set()):
            C.close_doors()

    def elevatorPositionSync(self):
        if self.isInElevator == False:
            print("The Passenger known as", self.get_name(), "is not in an elevator.")
        else:
            self.currentFloor = self.elevatorIn.get_floor()        

def get_available_buttons(n, top, bottom):
    """Returns the avaialable buttons on floor n"""
    if n == bottom:
        return {"Up"}
    elif n == top:
        return {"Down"}
    elif ((bottom < n) and (n < top)):
        return {"Up","Down"}

def setup_top_floor():
    floorString = input("""Please enter the number of the building's 
        highest floor: """)
    floors = int(floorString)
    if float(floorString) != floors:
        print("""J.M. is more comfortable with a whole number of 
            floors. Top floor set to """+floors)
    if floors < 0:
        print("An underground building? I can work with that...")
    if floors == 0:
        print("""This building isn't very tall. I wonder whether you 
            are putting in a parking elevator...""")
    if floors == 1:
        print("""If you are following the convention of calling the 
            ground floor 1, rather than the convention of calling it 0, 
            this building probably won't need an above-ground elevator. 
            An elevator could go below ground too, though... """)
    return floors

def start_Building():
    floors = setup_top_floor()
    baseFloor = int(input("Enter the floor number of the lowest floor: "))
    if baseFloor > floors:
        print("The bottom floor can't be above the top floor!")
        print("Resetting startup...")
        return(start_Building())
    if baseFloor == floors:
        print("The elevator won't do much if there's only one floor!")
    if baseFloor > 1:
        print("A tower in the sky? Okay, cool!")
    startFloor = int(input("""Please enter a floor for the main elevator 
        car to start on: """))
    if ((startFloor > floors) or (startFloor < baseFloor)):
        startFloor = int(input("Try entering a start floor one more time."))
        if ((startFloor > floors) or (startFloor < baseFloor)):
            print("The elevator car can't start outside the shaft!")
            print("Resetting startup...")
            return(start_Building()) 
    return Car(floors, baseFloor, startFloor)

def start_Passenger():
    passengerStart = int(input("""Enter a floor for the first 
        Passenger, Passenger 0, to start on: """))
    return Passenger(passengerStart)           

def control_passenger_execution_loop(P, usableCar):
    running = True
    #if P.isinstance(Passenger) == False:
    #    running = False
    #    print("Invalid input for passenger to control")
    if running == True:
        print("You are now controlling", P.get_name())
    print("This passenger is on floor", P.get_location())
    carName = usableCar.get_name()
    while running == True:
        if P.isInElevator == False:
            print("As a reminder, you are on floor", P.get_location())
            buttonOptions = get_available_buttons(P.get_location(), 
                    usableCar.get_top_floor(), usableCar.get_bottom_floor())
            print("Available buttons are", buttonOptions)
            if "Up" in buttonOptions: 
                print("Press 1 to press up button")
            if "Down" in buttonOptions:
                print("Press 2 to print down button")
            if (usableCar.get_floor() == P.get_location() and 
                    usableCar.get_door_opened_status() == True):
                print("Press 3 to get in", carName)
            print("Press 0 to quit program")
            print("\n")
            userInput = int(input("Make selection: "))
            if userInput == 1 or userInput ==2:
                usableCar.goToFloor(P.get_location())
            elif userInput == 3:
                P.board(usableCar)
                print("You have boarded the elevator")
            elif userInput == 0:
                running = 0
            else: 
                print("Invalid selection.")
        if (P.isInElevator == True and 
                usableCar.get_motion_status() == False):
            print("You are in the elevator.")
            print("Available floors are", usableCar.get_bottom_floor(), 
                    "through", usableCar.get_top_floor())
            print("Type a floor number to push the button for that floor.")
            print('Or, type "other" for door open/close buttons or to get off.')
            print("\n")
            userElevatorInput = input("Make your selection: ")
            if userElevatorInput == "other":
                print("press 1 to disembark the elevator.")
                print("press 2 to press the door close button.")
                print("press 3 to press the door open button.")
                print("\n")
                userChoice = int(input("Make your selection: "))
                if userChoice == 1:
                    P.disembark(usableCar)
                elif userChoice == 2:
                    usableCar.close_doors()
                    print("You are still inside the elevator on floor", usableCar.get_floor())
                elif userChoice == 3:
                    usableCar.open_doors()
                    print("You are still inside the elevator on floor", usableCar.get_floor())
                else:
                    print("Invalid input")
            else:
                floorInput = int(userElevatorInput)
                usableCar.goToFloor(floorInput)

                

def main():
    print("Welcome to the Elevator program!")
    Car0 = start_Building()
    Passenger0 = start_Passenger()
    if ( (Passenger0.get_location() > Car0.get_top_floor()) or 
            (Passenger0.get_location() < Car0.get_bottom_floor()) ):
        print("Passenger start floor out of bounds. Try again.")
        Passenger0 = start_Passenger()
        if ( (Passenger0.get_location() > Car0.get_top_floor()) or 
                (Passenger0.get_location() < Car0.get_bottom_floor()) ):
            print("Setting passenger on bottom floor.")
            Passenger0 = Passenger(Car0.get_bottom_floor)
    control_passenger_execution_loop(Passenger0, Car0)
    
    
if __name__ == "__main__":
    main()