import xmlrpc.client
import datetime
import random

servers = [
    xmlrpc.client.ServerProxy("http://localhost:8000"),
    xmlrpc.client.ServerProxy("http://localhost:8001"),
]

def get_server():
 
    return random.choice(servers)

def menu():
 
    while True:
        print("\n1. Add Note")
        print("2. Get Notes")
        print("3. Search Wikipedia")
        print("4. Exit")
        
        choice = input("Enter choice: ")
        server = get_server()  

        if choice == "1":
            topic = input("Enter topic: ")
            note_name = input("Enter note name: ")
            text = input("Enter note text: ")
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(server.add_note(topic, note_name, text, timestamp))
        
        elif choice == "2":
            topic = input("Enter topic to fetch: ")
            notes = server.get_notes(topic)
            if isinstance(notes, list):
                for note in notes:
                    print(note)
            else:
                print(notes)
        
        elif choice == "3":
            topic = input("Enter topic to search on Wikipedia: ")
            result = server.search_wikipedia(topic)
            title = result.get("title", "No result")
            link = result.get("link", "No result")

            print(f"Title: {title}")
            print(f"Link: {link}")

        elif choice == "4":
            break

menu()
