#!/usr/bin/env python3
"""
SalonPro Manager - CLI Application
Main entry point for the salon management system.
"""

from database import init_db, get_session
from models import Client, Stylist, Service, Appointment
from datetime import datetime, date, timedelta, time
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
        print("\nMAIN MENU")
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
        print("\nCLIENT MANAGEMENT")
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
        print("\nSTYLIST MANAGEMENT")
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
        print("\nSERVICE MANAGEMENT")
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
        print("\nAPPOINTMENT MANAGEMENT")
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
        print("\nSEARCH & FIND")
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
                print("Invalid choice. Please enter a number between 0-6.")

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
                print("Invalid choice. Please enter a number between 1-9.")

    def view_all_clients(self):
        """Display all clients."""
        clients = Client.get_all(self.session)
        if not clients:
            print("\nNo clients found.")
            return

        print(f"\nALL CLIENTS ({len(clients)} total)")
        print("-" * 70)
        print(f"{'ID':<5} {'Name':<25} {'Phone':<15} {'Email':<25}")
        print("-" * 70)

        for client in clients:
            print(f"{client.id:<5} {client.full_name:<25} {client.formatted_phone:<15} {client.email or 'N/A':<25}")

    def add_new_client(self):
        """Add a new client to the database."""
        print("\nADD NEW CLIENT")
        print("-" * 40)

        try:
            first_name = input("First Name: ").strip()
            last_name = input("Last Name: ").strip()
            phone = input("Phone Number: ").strip()
            email = input("Email (optional): ").strip() or None
            notes = input("Notes (optional): ").strip() or None

            if not first_name or not last_name or not phone:
                print("First name, last name, and phone are required.")
                return

            # Check if phone already exists
            existing = Client.find_by_phone(self.session, phone)
            if existing:
                print(f"Phone number already registered to {existing.full_name}")
                return

            client = Client.create(
                session=self.session,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                email=email,
                notes=notes
            )

            print(f"\nClient added successfully!")
            print(f"   Name: {client.full_name}")
            print(f"   ID: {client.id}")

        except Exception as e:
            print(f"Error adding client: {e}")

    def find_client_by_id(self):
        """Find a client by their ID."""
        try:
            client_id = int(input("\nEnter Client ID: ").strip())
            client = Client.find_by_id(self.session, client_id)

            if client:
                self.display_client_details(client)
            else:
                print(f"No client found with ID {client_id}")
        except ValueError:
            print("Please enter a valid number.")

    def find_client_by_name(self):
        """Find clients by name (partial match)."""
        name = input("\nEnter client name (or part): ").strip()
        if not name:
            print("Please enter a name to search.")
            return

        clients = Client.find_by_name(self.session, name)

        if not clients:
            print(f"No clients found matching '{name}'")
            return

        print(f"\nFOUND {len(clients)} CLIENT(S)")
        print("-" * 70)
        for client in clients:
            print(f"ID: {client.id} | Name: {client.full_name} | Phone: {client.formatted_phone}")

    def find_client_by_phone(self):
        """Find a client by phone number."""
        phone = input("\nEnter phone number: ").strip()
        if not phone:
            print("Please enter a phone number.")
            return

        client = Client.find_by_phone(self.session, phone)

        if client:
            self.display_client_details(client)
        else:
            print(f"No client found with phone {phone}")

    def display_client_details(self, client):
        """Display detailed information about a client."""
        print(f"\nCLIENT DETAILS")
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
                print(f"No client found with ID {client_id}")
                return

            self.display_client_details(client)
            print("\nUPDATE CLIENT (leave blank to keep current value)")
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
                    print(f"Phone number already registered to {existing.full_name}")
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
                print(f"\nClient {client_id} updated successfully!")
            else:
                print("\nNo changes made.")

        except ValueError:
            print("Please enter a valid number.")
        except Exception as e:
            print(f"Error updating client: {e}")

    def view_client_appointments(self):
        """View all appointments for a specific client."""
        try:
            client_id = int(input("\nEnter Client ID: ").strip())
            client = Client.find_by_id(self.session, client_id)

            if not client:
                print(f"No client found with ID {client_id}")
                return

            appointments = client.get_appointments(self.session)

            if not appointments:
                print(f"\nNo appointments found for {client.full_name}")
                return

            print(f"\nAPPOINTMENTS FOR {client.full_name.upper()} ({len(appointments)} total)")
            print("-" * 90)
            print(f"{'Date':<20} {'Time':<10} {'Stylist':<20} {'Service':<25} {'Status':<12} {'Price':<10}")
            print("-" * 90)

            for app in appointments:
                stylist_name = app.stylist.full_name if app.stylist else "N/A"
                service_name = app.service.name if app.service else "N/A"
                print(f"{app.date_only:<20} {app.time_only:<10} {stylist_name:<20} {service_name:<25} {app.status:<12} ${app.total_price:<9.2f}")

        except ValueError:
            print("Please enter a valid number.")

    def delete_client(self):
        """Delete a client from the database."""
        try:
            client_id = int(input("\nEnter Client ID to delete: ").strip())
            client = Client.find_by_id(self.session, client_id)

            if not client:
                print(f"No client found with ID {client_id}")
                return

            # Show client details first
            self.display_client_details(client)

            # Ask for confirmation
            confirm = input(f"\nAre you sure you want to delete {client.full_name}? (yes/no): ").strip().lower()

            if confirm == 'yes':
                # Check if client has appointments
                appointments = client.get_appointments(self.session)
                if appointments:
                    print(f"Cannot delete client with {len(appointments)} existing appointment(s).")
                    print("   Please cancel or reassign appointments first.")
                    return

                if Client.delete(self.session, client_id):
                    print(f"Client {client.full_name} deleted successfully!")
                else:
                    print(f"Failed to delete client.")
            else:
                print("Deletion cancelled.")

        except ValueError:
            print("Please enter a valid number.")

    

    def exit_program(self):
        """Exit the program gracefully."""
        print("\n" + "="*60)
        print("Thank you for using SalonPro Manager!")
        print("Goodbye!")
        print("="*60)
        self.session.close()
        sys.exit(0)

    # ========== STYLIST MANAGEMENT METHODS ==========
    
    def handle_stylist_management(self):
        """Handle stylist management operations."""
        while True:
            self.stylist_management_menu()
            choice = input("\nEnter your choice (1-9): ").strip()
            
            if choice == "9":
                break
            elif choice == "1":
                self.view_all_stylists()
            elif choice == "2":
                self.add_new_stylist()
            elif choice == "3":
                self.find_stylist_by_id()
            elif choice == "4":
                self.find_stylist_by_specialty()
            elif choice == "5":
                self.view_stylist_schedule()
            elif choice == "6":
                self.update_stylist()
            elif choice == "7":
                self.view_stylist_clients()
            elif choice == "8":
                self.deactivate_stylist()
            else:
                print("Invalid choice. Please enter a number between 1-9.")
    
    def view_all_stylists(self):
        """Display all stylists."""
        stylists = Stylist.get_all(self.session)
        if not stylists:
            print("\nNo stylists found.")
            return
        
        print(f"\nALL STYLISTS ({len(stylists)} total)")
        print("-" * 80)
        print(f"{'ID':<5} {'Name':<25} {'Specialty':<20} {'Hourly Rate':<12} {'Status':<10}")
        print("-" * 80)
        
        for stylist in stylists:
            status = "Active" if stylist.is_active else "Inactive"
            print(f"{stylist.id:<5} {stylist.full_name:<25} {stylist.specialty or 'N/A':<20} ${stylist.hourly_rate:<11.2f} {status:<10}")
    
    def add_new_stylist(self):
        """Add a new stylist to the database."""
        print("\nADD NEW STYLIST")
        print("-" * 40)
        
        try:
            first_name = input("First Name: ").strip()
            last_name = input("Last Name: ").strip()
            phone = input("Phone Number: ").strip()
            email = input("Email: ").strip()
            specialty = input("Specialty (e.g., Coloring, Haircut): ").strip()
            hourly_rate = input("Hourly Rate (default 25.00): ").strip()
            
            if not first_name or not last_name or not phone or not email:
                print("First name, last name, phone, and email are required.")
                return
            
            # Convert hourly rate
            try:
                hourly_rate = float(hourly_rate) if hourly_rate else 25.0
            except ValueError:
                print("Hourly rate must be a number.")
                return
            
            # Check if phone already exists
            existing = self.session.query(Stylist).filter_by(phone=phone).first()
            if existing:
                print(f"Phone number already registered to {existing.full_name}")
                return
            
            stylist = Stylist.create(
                session=self.session,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                email=email,
                specialty=specialty,
                hourly_rate=hourly_rate
            )
            
            print(f"\nStylist added successfully!")
            print(f"   Name: {stylist.full_name}")
            print(f"   ID: {stylist.id}")
            print(f"   Specialty: {stylist.specialty}")
            
        except Exception as e:
            print(f"Error adding stylist: {e}")
    
    def find_stylist_by_id(self):
        """Find a stylist by their ID."""
        try:
            stylist_id = int(input("\nEnter Stylist ID: ").strip())
            stylist = Stylist.find_by_id(self.session, stylist_id)
            
            if stylist:
                self.display_stylist_details(stylist)
            else:
                print(f"No stylist found with ID {stylist_id}")
        except ValueError:
            print("Please enter a valid number.")
    
    def find_stylist_by_specialty(self):
        """Find stylists by specialty."""
        specialty = input("\nEnter specialty to search: ").strip()
        if not specialty:
            print("Please enter a specialty to search.")
            return
        
        stylists = Stylist.find_by_specialty(self.session, specialty)
        
        if not stylists:
            print(f"No stylists found with specialty '{specialty}'")
            return
        
        print(f"\nFOUND {len(stylists)} STYLIST(S) WITH SPECIALTY '{specialty.upper()}'")
        print("-" * 70)
        for stylist in stylists:
            status = "Active" if stylist.is_active else "Inactive"
            print(f"ID: {stylist.id} | Name: {stylist.full_name} | Rate: ${stylist.hourly_rate}/hr | Status: {status}")
    
    def display_stylist_details(self, stylist):
        """Display detailed information about a stylist."""
        print(f"\nSTYLIST DETAILS")
        print("-" * 40)
        print(f"ID: {stylist.id}")
        print(f"Name: {stylist.full_name}")
        print(f"Phone: {stylist.formatted_phone}")
        print(f"Email: {stylist.email}")
        print(f"Specialty: {stylist.specialty}")
        print(f"Hourly Rate: ${stylist.hourly_rate:.2f}")
        print(f"Experience: {stylist.experience_years} years")
        print(f"Status: {'Active' if stylist.is_active else 'Inactive'}")
        print(f"Hire Date: {stylist.hire_date.strftime('%Y-%m-%d')}")
        
        # Show appointment count
        appointments = stylist.get_appointments(self.session)
        print(f"Total Appointments: {len(appointments)}")
        
        # Show today's appointments
        todays = stylist.get_todays_appointments(self.session)
        if todays:
            print(f"Today's Appointments: {len(todays)}")
    
    def view_stylist_schedule(self):
        """View a stylist's schedule."""
        try:
            stylist_id = int(input("\nEnter Stylist ID: ").strip())
            stylist = Stylist.find_by_id(self.session, stylist_id)
            
            if not stylist:
                print(f"No stylist found with ID {stylist_id}")
                return
            
            # Get upcoming appointments
            appointments = Appointment.find_by_stylist(self.session, stylist_id)
            upcoming = [app for app in appointments if app.is_upcoming]
            
            if not upcoming:
                print(f"\nNo upcoming appointments for {stylist.full_name}")
                return
            
            print(f"\nUPCOMING SCHEDULE FOR {stylist.full_name.upper()} ({len(upcoming)} appointments)")
            print("-" * 90)
            print(f"{'Date':<12} {'Time':<10} {'Client':<20} {'Service':<25} {'Duration':<10} {'Price':<10}")
            print("-" * 90)
            
            for app in sorted(upcoming, key=lambda x: x.appointment_date):
                client_name = app.client.full_name if app.client else "N/A"
                service_name = app.service.name if app.service else "N/A"
                print(f"{app.date_only:<12} {app.time_only:<10} {client_name:<20} {service_name:<25} {app.duration_minutes} min{'':<5} ${app.total_price:<9.2f}")
                
        except ValueError:
            print("Please enter a valid number.")
    
    def update_stylist(self):
        """Update stylist information."""
        try:
            stylist_id = int(input("\nEnter Stylist ID to update: ").strip())
            stylist = Stylist.find_by_id(self.session, stylist_id)
            
            if not stylist:
                print(f"No stylist found with ID {stylist_id}")
                return
            
            self.display_stylist_details(stylist)
            print("\nUPDATE STYLIST (leave blank to keep current value)")
            print("-" * 40)
            
            updates = {}
            
            new_first = input(f"First Name [{stylist.first_name}]: ").strip()
            if new_first:
                updates['first_name'] = new_first
            
            new_last = input(f"Last Name [{stylist.last_name}]: ").strip()
            if new_last:
                updates['last_name'] = new_last
            
            new_phone = input(f"Phone [{stylist.phone}]: ").strip()
            if new_phone and new_phone != stylist.phone:
                # Check if new phone already exists
                existing = self.session.query(Stylist).filter_by(phone=new_phone).first()
                if existing and existing.id != stylist_id:
                    print(f"Phone number already registered to {existing.full_name}")
                    return
                updates['phone'] = new_phone
            
            new_email = input(f"Email [{stylist.email}]: ").strip()
            if new_email:
                updates['email'] = new_email
            
            new_specialty = input(f"Specialty [{stylist.specialty}]: ").strip()
            if new_specialty:
                updates['specialty'] = new_specialty
            
            new_rate = input(f"Hourly Rate [${stylist.hourly_rate:.2f}]: ").strip()
            if new_rate:
                try:
                    updates['hourly_rate'] = float(new_rate.replace('$', ''))
                except ValueError:
                    print("Hourly rate must be a number.")
                    return
            
            if updates:
                Stylist.update(self.session, stylist_id, **updates)
                print(f"\nStylist {stylist_id} updated successfully!")
            else:
                print("\nNo changes made.")
                
        except ValueError:
            print("Please enter a valid number.")
        except Exception as e:
            print(f"Error updating stylist: {e}")
    
    def view_stylist_clients(self):
        """View all clients of a specific stylist."""
        try:
            stylist_id = int(input("\nEnter Stylist ID: ").strip())
            stylist = Stylist.find_by_id(self.session, stylist_id)
            
            if not stylist:
                print(f"No stylist found with ID {stylist_id}")
                return
            
            # Get all appointments for this stylist
            appointments = Appointment.find_by_stylist(self.session, stylist_id)
            
            if not appointments:
                print(f"\nNo appointments found for {stylist.full_name}")
                return
            
            # Get unique clients
            client_ids = set()
            for app in appointments:
                if app.client:
                    client_ids.add(app.client.id)
            
            print(f"\nCLIENTS OF {stylist.full_name.upper()} ({len(client_ids)} unique clients)")
            print("-" * 70)
            
            for client_id in client_ids:
                client = Client.find_by_id(self.session, client_id)
                if client:
                    # Count appointments with this stylist
                    client_appointments = [app for app in appointments if app.client_id == client_id]
                    print(f"• {client.full_name} ({len(client_appointments)} appointments)")
                    
        except ValueError:
            print("Please enter a valid number.")
    
    def deactivate_stylist(self):
        """Deactivate a stylist."""
        try:
            stylist_id = int(input("\nEnter Stylist ID to deactivate: ").strip())
            stylist = Stylist.find_by_id(self.session, stylist_id)
            
            if not stylist:
                print(f"No stylist found with ID {stylist_id}")
                return
            
            # Show stylist details first
            self.display_stylist_details(stylist)
            
            # Ask for confirmation
            confirm = input(f"\nAre you sure you want to deactivate {stylist.full_name}? (yes/no): ").strip().lower()
            
            if confirm == 'yes':
                # Check if stylist has upcoming appointments
                appointments = stylist.get_appointments(self.session)
                upcoming = [app for app in appointments if app.is_upcoming]
                
                if upcoming:
                    print(f"Cannot deactivate stylist with {len(upcoming)} upcoming appointment(s).")
                    print("   Please cancel or reassign appointments first.")
                    return
                
                stylist.is_active = 0
                self.session.commit()
                print(f"Stylist {stylist.full_name} deactivated successfully!")
            else:
                print("Deactivation cancelled.")
                
        except ValueError:
            print("Please enter a valid number.")
    # ========== SERVICE MANAGEMENT METHODS ==========
    
    def handle_service_management(self):
        """Handle service management operations."""
        while True:
            self.service_management_menu()
            choice = input("\nEnter your choice (1-9): ").strip()
            
            if choice == "9":
                break
            elif choice == "1":
                self.view_all_services()
            elif choice == "2":
                self.view_service_menu()
            elif choice == "3":
                self.add_new_service()
            elif choice == "4":
                self.find_service_by_id()
            elif choice == "5":
                self.find_service_by_category()
            elif choice == "6":
                self.update_service()
            elif choice == "7":
                self.view_service_popularity()
            elif choice == "8":
                self.deactivate_service()
            else:
                print("Invalid choice. Please enter a number between 1-9.")
    
    def view_all_services(self):
        """Display all services."""
        services = Service.get_all(self.session)
        if not services:
            print("\nNo services found.")
            return
        
        print(f"\nALL SERVICES ({len(services)} total)")
        print("-" * 90)
        print(f"{'ID':<5} {'Name':<25} {'Category':<15} {'Duration':<12} {'Price':<10} {'Status':<10}")
        print("-" * 90)
        
        for service in services:
            status = "Active" if service.is_active else "Inactive"
            print(f"{service.id:<5} {service.name:<25} {service.category or 'N/A':<15} {service.formatted_duration:<12} {service.formatted_price:<10} {status:<10}")
    
    def view_service_menu(self):
        """Display active services only (menu for clients)."""
        services = Service.get_active(self.session)
        if not services:
            print("\nNo active services found.")
            return
        
        print(f"\nSERVICE MENU ({len(services)} active services)")
        print("-" * 80)
        print(f"{'ID':<5} {'Name':<25} {'Category':<15} {'Duration':<12} {'Price':<10}")
        print("-" * 80)
        
        for service in services:
            print(f"{service.id:<5} {service.name:<25} {service.category or 'N/A':<15} {service.formatted_duration:<12} {service.formatted_price:<10}")
    
    def add_new_service(self):
        """Add a new service to the database."""
        print("\nADD NEW SERVICE")
        print("-" * 40)
        
        try:
            name = input("Service Name: ").strip()
            category = input("Category (e.g., Haircut, Color): ").strip()
            duration = input("Duration in minutes: ").strip()
            price = input("Price: ").strip()
            description = input("Description (optional): ").strip() or None
            
            if not name or not category or not duration or not price:
                print("Service name, category, duration, and price are required.")
                return
            
            # Convert to proper types
            try:
                duration = int(duration)
                price = float(price)
            except ValueError:
                print("Duration must be a whole number and price must be a number.")
                return
            
            # Check if service name already exists
            existing = self.session.query(Service).filter_by(name=name).first()
            if existing:
                print(f"Service '{name}' already exists (ID: {existing.id})")
                return
            
            service = Service.create(
                session=self.session,
                name=name,
                description=description,
                duration_minutes=duration,
                price=price,
                category=category
            )
            
            print(f"\nService added successfully!")
            print(f"   Name: {service.name}")
            print(f"   ID: {service.id}")
            print(f"   Price: {service.formatted_price}")
            print(f"   Duration: {service.formatted_duration}")
            
        except Exception as e:
            print(f"Error adding service: {e}")
    
    def find_service_by_id(self):
        """Find a service by its ID."""
        try:
            service_id = int(input("\nEnter Service ID: ").strip())
            service = Service.find_by_id(self.session, service_id)
            
            if service:
                self.display_service_details(service)
            else:
                print(f"No service found with ID {service_id}")
        except ValueError:
            print("Please enter a valid number.")
    
    def find_service_by_category(self):
        """Find services by category."""
        category = input("\nEnter category to search: ").strip()
        if not category:
            print("Please enter a category to search.")
            return
        
        services = Service.find_by_category(self.session, category)
        
        if not services:
            print(f"No services found in category '{category}'")
            return
        
        print(f"\nFOUND {len(services)} SERVICE(S) IN CATEGORY '{category.upper()}'")
        print("-" * 70)
        for service in services:
            status = "Active" if service.is_active else "Inactive"
            print(f"ID: {service.id} | Name: {service.name} | Price: {service.formatted_price} | Status: {status}")
    
    def display_service_details(self, service):
        """Display detailed information about a service."""
        print(f"\nSERVICE DETAILS")
        print("-" * 40)
        print(f"ID: {service.id}")
        print(f"Name: {service.name}")
        print(f"Description: {service.description or 'None'}")
        print(f"Category: {service.category}")
        print(f"Duration: {service.formatted_duration}")
        print(f"Price: {service.formatted_price}")
        print(f"Hourly Rate Equivalent: ${service.hourly_rate:.2f}/hr")
        print(f"Status: {'Active' if service.is_active else 'Inactive'}")
        print(f"Created: {service.created_at.strftime('%Y-%m-%d')}")
        
        # Show appointment count
        appointments = service.get_appointments(self.session)
        print(f"Total Bookings: {len(appointments)}")
    
    def update_service(self):
        """Update service information."""
        try:
            service_id = int(input("\nEnter Service ID to update: ").strip())
            service = Service.find_by_id(self.session, service_id)
            
            if not service:
                print(f"No service found with ID {service_id}")
                return
            
            self.display_service_details(service)
            print("\nUPDATE SERVICE (leave blank to keep current value)")
            print("-" * 40)
            
            updates = {}
            
            new_name = input(f"Service Name [{service.name}]: ").strip()
            if new_name and new_name != service.name:
                # Check if new name already exists
                existing = self.session.query(Service).filter_by(name=new_name).first()
                if existing and existing.id != service_id:
                    print(f"Service '{new_name}' already exists (ID: {existing.id})")
                    return
                updates['name'] = new_name
            
            new_category = input(f"Category [{service.category}]: ").strip()
            if new_category:
                updates['category'] = new_category
            
            new_duration = input(f"Duration [{service.duration_minutes} minutes]: ").strip()
            if new_duration:
                try:
                    updates['duration_minutes'] = int(new_duration)
                except ValueError:
                    print("Duration must be a whole number.")
                    return
            
            new_price = input(f"Price [${service.price:.2f}]: ").strip()
            if new_price:
                try:
                    updates['price'] = float(new_price.replace('$', ''))
                except ValueError:
                    print("Price must be a number.")
                    return
            
            new_desc = input(f"Description [{service.description or 'None'}]: ").strip()
            if new_desc:
                updates['description'] = new_desc if new_desc.lower() != 'none' else None
            
            if updates:
                Service.update(self.session, service_id, **updates)
                print(f"\nService {service_id} updated successfully!")
            else:
                print("\nNo changes made.")
                
        except ValueError:
            print("Please enter a valid number.")
        except Exception as e:
            print(f"Error updating service: {e}")
    
    def view_service_popularity(self):
        """View service popularity based on bookings."""
        services = Service.get_all(self.session)
        
        if not services:
            print("\nNo services found.")
            return
        
        # Get appointment counts for each service
        service_stats = []
        for service in services:
            appointments = service.get_appointments(self.session)
            completed = [app for app in appointments if app.status == 'completed']
            service_stats.append({
                'service': service,
                'total_bookings': len(appointments),
                'completed_bookings': len(completed),
                'revenue': sum(app.total_price for app in completed)
            })
        
        # Sort by total bookings
        service_stats.sort(key=lambda x: x['total_bookings'], reverse=True)
        
        print(f"\nSERVICE POPULARITY REPORT")
        print("-" * 100)
        print(f"{'Rank':<6} {'Service':<25} {'Category':<15} {'Total Bookings':<15} {'Completed':<12} {'Revenue':<12}")
        print("-" * 100)
        
        for i, stats in enumerate(service_stats, 1):
            service = stats['service']
            print(f"{i:<6} {service.name:<25} {service.category or 'N/A':<15} {stats['total_bookings']:<15} {stats['completed_bookings']:<12} ${stats['revenue']:<11.2f}")
    
    def deactivate_service(self):
        """Deactivate a service."""
        try:
            service_id = int(input("\nEnter Service ID to deactivate: ").strip())
            service = Service.find_by_id(self.session, service_id)
            
            if not service:
                print(f"No service found with ID {service_id}")
                return
            
            # Show service details first
            self.display_service_details(service)
            
            # Ask for confirmation
            confirm = input(f"\nAre you sure you want to deactivate '{service.name}'? (yes/no): ").strip().lower()
            
            if confirm == 'yes':
                # Check if service has upcoming appointments
                appointments = service.get_appointments(self.session)
                upcoming = [app for app in appointments if app.is_upcoming]
                
                if upcoming:
                    print(f"Cannot deactivate service with {len(upcoming)} upcoming appointment(s).")
                    print("   Please cancel or reassign appointments first.")
                    return
                
                if Service.delete(self.session, service_id):
                    print(f"Service '{service.name}' deactivated successfully!")
                else:
                    print(f"Failed to deactivate service.")
            else:
                print("Deactivation cancelled.")
                
        except ValueError:
            print("Please enter a valid number.")

    # ========== APPOINTMENT MANAGEMENT METHODS ==========
    
    def handle_appointment_management(self):
        """Handle appointment management operations."""
        while True:
            self.appointment_management_menu()
            choice = input("\nEnter your choice (1-12): ").strip()
            
            if choice == "12":
                break
            elif choice == "1":
                self.view_all_appointments()
            elif choice == "2":
                self.view_todays_appointments()
            elif choice == "3":
                self.view_upcoming_appointments()
            elif choice == "4":
                self.schedule_new_appointment()
            elif choice == "5":
                self.find_appointment_by_id()
            elif choice == "6":
                self.find_appointments_by_date()
            elif choice == "7":
                self.find_appointments_by_client()
            elif choice == "8":
                self.find_appointments_by_stylist()
            elif choice == "9":
                self.update_appointment_status()
            elif choice == "10":
                self.cancel_appointment()
            elif choice == "11":
                self.delete_appointment()
            else:
                print("Invalid choice. Please enter a number between 1-12.")
    
    def view_all_appointments(self):
        """Display all appointments."""
        appointments = Appointment.get_all(self.session)
        if not appointments:
            print("\nNo appointments found.")
            return
        
        print(f"\nALL APPOINTMENTS ({len(appointments)} total)")
        print("-" * 120)
        print(f"{'ID':<5} {'Date':<12} {'Time':<10} {'Client':<20} {'Stylist':<20} {'Service':<20} {'Status':<12} {'Price':<10}")
        print("-" * 120)
        
        for app in sorted(appointments, key=lambda x: x.appointment_date, reverse=True):
            client_name = app.client.full_name if app.client else "N/A"
            stylist_name = app.stylist.full_name if app.stylist else "N/A"
            service_name = app.service.name if app.service else "N/A"
            print(f"{app.id:<5} {app.date_only:<12} {app.time_only:<10} {client_name:<20} {stylist_name:<20} {service_name:<20} {app.status:<12} ${app.total_price:<9.2f}")
    
    def view_todays_appointments(self):
        """Display today's appointments."""
        today = date.today()
        appointments = Appointment.find_by_date(self.session, today)
        
        if not appointments:
            print("\nNo appointments scheduled for today.")
            return
        
        # Filter for scheduled appointments only
        todays_apps = [app for app in appointments if app.status == 'scheduled']
        
        if not todays_apps:
            print(f"\nNo scheduled appointments for today ({len(appointments) - len(todays_apps)} cancelled/completed)")
            return
        
        print(f"\nTODAY'S APPOINTMENTS ({len(todays_apps)} scheduled)")
        print("-" * 100)
        print(f"{'Time':<10} {'Client':<20} {'Stylist':<20} {'Service':<25} {'Duration':<10} {'Price':<10}")
        print("-" * 100)
        
        for app in sorted(todays_apps, key=lambda x: x.appointment_date):
            client_name = app.client.full_name if app.client else "N/A"
            stylist_name = app.stylist.full_name if app.stylist else "N/A"
            service_name = app.service.name if app.service else "N/A"
            print(f"{app.time_only:<10} {client_name:<20} {stylist_name:<20} {service_name:<25} {app.duration_minutes} min{'':<5} ${app.total_price:<9.2f}")
    
    def view_upcoming_appointments(self):
        """Display all upcoming appointments."""
        appointments = Appointment.find_upcoming(self.session)
        
        if not appointments:
            print("\nNo upcoming appointments.")
            return
        
        print(f"\nUPCOMING APPOINTMENTS ({len(appointments)} total)")
        print("-" * 110)
        print(f"{'Date':<12} {'Time':<10} {'Client':<20} {'Stylist':<20} {'Service':<25} {'Duration':<10} {'Price':<10}")
        print("-" * 110)
        
        for app in sorted(appointments, key=lambda x: x.appointment_date):
            client_name = app.client.full_name if app.client else "N/A"
            stylist_name = app.stylist.full_name if app.stylist else "N/A"
            service_name = app.service.name if app.service else "N/A"
            print(f"{app.date_only:<12} {app.time_only:<10} {client_name:<20} {stylist_name:<20} {service_name:<25} {app.duration_minutes} min{'':<5} ${app.total_price:<9.2f}")
    
    def schedule_new_appointment(self):
        """Schedule a new appointment."""
        print("\nSCHEDULE NEW APPOINTMENT")
        print("-" * 40)
        
        try:
            # Show available clients
            clients = Client.get_all(self.session)
            if not clients:
                print("No clients available. Please add a client first.")
                return
            
            print("\nAvailable Clients:")
            for client in clients[:10]:  # Show first 10
                print(f"  {client.id}. {client.full_name}")
            
            client_id = int(input("\nSelect Client ID: ").strip())
            client = Client.find_by_id(self.session, client_id)
            if not client:
                print(f"No client found with ID {client_id}")
                return
            
            # Show available stylists
            stylists = Stylist.get_active(self.session)
            if not stylists:
                print("No active stylists available. Please add a stylist first.")
                return
            
            print("\nAvailable Stylists:")
            for stylist in stylists:
                print(f"  {stylist.id}. {stylist.full_name} ({stylist.specialty})")
            
            stylist_id = int(input("\nSelect Stylist ID: ").strip())
            stylist = Stylist.find_by_id(self.session, stylist_id)
            if not stylist or not stylist.is_active:
                print(f"No active stylist found with ID {stylist_id}")
                return
            
            # Show available services
            services = Service.get_active(self.session)
            if not services:
                print("No active services available. Please add a service first.")
                return
            
            print("\nAvailable Services:")
            for service in services:
                print(f"  {service.id}. {service.name} (${service.price}, {service.duration_minutes}min)")
            
            service_id = int(input("\nSelect Service ID: ").strip())
            service = Service.find_by_id(self.session, service_id)
            if not service or not service.is_active:
                print(f"No active service found with ID {service_id}")
                return
            
            # Get appointment date and time
            date_str = input("Appointment Date (YYYY-MM-DD): ").strip()
            time_str = input("Appointment Time (HH:MM in 24-hour format): ").strip()
            
            if not date_str or not time_str:
                print("Date and time are required.")
                return
            
            # Parse date and time
            try:
                year, month, day = map(int, date_str.split('-'))
                hour, minute = map(int, time_str.split(':'))
                appointment_datetime = datetime(year, month, day, hour, minute)
            except ValueError:
                print("Invalid date or time format.")
                return
            
            # Check if appointment is in the past
            if appointment_datetime < datetime.now():
                print("Cannot schedule appointments in the past.")
                return
            
            # Check business hours (9 AM to 6 PM)
            if hour < 9 or hour >= 18:
                print("Appointments can only be scheduled between 9 AM and 6 PM.")
                return
            
            notes = input("Notes (optional): ").strip() or None
            
            # Create the appointment
            appointment = Appointment.create(
                session=self.session,
                client_id=client_id,
                stylist_id=stylist_id,
                service_id=service_id,
                appointment_date=appointment_datetime,
                duration_minutes=service.duration_minutes,
                total_price=service.price,
                notes=notes
            )
            
            print(f"\nAppointment scheduled successfully!")
            print(f"   ID: {appointment.id}")
            print(f"   Client: {client.full_name}")
            print(f"   Stylist: {stylist.full_name}")
            print(f"   Service: {service.name}")
            print(f"   Date & Time: {appointment.formatted_date}")
            print(f"   Duration: {service.formatted_duration}")
            print(f"   Price: ${service.price:.2f}")
            
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error scheduling appointment: {e}")
    
    def find_appointment_by_id(self):
        """Find an appointment by its ID."""
        try:
            appointment_id = int(input("\nEnter Appointment ID: ").strip())
            appointment = Appointment.find_by_id(self.session, appointment_id)
            
            if appointment:
                self.display_appointment_details(appointment)
            else:
                print(f"No appointment found with ID {appointment_id}")
        except ValueError:
            print("Please enter a valid number.")
    
    def find_appointments_by_date(self):
        """Find appointments on a specific date."""
        date_str = input("\nEnter date (YYYY-MM-DD): ").strip()
        if not date_str:
            print("Please enter a date.")
            return
        
        try:
            year, month, day = map(int, date_str.split('-'))
            search_date = date(year, month, day)
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")
            return
        
        appointments = Appointment.find_by_date(self.session, search_date)
        
        if not appointments:
            print(f"\nNo appointments found on {date_str}")
            return
        
        print(f"\nAPPOINTMENTS ON {date_str} ({len(appointments)} total)")
        print("-" * 100)
        print(f"{'Time':<10} {'Client':<20} {'Stylist':<20} {'Service':<25} {'Status':<12} {'Price':<10}")
        print("-" * 100)
        
        for app in sorted(appointments, key=lambda x: x.appointment_date):
            client_name = app.client.full_name if app.client else "N/A"
            stylist_name = app.stylist.full_name if app.stylist else "N/A"
            service_name = app.service.name if app.service else "N/A"
            print(f"{app.time_only:<10} {client_name:<20} {stylist_name:<20} {service_name:<25} {app.status:<12} ${app.total_price:<9.2f}")
    
    def find_appointments_by_client(self):
        """Find appointments for a specific client."""
        try:
            client_id = int(input("\nEnter Client ID: ").strip())
            client = Client.find_by_id(self.session, client_id)
            
            if not client:
                print(f"No client found with ID {client_id}")
                return
            
            appointments = Appointment.find_by_client(self.session, client_id)
            
            if not appointments:
                print(f"\nNo appointments found for {client.full_name}")
                return
            
            print(f"\nAPPOINTMENTS FOR {client.full_name.upper()} ({len(appointments)} total)")
            print("-" * 100)
            print(f"{'Date':<12} {'Time':<10} {'Stylist':<20} {'Service':<25} {'Status':<12} {'Price':<10}")
            print("-" * 100)
            
            for app in sorted(appointments, key=lambda x: x.appointment_date, reverse=True):
                stylist_name = app.stylist.full_name if app.stylist else "N/A"
                service_name = app.service.name if app.service else "N/A"
                print(f"{app.date_only:<12} {app.time_only:<10} {stylist_name:<20} {service_name:<25} {app.status:<12} ${app.total_price:<9.2f}")
                
        except ValueError:
            print("Please enter a valid number.")
    
    def find_appointments_by_stylist(self):
        """Find appointments for a specific stylist."""
        try:
            stylist_id = int(input("\nEnter Stylist ID: ").strip())
            stylist = Stylist.find_by_id(self.session, stylist_id)
            
            if not stylist:
                print(f"No stylist found with ID {stylist_id}")
                return
            
            appointments = Appointment.find_by_stylist(self.session, stylist_id)
            
            if not appointments:
                print(f"\nNo appointments found for {stylist.full_name}")
                return
            
            print(f"\nAPPOINTMENTS FOR {stylist.full_name.upper()} ({len(appointments)} total)")
            print("-" * 100)
            print(f"{'Date':<12} {'Time':<10} {'Client':<20} {'Service':<25} {'Status':<12} {'Price':<10}")
            print("-" * 100)
            
            for app in sorted(appointments, key=lambda x: x.appointment_date, reverse=True):
                client_name = app.client.full_name if app.client else "N/A"
                service_name = app.service.name if app.service else "N/A"
                print(f"{app.date_only:<12} {app.time_only:<10} {client_name:<20} {service_name:<25} {app.status:<12} ${app.total_price:<9.2f}")
                
        except ValueError:
            print("Please enter a valid number.")
    
    def display_appointment_details(self, appointment):
        """Display detailed information about an appointment."""
        print(f"\nAPPOINTMENT DETAILS")
        print("-" * 40)
        print(f"ID: {appointment.id}")
        print(f"Date & Time: {appointment.formatted_date}")
        print(f"Duration: {appointment.duration_minutes} minutes")
        print(f"Status: {appointment.status}")
        print(f"Price: ${appointment.total_price:.2f}")
        print(f"Notes: {appointment.notes or 'None'}")
        print(f"Created: {appointment.created_at.strftime('%Y-%m-%d %H:%M')}")
        
        # Client information
        if appointment.client:
            print(f"\nCLIENT:")
            print(f"  Name: {appointment.client.full_name}")
            print(f"  Phone: {appointment.client.formatted_phone}")
            print(f"  Email: {appointment.client.email or 'Not provided'}")
        
        # Stylist information
        if appointment.stylist:
            print(f"\nSTYLIST:")
            print(f"  Name: {appointment.stylist.full_name}")
            print(f"  Specialty: {appointment.stylist.specialty}")
            print(f"  Hourly Rate: ${appointment.stylist.hourly_rate:.2f}")
        
        # Service information
        if appointment.service:
            print(f"\nSERVICE:")
            print(f"  Name: {appointment.service.name}")
            print(f"  Category: {appointment.service.category}")
            print(f"  Duration: {appointment.service.formatted_duration}")
            print(f"  Price: ${appointment.service.price:.2f}")
    
    def update_appointment_status(self):
        """Update appointment status."""
        try:
            appointment_id = int(input("\nEnter Appointment ID: ").strip())
            appointment = Appointment.find_by_id(self.session, appointment_id)
            
            if not appointment:
                print(f"No appointment found with ID {appointment_id}")
                return
            
            self.display_appointment_details(appointment)
            print("\nUPDATE STATUS")
            print("-" * 40)
            print("Available statuses: scheduled, completed, cancelled, no-show")
            
            new_status = input(f"New Status [{appointment.status}]: ").strip().lower()
            if not new_status:
                print("No change made.")
                return
            
            # Validate status
            valid_statuses = ['scheduled', 'completed', 'cancelled', 'no-show']
            if new_status not in valid_statuses:
                print(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
                return
            
            # Update the appointment
            appointment.status = new_status
            self.session.commit()
            
            print(f"\nAppointment {appointment_id} status updated to '{new_status}'")
            
        except ValueError:
            print("Please enter a valid number.")
        except Exception as e:
            print(f"Error updating appointment: {e}")
    
    def cancel_appointment(self):
        """Cancel an appointment."""
        try:
            appointment_id = int(input("\nEnter Appointment ID to cancel: ").strip())
            appointment = Appointment.find_by_id(self.session, appointment_id)
            
            if not appointment:
                print(f"No appointment found with ID {appointment_id}")
                return
            
            # Show appointment details first
            self.display_appointment_details(appointment)
            
            if appointment.status == 'cancelled':
                print(f"\nAppointment is already cancelled.")
                return
            
            # Ask for confirmation
            confirm = input(f"\nAre you sure you want to cancel this appointment? (yes/no): ").strip().lower()
            
            if confirm == 'yes':
                if Appointment.cancel(self.session, appointment_id):
                    print(f"Appointment {appointment_id} cancelled successfully!")
                else:
                    print(f"Failed to cancel appointment.")
            else:
                print("Cancellation cancelled.")
                
        except ValueError:
            print("Please enter a valid number.")
    
    def delete_appointment(self):
        """Delete an appointment."""
        try:
            appointment_id = int(input("\nEnter Appointment ID to delete: ").strip())
            appointment = Appointment.find_by_id(self.session, appointment_id)
            
            if not appointment:
                print(f"No appointment found with ID {appointment_id}")
                return
            
            # Show appointment details first
            self.display_appointment_details(appointment)
            
            # Ask for confirmation
            confirm = input(f"\nAre you sure you want to DELETE this appointment? This cannot be undone. (yes/no): ").strip().lower()
            
            if confirm == 'yes':
                if Appointment.delete(self.session, appointment_id):
                    print(f"Appointment {appointment_id} deleted successfully!")
                else:
                    print(f"Failed to delete appointment.")
            else:
                print("Deletion cancelled.")
                
        except ValueError:
            print("Please enter a valid number.")

             # ========== REPORT METHODS ==========
    
    def handle_reports(self):
        """Handle reports and analytics."""
        print("\nREPORTS & ANALYTICS")
        print("-" * 40)
        print("1. Daily Revenue Report")
        print("2. Client Count Report")
        print("3. Stylist Performance Report")
        print("4. Service Popularity Report")
        print("5. Back to Main Menu")
        print("-" * 40)
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            self.daily_revenue_report()
        elif choice == "2":
            self.client_count_report()
        elif choice == "3":
            self.stylist_performance_report()
        elif choice == "4":
            self.view_service_popularity()  # Already implemented
        elif choice == "5":
            return
        else:
            print("Invalid choice.")
    
    def daily_revenue_report(self):
        """Generate daily revenue report."""
        date_str = input("\nEnter date for report (YYYY-MM-DD): ").strip()
        if not date_str:
            print("Please enter a date.")
            return
        
        try:
            year, month, day = map(int, date_str.split('-'))
            report_date = date(year, month, day)
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")
            return
        
        # Get appointments for the date
        appointments = Appointment.find_by_date(self.session, report_date)
        completed_appointments = [app for app in appointments if app.status == 'completed']
        
        print(f"\nDAILY REVENUE REPORT - {date_str}")
        print("=" * 60)
        print(f"Total Appointments: {len(appointments)}")
        print(f"Completed Appointments: {len(completed_appointments)}")
        print(f"Cancelled/No-Show: {len(appointments) - len(completed_appointments)}")
        
        if completed_appointments:
            total_revenue = sum(app.total_price for app in completed_appointments)
            print(f"\nTotal Revenue: ${total_revenue:.2f}")
            
            print(f"\nBreakdown by Service:")
            print("-" * 50)
            
            # Group by service
            service_revenue = {}
            for app in completed_appointments:
                if app.service:
                    service_name = app.service.name
                    service_revenue[service_name] = service_revenue.get(service_name, 0) + app.total_price
            
            for service_name, revenue in sorted(service_revenue.items(), key=lambda x: x[1], reverse=True):
                print(f"  {service_name}: ${revenue:.2f}")
        else:
            print(f"\nTotal Revenue: $0.00")
    
    def client_count_report(self):
        """Generate client count report."""
        clients = Client.get_all(self.session)
        
        print(f"\nCLIENT COUNT REPORT")
        print("=" * 60)
        print(f"Total Clients: {len(clients)}")
        
        # Count clients with appointments
        clients_with_appointments = 0
        total_appointments = 0
        appointment_counts = []
        
        for client in clients:
            appointments = client.get_appointments(self.session)
            if appointments:
                clients_with_appointments += 1
                total_appointments += len(appointments)
                appointment_counts.append(len(appointments))
        
        print(f"Clients with Appointments: {clients_with_appointments}")
        print(f"Clients without Appointments: {len(clients) - clients_with_appointments}")
        print(f"Total Appointments: {total_appointments}")
        
        if appointment_counts:
            avg_appointments = total_appointments / clients_with_appointments
            print(f"Average Appointments per Client: {avg_appointments:.1f}")
            print(f"Most Appointments by a Client: {max(appointment_counts)}")
            print(f"Least Appointments by a Client: {min(appointment_counts)}")
    
    def stylist_performance_report(self):
        """Generate stylist performance report."""
        stylists = Stylist.get_all(self.session)
        
        print(f"\nSTYLIST PERFORMANCE REPORT")
        print("=" * 80)
        print(f"{'Name':<20} {'Specialty':<15} {'Total Appts':<12} {'Completed':<12} {'Revenue':<12} {'Avg/Appt':<12}")
        print("=" * 80)
        
        for stylist in stylists:
            appointments = stylist.get_appointments(self.session)
            completed = [app for app in appointments if app.status == 'completed']
            revenue = sum(app.total_price for app in completed)
            
            avg_revenue = revenue / len(completed) if completed else 0
            
            print(f"{stylist.full_name:<20} {stylist.specialty or 'N/A':<15} {len(appointments):<12} {len(completed):<12} ${revenue:<11.2f} ${avg_revenue:<11.2f}")
    
    # ========== SEARCH METHODS ==========
    
    def handle_search(self):
        """Handle search operations."""
        while True:
            self.search_menu()
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == "4":
                break
            elif choice == "1":
                self.search_clients()
            elif choice == "2":
                self.search_appointments_by_date_range()
            elif choice == "3":
                self.search_revenue_by_date()
            else:
                print("Invalid choice. Please enter a number between 1-4.")
    
    def search_clients(self):
        """Search clients by various criteria."""
        print("\nSEARCH CLIENTS")
        print("-" * 40)
        print("1. By Name")
        print("2. By Phone")
        print("3. By Email")
        print("4. Back to Search Menu")
        print("-" * 40)
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            name = input("Enter name to search: ").strip()
            clients = Client.find_by_name(self.session, name)
            
            if clients:
                print(f"\nFOUND {len(clients)} CLIENT(S)")
                print("-" * 70)
                for client in clients:
                    print(f"ID: {client.id} | Name: {client.full_name} | Phone: {client.formatted_phone} | Email: {client.email or 'N/A'}")
            else:
                print(f"No clients found matching '{name}'")
                
        elif choice == "2":
            phone = input("Enter phone to search: ").strip()
            client = Client.find_by_phone(self.session, phone)
            
            if client:
                self.display_client_details(client)
            else:
                print(f"No client found with phone {phone}")
                
        elif choice == "3":
            email = input("Enter email to search: ").strip()
            clients = self.session.query(Client).filter(Client.email.ilike(f"%{email}%")).all()
            
            if clients:
                print(f"\nFOUND {len(clients)} CLIENT(S)")
                print("-" * 70)
                for client in clients:
                    print(f"ID: {client.id} | Name: {client.full_name} | Phone: {client.formatted_phone} | Email: {client.email}")
            else:
                print(f"No clients found with email containing '{email}'")
                
        elif choice == "4":
            return
        else:
            print("Invalid choice.")
    
    def search_appointments_by_date_range(self):
        """Search appointments within a date range."""
        print("\nSEARCH APPOINTMENTS BY DATE RANGE")
        print("-" * 40)
        
        try:
            start_str = input("Start Date (YYYY-MM-DD): ").strip()
            end_str = input("End Date (YYYY-MM-DD): ").strip()
            
            if not start_str or not end_str:
                print("Both start and end dates are required.")
                return
            
            # Parse dates
            start_year, start_month, start_day = map(int, start_str.split('-'))
            end_year, end_month, end_day = map(int, end_str.split('-'))
            
            start_date = date(start_year, start_month, start_day)
            end_date = date(end_year, end_month, end_day)
            
            if start_date > end_date:
                print("Start date must be before end date.")
                return
            
            # Query appointments in date range
            start_datetime = datetime.combine(start_date, time.min)
            end_datetime = datetime.combine(end_date, time.max)
            
            appointments = self.session.query(Appointment).filter(
                Appointment.appointment_date >= start_datetime,
                Appointment.appointment_date <= end_datetime
            ).all()
            
            if not appointments:
                print(f"\nNo appointments found between {start_str} and {end_str}")
                return
            
            print(f"\nAPPOINTMENTS BETWEEN {start_str} AND {end_str} ({len(appointments)} total)")
            print("-" * 100)
            print(f"{'Date':<12} {'Time':<10} {'Client':<20} {'Stylist':<20} {'Service':<20} {'Status':<12} {'Price':<10}")
            print("-" * 100)
            
            for app in sorted(appointments, key=lambda x: x.appointment_date):
                client_name = app.client.full_name if app.client else "N/A"
                stylist_name = app.stylist.full_name if app.stylist else "N/A"
                service_name = app.service.name if app.service else "N/A"
                print(f"{app.date_only:<12} {app.time_only:<10} {client_name:<20} {stylist_name:<20} {service_name:<20} {app.status:<12} ${app.total_price:<9.2f}")
                
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")
        except Exception as e:
            print(f"Error: {e}")
    
    def search_revenue_by_date(self):
        """Search revenue by date."""
        print("\nSEARCH REVENUE BY DATE")
        print("-" * 40)
        
        try:
            start_str = input("Start Date (YYYY-MM-DD): ").strip()
            end_str = input("End Date (YYYY-MM-DD): ").strip()
            
            if not start_str or not end_str:
                print("Both start and end dates are required.")
                return
            
            # Parse dates
            start_year, start_month, start_day = map(int, start_str.split('-'))
            end_year, end_month, end_day = map(int, end_str.split('-'))
            
            start_date = date(start_year, start_month, start_day)
            end_date = date(end_year, end_month, end_day)
            
            if start_date > end_date:
                print("Start date must be before end date.")
                return
            
            # Calculate total revenue for the period
            total_revenue = 0
            current_date = start_date
            daily_revenues = []
            
            while current_date <= end_date:
                daily_rev = Appointment.get_daily_revenue(self.session, current_date)
                total_revenue += daily_rev
                if daily_rev > 0:
                    daily_revenues.append((current_date, daily_rev))
                current_date += timedelta(days=1)
            
            print(f"\nREVENUE REPORT: {start_str} TO {end_str}")
            print("=" * 60)
            print(f"Total Revenue: ${total_revenue:.2f}")
            print(f"Days with Revenue: {len(daily_revenues)}")
            print(f"Days in Period: {(end_date - start_date).days + 1}")
            
            if daily_revenues:
                print(f"\nDaily Breakdown:")
                print("-" * 30)
                for day, rev in sorted(daily_revenues, key=lambda x: x[1], reverse=True):
                    print(f"  {day.strftime('%Y-%m-%d')}: ${rev:.2f}")
                    
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")
        except Exception as e:
            print(f"Error: {e}")
                        
def main():
    """Main function to run the CLI."""
    cli = SalonProCLI()
    cli.run()


if __name__ == "__main__":
    main()