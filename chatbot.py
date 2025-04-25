import google.generativeai as genai
import os
import textwrap
from IPython.display import display, Markdown 

try:
  
    from google.colab import userdata
    GOOGLE_API_KEY = userdata.get('GOOGLE_API_KEY')
    if not GOOGLE_API_KEY:
        raise ValueError("API Key not found in Colab Secrets")
    genai.configure(api_key=GOOGLE_API_KEY)
    print("API Key configured successfully using Colab Secrets.")
except (ImportError, ValueError, Exception) as e:
    print(f"Could not get API Key from Colab Secrets: {e}")
  
    print("\nWARNING: Storing API keys directly in code is insecure.")
    print("Consider using Colab Secrets (View -> Secrets) for better security.")
    GOOGLE_API_KEY = input("Please enter your Google API Key: ")
    if not GOOGLE_API_KEY:
        print("API Key not provided. Exiting.")
        
    else:
        genai.configure(api_key=GOOGLE_API_KEY)
        print("API Key configured manually.")


def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


customer_service_rules = {
    ("hello", "hi", "hey", "greetings"): "Hello! Welcome to our customer service chat. How can I help you today?",
    ("hours", "open", "business hours"): "Our business hours are Monday to Friday, 9:00 AM to 5:00 PM Eastern Time.",
    ("contact", "phone", "email", "call us"): "You can reach us by phone at 1-800-123-4567 or email us at support@example-store.com.",
    ("return policy", "refund policy", "send back"): "Our return policy allows returns within 30 days of purchase with the original receipt. Items must be unused and in original packaging. For more details, visit example-store.com/returns.",
    ("track order", "order status", "where is my order"): "To track your order, please provide your order number, and I can look it up for you. Alternatively, you can use the tracking link sent to your email.",
    ("shipping cost", "delivery fee"): "Standard shipping within the US is $5.99. Orders over $50 qualify for free standard shipping.",
    ("product info", "item details"): "Could you please specify which product you're interested in? I can provide details if you give me the product name or ID.",
    ("thank you", "thanks", "appreciate it"): "You're welcome! Is there anything else I can assist you with today?",
    ("bye", "goodbye", "exit", "quit"): "Thank you for contacting us. Have a great day!" 
}


model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',

    system_instruction="You are a friendly and helpful customer service assistant for 'My Awesome Store'. Answer customer questions politely and concisely. If a question is outside your scope or you don't know the answer, clearly state that you cannot help with that specific request and suggest contacting a human agent via support@example-store.com.",
    )

chat = model.start_chat(history=[]) 



print("🤖 Chatbot: Hello! I'm the customer service bot for 'My Awesome Store'. How can I help you?")
print("🤖 Chatbot: Type 'quit' or 'bye' to end the chat.")

while True:
    try:
    
        user_input = input("👤 You: ")
        user_input_lower = user_input.lower().strip() 

        if user_input_lower in ["quit", "exit", "bye", "goodbye"]:
            print("🤖 Chatbot: Thank you for contacting us. Have a great day!")
            break

        responded = False
        for keywords, response in customer_service_rules.items():
         
            if any(keyword in user_input_lower for keyword in keywords):
                display(to_markdown(f"🤖 Chatbot: {response}"))
                responded = True
                break 


        if not responded:
           
            print("🤖 Chatbot: Thinking...") 
            try:
                gemini_response = chat.send_message(user_input)
             
                display(to_markdown(f"🤖 Chatbot: {gemini_response.text}"))
            except Exception as e:
              
                print(f"\n🤖 Chatbot: Sorry, I encountered an error trying to understand that. Error: {e}")
                print("🤖 Chatbot: Could you please rephrase your question or try again later?")

    except KeyboardInterrupt:
      
        print("\n🤖 Chatbot: Goodbye!")
        break
    except Exception as e:
     
        print(f"\nAn unexpected error occurred: {e}")
        print("🤖 Chatbot: I seem to be having trouble. Please try restarting the chat.")
        break

print("\n--- Chat Session Ended ---")
