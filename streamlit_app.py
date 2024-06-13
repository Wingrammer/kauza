import streamlit as st
import requests
import base64
import uuid


# Define the URL of your logo image
# jack
logo_url = "https://ksysmoixgyrwexukfifh.supabase.co/storage/v1/object/sign/kauza/logo.png?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJrYXV6YS9sb2dvLnBuZyIsImlhdCI6MTcxODI2NjkxOSwiZXhwIjoxNzIwODU4OTE5fQ.9lhDbWO_1mDCVhxXKQjfd8BuBBRqpcGj05XVh8CZbn8&t=2024-06-13T08%3A21%3A51.191Z"  # Replace with your logo URL

# Add a logo and title in the header
# jack
# hide_github_icon = """
# #GithubIcon {
#   visibility: hidden;
# }
# """
# st.markdown(hide_github_icon, unsafe_allow_html=True)

st.markdown(
    f"""
    <div style="display: flex; align-items: center;">
        <img src="{logo_url}" alt="Logo" style="height: 60px; margin-right: 10px;">
        <h1 style="margin: 0;">Chat with Kauza bots here</h1>
    </div>
    """,
    unsafe_allow_html=True
)


# Retrieve URL parameters
query_params = st.query_params
bot_id = query_params.get("bot", "ZGJiZjQ4ZWQtM2I2ZC00YTIwLWEwOTEtNjA2ZDBiZDZhNDcwLTY1ZTllZjBkN2FlOGNlMDhlMDcxYjRlMg")
decoded_data = base64.b64decode(bot_id+'==').decode()
parts = decoded_data.split('-')
agent_id = parts.pop()
tenant_id = "-".join(parts)

# Generate a unique session_id for each user session
if 'session_id' not in st.session_state:
    st.session_state['session_id'] = str(uuid.uuid4())

session_id = st.session_state['session_id']

# Display the retrieved tenant_id and agent_id
# st.write(f"Tenant ID: {tenant_id}")
# st.write(f"Agent ID: {agent_id}")
# Add custom CSS for button styles
# Jack, le bleu de Kauza
st.markdown(
    """
    <style>
    .stButton button {
        background-color: #1044a4 !important;  /* Blue background */
        color: white !important;  /* White text */
        border: 2px solid #1044a4 !important;  /* Blue border */
    }
    .stButton button:hover {
        background-color: #0056b3 !important;  /* Darker blue on hover */
        border: 2px solid #1044a4 !important;  /* Darker blue border on hover */
    }
    .chat-message {
        display: flex;
        align-items: center;
        margin: 5px 0;
    }
    .chat-message img {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        margin-right: 10px;
    }
    .chat-message div {
       
        padding: 10px;
        border-radius: 5px;
    }
    .chat-message.bot div {
        
        color: white;
    }
    #GithubIcon {
        visibility: hidden;
    }
    #MainMenu {
    visibility: hidden;
    }
    header {
    visibility: hidden;
    display: none;
    }

    </style>
    """,
    unsafe_allow_html=True
)

if tenant_id and agent_id:
    
    # Display the chat history
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    # Function to send message to kauza server
    def send_message_to_kauza(message):
        url = f"http://kauza.serveo.net/webhooks/rest/webhook/{tenant_id}/agents/{agent_id}"
        payload = {
            "sender": session_id,
            "message": message
        }
        response = requests.post(url, json=payload)
        print(response.json())
        return response.json() if response.status_code == 200 else None

    # If the user enters a message, send it to the kauza server and # Function to handle and display response elements
    def display_response(response):
        if "text" in response:
            st.markdown(f"""
            <div class="chat-message bot">
                <img src="https://www.pikpng.com/pngl/m/490-4906657_emma-mobile-screen-chatbot-image-transparent-clipart.png" alt="Bot Icon">
                <div>{response["text"]}</div>
            </div>
            """, unsafe_allow_html=True)
        if "buttons" in response:
            for button in response["buttons"]:
                if st.button(button["title"]):
                    st.session_state['chat_history'].append(button["title"])
                    responses = send_message_to_kauza(button["payload"])
                    if responses:
                        for res in responses:
                            st.session_state['chat_history'].append(res)
                    st.rerun()
        if "image" in response:
            st.image(response["image"])
        if "custom" in response:
            st.json(response["custom"])
            if "document" in response["custom"]:
                st.markdown(f"""
            <a href="{response["custom"]["document"]["link"]}" download>
             <div class="message-document">
                <span>Document</span>
                <span>Sans titre</span>
             </div>
            </a>
           
            """, unsafe_allow_html=True)
            if "location" in response["custom"]:
                st.markdown(f"""
                <a href="https://google.com/maps/search/SIA+2024/@{response["custom"]["location"]["name"]},6.128463,17z?hl=fr&entry=ttu" download>
                <div class="message-document">
                    <span>{response["custom"]["location"]["name"]}</span>
                    <span>{response["custom"]["location"]["address"]}</span>
                </div>
                </a>
            
                """, unsafe_allow_html=True)
                

    # Handle displaying messages and buttons in chat history
    for chat in st.session_state['chat_history']:
        if isinstance(chat, str):
            st.markdown(f"""
            <div class="chat-message user">
                <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTBc-AEj_9MJQIUQqlgB0a9Nao0kuhi4ydeyQ&s" alt="User Icon">
                <div>{chat}</div>
            </div>
            """, unsafe_allow_html=True)
        elif isinstance(chat, dict):
            display_response(chat)

    
    # Input field for the user to enter their message
    user_message = st.text_input("You: ", "")

    
    
    # If the user enters a message, send it to the kauza server and display the response
    if st.button("Send") and user_message:
        st.session_state['chat_history'].append(f"{user_message}")
        responses = send_message_to_kauza(user_message)
        
        if responses:
            for response in responses:
                # display_response(response)
                st.session_state['chat_history'].append(response)
        
        st.rerun()
    # if st.document("Send") and user_message:
    #     responses = send_message_to_kauza(user_message)
        
    #     if responses:
    #         for response in responses:
    #             display_response(response)
        
    #     st.session_state['chat_history'].append(f"You: {user_message}")
    #     st.rerun()
else:
    st.write("Please provide bot's id as URL parameters to start the chat. Example: `?bot=something`")
