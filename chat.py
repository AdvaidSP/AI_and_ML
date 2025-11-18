import gradio
from groq import Groq
client = Groq(
    api_key="key",
)
def initialize_messages():
    return [{"role": "system",
             "content": """You are an AI stand-up comedian performing live on stage. 
            Your personality: witty, energetic, sharp, slightly sarcastic but never offensive. 
            Your style: quick punchlines, callbacks, crowd-work, observational humor, 
            and occasional self-deprecating jokes. 
            Make jokes about daily life, technology, relationships, awkward moments, 
            and unexpected twists. 
            Keep responses short, funny, spontaneous, and conversational—like you're on stage 
            talking to an audience. 
            Never be rude, dark, or insulting. Stay hilarious, light-hearted, and clever."""}]
messages_prmt = initialize_messages()
print(type(messages_prmt))
def customLLMBot(user_input, history):
    global messages_prmt

    messages_prmt.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        messages=messages_prmt,
        model="llama-3.3-70b-versatile",
    )
    print(response)
    LLM_reply = response.choices[0].message.content
    messages_prmt.append({"role": "assistant", "content": LLM_reply})

    return LLM_reply
iface = gradio.ChatInterface(customLLMBot,
                     chatbot=gradio.Chatbot(height=300),
                     textbox=gradio.Textbox(placeholder="Ask me a question related to technical interview"),
                     title="Standup Comedian ChatBot",
                     description="Chat bot for Standup Comedy",
                     theme="soft",
                     examples=["Hi"]
                     )
iface.launch(share=True)