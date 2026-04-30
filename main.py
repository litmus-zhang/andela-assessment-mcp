from dotenv import load_dotenv
load_dotenv()

from ui import create_ui

def main():
    print("Starting Meridian Electronics Support Chatbot...")
    demo = create_ui()
    demo.launch(debug=True)

if __name__ == "__main__":
    main()
