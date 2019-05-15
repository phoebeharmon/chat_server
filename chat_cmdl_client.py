
from voice_chat_client_class import *
import chat_client_class

def main():
    import argparse
    parser = argparse.ArgumentParser(description='chat client argument')
    parser.add_argument('-d', type=str, default=None, help='server IP addr')
    args = parser.parse_args()

    #get input
    choice = input("enter 1 for text-based chat system. enter 2 for voice-based chat system.")
    if choice == '1': #text
        client = chat_client_class.Client(args)
    elif choice == '2': #voice, *
        client = Client(args)


    #client = Client(args)
    client.run_chat()

main()
