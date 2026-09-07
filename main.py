from modules.web_recon import web_menu
def show_banner():
    print("="*50)
    print("Arpit-recon")
    print(" Recon • DFIR • Intelligence • Reporting")
    print("="*50)
def show_menu():
    print("\nSelect an option:")
    print("1. Recon")
    print("2. DFIR")
    print("3. Intelligence")
    print("4. Reporting")
    print("5. Exit")
def main():
    show_menu()
    choice = input("Enter your choice: ")
    if choice == '1':
        print("You selected Recon.")
        # Add Recon functionality here
    elif choice == '2':
        print("You selected DFIR.")
        # Add DFIR functionality here
    elif choice == '3':
        print("You selected Intelligence.")
        web_menu()  #!Call the web_menu function from web_recon.py
    elif choice == '4':
        print("You selected Reporting.")
        # Add Reporting functionality here
    elif choice == '5':
        print("Exiting the program.")
        exit()
    else:
        print("Invalid choice. Please try again.")
        main()  # Call main again for a new input 
if __name__ == "__main__":
    show_banner()
    main()