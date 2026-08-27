def web_menu():

    while True:

        print("\n========================")
        print("Web Intelligence")
        print("========================")
        print("1. HTTP Analysis")
        print("2. DNS Intelligence")
        print("3. TLS Analysis")
        print("4. Technology Detection")
        print("5. Subdomain Enumeration")
        print("6. Back")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            print("HTTP Analysis")

        elif choice == "2":
            print("DNS Intelligence")

        elif choice == "3":
            print("TLS Analysis")

        elif choice == "4":
            print("Technology Detection")

        elif choice == "5":
            print("Subdomain Enumeration")

        elif choice == "6":
            break

        else:
            print("Invalid choice!")