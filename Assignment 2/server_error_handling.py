from xmlrpc.server import SimpleXMLRPCServer
import xml.etree.ElementTree as ET
import os
import datetime
import requests

XML_FILE = "notebook.xml"

class NotebookServer:
    def __init__(self):
  
        if not os.path.exists(XML_FILE) or not self._validate_xml():
            print("Notebook file missing or corrupted. Resetting...")
            root = ET.Element("data")  
            tree = ET.ElementTree(root)
            tree.write(XML_FILE)

    def _validate_xml(self):
 
        try:
            ET.parse(XML_FILE)
            return True
        except ET.ParseError:
            return False

    def add_note(self, topic, note_name, text, timestamp):
  
        tree = ET.parse(XML_FILE)
        root = tree.getroot()

        topic_element = None
        for t in root.findall("topic"):
            if t.get("name") == topic:
                topic_element = t
                break

        if topic_element is None:
            topic_element = ET.SubElement(root, "topic", name=topic)

        note_element = ET.SubElement(topic_element, "note", name=note_name)
        ET.SubElement(note_element, "text").text = text
        ET.SubElement(note_element, "timestamp").text = timestamp

        tree.write(XML_FILE)
        return f"Note added to {topic}!"

    def get_notes(self, topic):

        tree = ET.parse(XML_FILE)
        root = tree.getroot()

        for t in root.findall("topic"):
            if t.get("name") == topic:
                notes = []
                for note in t.findall("note"):
                    note_name = note.get("name")
                    text = note.find("text").text if note.find("text") is not None else "No text"
                    timestamp = note.find("timestamp").text if note.find("timestamp") is not None else "No timestamp"
                    notes.append(f"{note_name}: {text} ({timestamp})")
                return notes

        return "No notes found for this topic."

    def search_wikipedia(self, topic):

        try:
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic}"
            headers = {"User-Agent": "MyNotebookApp"}
            response = requests.get(url, headers=headers)
            response.raise_for_status() 

            data = response.json()
            if "content_urls" in data and "desktop" in data["content_urls"]:
                return {"title": data["title"], "link": data["content_urls"]["desktop"]["page"]}

            return {"error": "No results found"}
        except requests.exceptions.RequestException as e:
            return {"error": f"API request failed: {str(e)}"}

def start_server():

    while True:
        try:
            port = int(input("Enter server port (e.g., 8000, 8001): "))
            server = SimpleXMLRPCServer(("localhost", port), allow_none=True)
            notebook = NotebookServer()

            server.register_function(notebook.add_note, "add_note")
            server.register_function(notebook.get_notes, "get_notes")
            server.register_function(notebook.search_wikipedia, "search_wikipedia")

            print(f"Server started on port {port}...")
            server.serve_forever()
        except OSError:
            print("Port is already in use. Please enter a different port.")

if __name__ == "__main__":
    start_server()
