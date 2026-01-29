#!/usr/bin/env python3
"""
SalonPro Manager - CLI Application
Main entry point for the salon management system.
"""

from database import init_db, get_session
from models import Client, Stylist, Service, Appointment
from datetime import datetime, date, timedelta
import sys


class SalonProCLI:
    def __init__(self):
        """Initialize the CLI application."""
        self.session = init_db()
        print("\n" + "="*60)
        print("       WELCOME TO SALONPRO MANAGER")
        print("="*60)
        print("Your complete salon management solution")
        print("="*60)

    def display_main_menu(self):
        """Display the main menu options."""
        print("\n📋 MAIN MENU")
        print("-" * 40)
        print("1.  Client Management")
        print("2.  Stylist Management")
        print("3.  Service Management")
        print("4.  Appointment Management")
        print("5.  View Reports & Analytics")
        print("6.  Search & Find")
        print("0.  Exit Program")
        print("-" * 40)

    def client_management_menu(self):
        """Display client management menu."""
        print("\n👥 CLIENT MANAGEMENT")
        print("-" * 40)
        print("1.  View All Clients")
        print("2.  Add New Client")
        print("3.  Find Client by ID")
        print("4.  Find Client by Name")
        print("5.  Find Client by Phone")
        print("6.  Update Client Information")
        print("7.  View Client's Appointment History")
        print("8.  Delete Client")
        print("9.  Back to Main Menu")
        print("-" * 40)

    def stylist_management_menu(self):
        """Display stylist management menu."""
        print("\n💇 STYLIST MANAGEMENT")
        print("-" * 40)
        print("1.  View All Stylists")
        print("2.  Add New Stylist")
        print("3.  Find Stylist by ID")
        print("4.  Find Stylist by Specialty")
        print("5.  View Stylist's Schedule")
        print("6.  Update Stylist Information")
        print("7.  View Stylist's Clients")
        print("8.  Deactivate Stylist")
        print("9.  Back to Main Menu")
        print("-" * 40)

    def service_management_menu(self):
        """Display service management menu."""
        print("\n✂️ SERVICE MANAGEMENT")
        print("-" * 40)
        print("1.  View All Services")
        print("2.  View Service Menu (Active Only)")
        print("3.  Add New Service")
        print("4.  Find Service by ID")
        print("5.  Find Service by Category")
        print("6.  Update Service Information")
        print("7.  View Service Popularity")
        print("8.  Deactivate Service")
        print("9.  Back to Main Menu")
        print("-" * 40)

    def appointment_management_menu(self):
        """Display appointment management menu."""
        print("\n📅 APPOINTMENT MANAGEMENT")
        print("-" * 40)
        print("1.  View All Appointments")
        print("2.  View Today's Appointments")
        print("3.  View Upcoming Appointments")
        print("4.  Schedule New Appointment")
        print("5.  Find Appointment by ID")
        print("6.  Find Appointments by Date")
        print("7.  Find Appointments by Client")
        print("8.  Find Appointments by Stylist")
        print("9.  Update Appointment Status")
        print("10. Cancel Appointment")
        print("11. Delete Appointment")
        print("12. Back to Main Menu")
        print("-" * 40)

    def search_menu(self):
        """Display search menu."""
        print("\n🔍 SEARCH & FIND")
        print("-" * 40)
        print("1.  Search Clients")
        print("2.  Search Appointments by Date Range")
        print("3.  Search Revenue by Date")
        print("4.  Back to Main Menu")
        print("-" * 40)

    def run(self):
        """Main loop to run the CLI application."""
        while True:
            self.display_main_menu()
            choice = input("\nEnter your choice (0-6): ").strip()

            if choice == "0":
                self.exit_program()
            elif choice == "1":
                self.handle_client_management()
            elif choice == "2":
                self.handle_stylist_management()
            elif choice == "3":
                self.handle_service_management()
            elif choice == "4":
                self.handle_appointment_management()
            elif choice == "5":
                self.handle_reports()
            elif choice == "6":
                self.handle_search()
            else:
                print("❌ Invalid choice. Please enter a number between 0-6.")

    # ========== CLIENT MANAGEMENT METHODS ==========

    def handle_client_management(self):
        """Handle client management operations."""
        while True:
            self.client_management_menu()
            choice = input("\nEnter your choice (1-9): ").strip()

            if choice == "9":
                break
            elif choice == "1":
                self.view_all_clients()
            elif choice == "2":
                self.add_new_client()
            elif choice == "3":
                self.find_client_by_id()
            elif choice == "4":
                self.find_client_by_name()
            elif choice == "5":
                self.find_client_by_phone()
            elif choice == "6":
                self.update_client()
            elif choice == "7":
                self.view_client_appointments()
            elif choice == "8":
                self.delete_client()
            else:
                print("❌ Invalid choice. Please enter a number between 1-9.")

    def view_all_clients(self):
        """Display all clients."""
        clients = Client.get_all(self.session)
        if not clients:
            print("\n📭 No clients found.")
            return

        print(f"\n👥 ALL CLIENTS ({len(clients)} total)")
        print("-" * 70)
        print(f"{'ID':<5} {'Name':<25} {'Phone':<15} {'Email':<25}")
        print("-" * 70)

        for client in clients:
            print(f"{client.id:<5} {client.full_name:<25} {client.formatted_phone:<15} {client.email or 'N/A':<25}")

    def add_new_client(self):
        """Add a new client to the database."""
        print("\n➕ ADD NEW CLIENT")
        print("-" * 40)

        try:
            first_name = input("First Name: ").strip()
            last_name = input("Last Name: ").strip()
            phone = input("Phone Number: ").strip()
            email = input("Email (optional): ").strip() or None
            notes = input("Notes (optional): ").strip() or None

            if not first_name or not last_name or not phone:
                print("❌ First name, last name, and phone are required.")
                return

            # Check if phone already exists
            existing = Client.find_by_phone(self.session, phone)
            if existing:
                print(f"❌ Phone number already registered to {existing.full_name}")
                return

            client = Client.create(
                session=self.session,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                email=email,
                notes=notes
            )

            print(f"\n✅ Client added successfully!")
            print(f"   Name: {client.full_name}")
            print(f"   ID: {client.id}")

        except Exception as e:
            print(f"❌ Error adding client: {e}")

    def find_client_by_id(self):
        """Find a client by their ID."""
        try:
            client_id = int(input("\nEnter Client ID: ").strip())
            client = Client.find_by_id(self.session, client_id)

            if client:
                self.display_client_details(client)
            else:
                print(f"❌ No client found with ID {client_id}")
        except ValueError:
            print("❌ Please enter a valid number.")

    def find_client_by_name(self):
        """Find clients by name (partial match)."""
        name = input("\nEnter client name (or part): ").strip()
        if not name:
            print("❌ Please enter a name to search.")
            return

        clients = Client.find_by_name(self.session, name)

        if not clients:
            print(f"❌ No clients found matching '{name}'")
            return

        print(f"\n🔍 FOUND {len(clients)} CLIENT(S)")
        print("-" * 70)
        for client in clients:
            print(f"ID: {client.id} | Name: {client.full_name} | Phone: {client.formatted_phone}")

    def find_client_by_phone(self):
        """Find a client by phone number."""
        phone = input("\nEnter phone number: ").strip()
        if not phone:
            print("❌ Please enter a phone number.")
            return

        client = Client.find_by_phone(self.session, phone)

        if client:
            self.display_client_details(client)
        else:
            print(f"❌ No client found with phone {phone}")

    def display_client_details(self, client):
        """Display detailed information about a client."""
        print(f"\n📄 CLIENT DETAILS")
        print("-" * 40)
        print(f"ID: {client.id}")
        print(f"Name: {client.full_name}")
        print(f"Phone: {client.formatted_phone}")
        print(f"Email: {client.email or 'Not provided'}")
        print(f"Email Valid: {'Yes' if client.email_is_valid else 'No'}")
        print(f"Notes: {client.notes or 'None'}")
        print(f"Created: {client.created_at.strftime('%Y-%m-%d')}")

        # Show appointment count
        appointments = client.get_appointments(self.session)
        print(f"Total Appointments: {len(appointments)}")

    def update_client(self):
        """Update client information."""
        try:
            client_id = int(input("\nEnter Client ID to update: ").strip())
            client = Client.find_by_id(self.session, client_id)

            if not client:
                print(f"❌ No client found with ID {client_id}")
                return

            self.display_client_details(client)
            print("\n📝 UPDATE CLIENT (leave blank to keep current value)")
            print("-" * 40)

            updates = {}

            new_first = input(f"First Name [{client.first_name}]: ").strip()
            if new_first:
                updates['first_name'] = new_first

            new_last = input(f"Last Name [{client.last_name}]: ").strip()
            if new_last:
                updates['last_name'] = new_last

            new_phone = input(f"Phone [{client.phone}]: ").strip()
            if new_phone and new_phone != client.phone:
                # Check if new phone already exists
                existing = Client.find_by_phone(self.session, new_phone)
                if existing and existing.id != client_id:
                    print(f"❌ Phone number already registered to {existing.full_name}")
                    return
                updates['phone'] = new_phone

            new_email = input(f"Email [{client.email or 'None'}]: ").strip()
            if new_email:
                updates['email'] = new_email if new_email.lower() != 'none' else None

            new_notes = input(f"Notes [{client.notes or 'None'}]: ").strip()
            if new_notes:
                updates['notes'] = new_notes if new_notes.lower() != 'none' else None

            if updates:
                Client.update(self.session, client_id, **updates)
                print(f"\n✅ Client {client_id} updated successfully!")
            else:
                print("\nℹ️  No changes made.")

        except ValueError:
            print("❌ Please enter a valid number.")
        except Exception as e:
            print(f"❌ Error updating client: {e}")

    def view_client_appointments(self):
        """View all appointments for a specific client."""
        try:
            client_id = int(input("\nEnter Client ID: ").strip())
            client = Client.find_by_id(self.session, client_id)

            if not client:
                print(f"❌ No client found with ID {client_id}")
                return

            appointments = client.get_appointments(self.session)

            if not appointments:
                print(f"\n📭 No appointments found for {client.full_name}")
                return

            print(f"\n📅 APPOINTMENTS FOR {client.full_name.upper()} ({len(appointments)} total)")
            print("-" * 90)
            print(f"{'Date':<20} {'Time':<10} {'Stylist':<20} {'Service':<25} {'Status':<12} {'Price':<10}")
            print("-" * 90)

            for app in appointments:
                stylist_name = app.stylist.full_name if app.stylist else "N/A"
                service_name = app.service.name if app.service else "N/A"
                print(f"{app.date_only:<20} {app.time_only:<10} {stylist_name:<20} {service_name:<25} {app.status:<12} ${app.total_price:<9.2f}")

        except ValueError:
            print("❌ Please enter a valid number.")

    def delete_client(self):
        """Delete a client from the database."""
        try:
            client_id = int(input("\nEnter Client ID to delete: ").strip())
            client = Client.find_by_id(self.session, client_id)

            if not client:
                print(f"❌ No client found with ID {client_id}")
                return

            # Show client details first
            self.display_client_details(client)

            # Ask for confirmation
            confirm = input(f"\n⚠️  Are you sure you want to delete {client.full_name}? (yes/no): ").strip().lower()

            if confirm == 'yes':
                # Check if client has appointments
                appointments = client.get_appointments(self.session)
                if appointments:
                    print(f"❌ Cannot delete client with {len(appointments)} existing appointment(s).")
                    print("   Please cancel or reassign appointments first.")
                    return

                if Client.delete(self.session, client_id):
                    print(f"✅ Client {client.full_name} deleted successfully!")
                else:
                    print(f"❌ Failed to delete client.")
            else:
                print("❌ Deletion cancelled.")

        except ValueError:
            print("❌ Please enter a valid number.")

    

    def exit_program(self):
        """Exit the program gracefully."""
        print("\n" + "="*60)
        print("Thank you for using SalonPro Manager!")
        print("Goodbye! 👋")
        print("="*60)
        self.session.close()
        sys.exit(0)


def main():
    """Main function to run the CLI."""
    cli = SalonProCLI()
    cli.run()


if __name__ == "__main__":
    main()