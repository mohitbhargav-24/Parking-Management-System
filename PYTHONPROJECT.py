import math

# Configuration Constants
TOTAL_SLOTS = 5
RATES = {
    "car": 20,   # Rs. 20 per hour
    "bike": 10   # Rs. 10 per hour
}
FILE_NAME = "parking.txt"


def save_to_file(slots):
    """Saves the current state of parking slots to parking.txt."""
    with open(FILE_NAME, "w") as f:
        for i, slot in enumerate(slots, start=1):
            if slot is None:
                f.write(f"Slot {i}: Free\n")
            else:
                f.write(f"Slot {i}: {slot['reg_no']} | Type: {slot['type']}\n")


def calculate_fee(vehicle_type, hours):
    """
    Calculates parking fee based on vehicle type and hours.
    - Hours are rounded up (ceiling).
    - Minimum charge duration is 1 hour.
    """
    # Round up hours and ensure minimum of 1 hour
    billed_hours = max(1, math.ceil(hours))
    rate = RATES.get(vehicle_type.lower(), 0)
    total_fee = billed_hours * rate
    return billed_hours, total_fee


def vehicle_entry(slots):
    """Handles vehicle entry (Menu Option 1)."""
    # Check if lot is full
    if all(slot is not None for slot in slots):
        print("Parking lot is full!")
        return

    reg_no = input("Enter vehicle number: ").strip()

    # Check if vehicle is already parked
    for slot in slots:
        if slot and slot["reg_no"] == reg_no:
            print(f"Vehicle {reg_no} is already parked.")
            return

    v_type = input("Enter vehicle type (car/bike): ").strip().lower()

    # Validate vehicle type
    if v_type not in RATES:
        print("Invalid type. Enter car or bike.")
        return

    # Find the first available (free) slot
    for i in range(len(slots)):
        if slots[i] is None:
            slots[i] = {"reg_no": reg_no, "type": v_type}
            free_slots = sum(1 for s in slots if s is None)
            print(f"Vehicle {reg_no} parked in slot {i + 1}.")
            print(f"Slots free: {free_slots}")
            save_to_file(slots)
            break


def vehicle_exit(slots):
    """Handles vehicle exit (Menu Option 2)."""
    reg_no = input("Enter vehicle number: ").strip()

    # Find the slot with the matching vehicle
    found_index = -1
    for i, slot in enumerate(slots):
        if slot and slot["reg_no"] == reg_no:
            found_index = i
            break

    if found_index == -1:
        print(f"Vehicle {reg_no} not found.")
        return

    try:
        hours = float(input("Enter hours parked: "))
    except ValueError:
        print("Invalid hours input.")
        return

    parked_vehicle = slots[found_index]
    billed_hours, fee = calculate_fee(parked_vehicle["type"], hours)

    # Free the slot
    slots[found_index] = None

    print(f"Hours charged: {billed_hours} (rounded up) | Fee: {fee}")
    print(f"Slot {found_index + 1} is now free.")

    save_to_file(slots)


def display_status(slots):
    """Displays the current status of all parking slots (Menu Option 3)."""
    free_count = sum(1 for s in slots if s is None)
    print(f"Slots free: {free_count} of {TOTAL_SLOTS}")


def main():
    # Initialize 5 slots as None (empty)
    slots = [None] * TOTAL_SLOTS
    save_to_file(slots)  # Create initial file state

    while True:
        print("\n--- Parking Management System ---")
        print("1. Entry")
        print("2. Exit")
        print("3. Status")
        print("4. Exit Program")

        choice = input("Select an option (1-4): ").strip()

        if choice == "1":
            vehicle_entry(slots)
        elif choice == "2":
            vehicle_exit(slots)
        elif choice == "3":
            display_status(slots)
        elif choice == "4":
            print("Exiting system.")
            break
        else:
            print("Invalid choice! Please select 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()