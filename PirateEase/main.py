from chatbot import ChatBot
from PirateEase.Utils.slow_print import slow_print

if __name__ == '__main__':
    chatbot: ChatBot = ChatBot()
    print('PirateEase: Hello! Welcome to the PirateEase support bot!')
    print('PirateEase: You can ask me about the status of your order, '
          'have me refund a purchase, have me check the availability of a product, or I can connect you with one of our '
          'live agents.')
    user_input: str = ''
    response: str = ''
    while not chatbot.should_disconnect(response + user_input):
        user_input= input('User: ')
        response = chatbot.process_query(user_input)
        slow_print(f'PirateEase: {response}')