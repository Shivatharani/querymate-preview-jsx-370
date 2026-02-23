import uuid # To generate unique booking IDs
import datetime # For booking timestamps

class TicketBookingSystem:
    def __init__(self):
        self.events = {}  # Stores event details: {event_id: {'name': '...', 'date': '...', 'total_tickets': 100, 'available_tickets': 100, 'price': 25.00}}
        self.bookings = {} # Stores booking details: {booking_id: {'user_id': '...', 'event_id': '...', 'num_tickets': 2, 'total_price': 50.00, 'timestamp': '...'}}
        self.users = {}   # Stores simple user info: {user_id: {'username': '...', 'email': '...'}}

    def create_event(self, name, date, total_tickets, price):
        event_id = str(uuid.uuid4())
        self.events[event_id] = {
            'name': name,
            'date': date,
            'total_tickets': total_tickets,
            'available_tickets': total_tickets, # Initially all tickets are available
            'price': price
        }
        print(f"Event '{name}' created with ID: {event_id}")
        return event_id

    def register_user(self, username, email):
        user_id = str(uuid.uuid4())
        self.users[user_id] = {
            'username': username,
            'email': email
        }
        print(f"User '{username}' registered with ID: {user_id}")
        return user_id

    def list_events(self):
        if not self.events:
            print("No events available.")
            return

        print("\n--- Available Events ---")
        for event_id, event_info in self.events.items():
            print(f"Event ID: {event_id}")
            print(f"  Name: {event_info['name']}")
            print(f"  Date: {event_info['date']}")
            print(f"  Available Tickets: {event_info['available_tickets']}/{event_info['total_tickets']}")
            print(f"  Price per Ticket: ${event_info['price']:.2f}")
            print("-" * 30)

    def book_tickets(self, user_id, event_id, num_tickets):
        if user_id not in self.users:
            print("Error: Invalid user ID.")
            return None
        if event_id not in self.events:
            print("Error: Invalid event ID.")
            return None

        event = self.events[event_id]

        if num_tickets <= 0:
            print("Error: Number of tickets must be positive.")
            return None

        if event['available_tickets'] < num_tickets:
            print(f"Error: Not enough tickets available for '{event['name']}'. Only {event['available_tickets']} remaining.")
            return None

        # Simulate payment (in a real app, this would involve a payment gateway)
        total_price = num_tickets * event['price']
        print(f"\nProcessing payment of ${total_price:.2f} for {num_tickets} tickets to '{event['name']}'...")
        # In a real app, integrate with Stripe/PayPal here.
        # For this example, we'll assume payment is successful.
        print("Payment successful (simulated)!")

        # Update available tickets
        event['available_tickets'] -= num_tickets

        # Record the booking
        booking_id = str(uuid.uuid4())
        self.bookings[booking_id] = {
            'user_id': user_id,
            'event_id': event_id,
            'num_tickets': num_tickets,
            'total_price': total_price,
            'timestamp': datetime.datetime.now().isoformat()
        }

        print(f"Success! Booked {num_tickets} tickets for '{event['name']}'.")
        print(f"Booking ID: {booking_id}")
        return booking_id

    def get_user_bookings(self, user_id):
        user_bookings = []
        for booking_id, booking_info in self.bookings.items():
            if booking_info['user_id'] == user_id:
                event_name = self.events[booking_info['event_id']]['name']
                user_bookings.append({
                    'booking_id': booking_id,
                    'event_name': event_name,
                    'num_tickets': booking_info['num_tickets'],
                    'total_price': booking_info['total_price'],
                    'timestamp': booking_info['timestamp']
                })
        return user_bookings

# --- Demonstration ---
if __name__ == "__main__":
    app = TicketBookingSystem()

    # 1. Register Users
    user1_id = app.register_user("Alice", "alice@example.com")
    user2_id = app.register_user("Bob", "bob@example.com")

    # 2. Create Events
    event1_id = app.create_event("Concert A", "2026-03-15", 100, 50.00)
    event2_id = app.create_event("Comedy Show", "2026-03-20", 50, 25.00)
    event3_id = app.create_event("Sports Match", "2026-03-22", 200, 75.00)

    # 3. List Events
    app.list_events()

    # 4. Book Tickets
    print("\n--- Alice booking tickets ---")
    app.book_tickets(user1_id, event1_id, 2) # Alice books 2 tickets for Concert A
    app.book_tickets(user1_id, event2_id, 1) # Alice books 1 ticket for Comedy Show
    app.book_tickets(user1_id, event1_id, 99) # Alice tries to book more than available for Concert A (should fail)
    app.book_tickets(user1_id, event1_id, 98) # Alice books remaining tickets for Concert A

    print("\n--- Bob booking tickets ---")
    app.book_tickets(user2_id, event2_id, 3) # Bob books 3 tickets for Comedy Show
    app.book_tickets(user2_id, event3_id, 5) # Bob books 5 tickets for Sports Match
    app.book_tickets(user2_id, "non_existent_event", 1) # Bob tries to book a non-existent event

    # 5. List Events again to see updated availability
    app.list_events()

    # 6. View User's Bookings
    print(f"\n--- Bookings for {app.users[user1_id]['username']} ---")
    alice_bookings = app.get_user_bookings(user1_id)
    if alice_bookings:
        for booking in alice_bookings:
            print(f"  Booking ID: {booking['booking_id']}")
            print(f"  Event: {booking['event_name']}")
            print(f"  Tickets: {booking['num_tickets']}")
            print(f"  Total Price: ${booking['total_price']:.2f}")
            print(f"  Timestamp: {booking['timestamp']}")
            print("-" * 20)
    else:
        print("  No bookings found.")

    print(f"\n--- Bookings for {app.users[user2_id]['username']} ---")
    bob_bookings = app.get_user_bookings(user2_id)
    if bob_bookings:
        for booking in bob_bookings:
            print(f"  Booking ID: {booking['booking_id']}")
            print(f"  Event: {booking['event_name']}")
            print(f"  Tickets: {booking['num_tickets']}")
            print(f"  Total Price: ${booking['total_price']:.2f}")
            print(f"  Timestamp: {booking['timestamp']}")
            print("-" * 20)
    else:
        print("  No bookings found.")