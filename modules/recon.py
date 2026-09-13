def recon_menu():

    while True:

        print("\n========================")
        print("Recon")
        print("========================")
        print("1. Host Discovery")
        print("2. Port Scanner")
        print("3. Service Detection")
        print("4. Banner Grab")
        print("5. Back")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            print("Host Discovery")

        elif choice == "2":
            print("Port Scanner")

        elif choice == "3":
            print("Service Detection")

        elif choice == "4":
            print("Banner Grab")

        elif choice == "5":
            break

        else:
            print("Invalid choice!")