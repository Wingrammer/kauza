import streamlit as st
import requests
import base64
import uuid


# Define the URL of your logo image
logo_url = "https://ksysmoixgyrwexukfifh.supabase.co/storage/v1/object/sign/kauza/logo.png?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJrYXV6YS9sb2dvLnBuZyIsImlhdCI6MTcxODI2NjkxOSwiZXhwIjoxNzIwODU4OTE5fQ.9lhDbWO_1mDCVhxXKQjfd8BuBBRqpcGj05XVh8CZbn8&t=2024-06-13T08%3A21%3A51.191Z"

# Add a logo and title in the header
st.markdown(
    f"""
    <div style="position: fixed; top: 0; left: 0; right: 0; display: flex; align-items: center; justify-content: center; height: 80px; z-index: 1000;">
        <img src="{logo_url}" alt="Logo" style="height: 60px; margin-right: 10px;">
        <h1 style="margin: 0; font-size: 24px;">Chat with Kauza bots here</h1>
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

# Add custom CSS for button styles and positioning the input box and send button at the bottom
st.markdown(
    """
    <style>
    .stButton button {
        background-color: #1044a4 !important;  /* Blue background */
        color: white !important;  /* White text */
        border: 2px solid #1044a4 !important;  /* Blue border */
        margin: 5px !important;  /* Add margin to buttons */
        width: calc(100% - 20px);  /* Adjust width of buttons */
        text-align: center;  /* Center text in buttons */
    }
    .stButton button:hover {
        background-color: #0056b3 !important;  /* Darker blue on hover */
        border: 2px solid #1044a4 !important;  /* Darker blue border on hover */
    }
    .chat-container {
        position: fixed;
        top: 80px; /* Height of the header */
        bottom: 50px; /* Height of the input box */
        left: 0;
        right: 0;
        overflow-y: auto; /* Enable vertical scroll */
        padding: 10px;
    }
    .chat-message {
        display: flex;
        margin-bottom: 10px;
    }
    .chat-message.user {
        justify-content: flex-end;
    }
    .chat-message.user .chat-bubble {
        
    }
    .chat-message.bot .chat-bubble {
        
    }
    .chat-bubble {
        max-width: 70%; /* Limit max-width of chat bubbles */
        padding: 10px;
        border-radius: 10px;
    }
    .chat-message.user .chat-bubble {
        float: right; /* Float user messages to the right */
    }
    .chat-message.bot .chat-bubble {
        float: left; /* Float bot messages to the left */
    }
    .input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        display: flex;
        align-items: center;
        
        padding: 10px;
        border-top: 1px solid #ddd;
    }
    .input-container input {
        flex: 1;
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 5px;
        margin-right: 10px;
    }
    .input-container button {
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        
        color: white;
        cursor: pointer;
    }
    .input-container button:hover {
        
    }
    </style>
    """,
    unsafe_allow_html=True
)

if tenant_id and agent_id:
    
    # Display the chat history
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    # Function to handle and display response elements
    def display_response(response):
        if "text" in response:
            st.markdown(f"""
            <div class="chat-message bot">
                <div class="chat-bubble">{response["text"]}</div>
            </div>
            """, unsafe_allow_html=True)
        if "buttons" in response:
            button_html = '<div style="display: flex; justify-content: space-around;">'
            for button in response["buttons"]:
                button_html += f'<button onclick="sendMessage(\'{button["payload"]}\')">{button["title"]}</button>'
            button_html += '</div>'
            st.markdown(button_html, unsafe_allow_html=True)
        if "image" in response:
            st.image(response["image"])
        if "custom" in response:
            st.json(response["custom"])
            if "document" in response["custom"]:
                st.markdown(f"""
            <div class="chat-message bot">
                <img src="https://www.pikpng.com/pngl/m/490-4906657_emma-mobile-screen-chatbot-image-transparent-clipart.png" alt="Bot Icon">
                <div>{response["custom"]["document"]["link"]}</div>
            </div>
            """, unsafe_allow_html=True)

    # Handle displaying messages and buttons in chat history
    for chat in st.session_state['chat_history']:
        if isinstance(chat, str):
            st.markdown(f"""
            <div class="chat-message user">
                <div class="chat-bubble" style="">{chat}</div>
            </div>
            """, unsafe_allow_html=True)
        elif isinstance(chat, dict):
            display_response(chat)

    # Input field for the user to enter their message
    st.markdown('<div class="chat-container" id="chat-container"></div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="input-container">
            <input id="user_input" type="text" placeholder="Type your message here...">
            <button onclick="sendMessage()">Send</button>
        </div>
        <script>
        function sendMessage(payload) {
            var user_input = document.getElementById("user_input").value;
            if (payload) {
                user_input = payload;  // Use payload if provided (for buttons)
            }
            if (user_input) {
                var chat_container = document.getElementById("chat-container");
                var user_message_html = '<div class="chat-message user"><div class="chat-bubble" style="">' + user_input + '</div></div>';
                chat_container.innerHTML += user_message_html;
                document.getElementById("user_input").value = "";
                st.sessionState.syncSession = "true"
                st.sessionState = syncSess
            }
        }
        </script>
        """,
        unsafe_allow_html=True
    )

    # Input field for the user to enter their message
    user_message = st.text_input("You: ", "")

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

    # If the user enters a message, send it to the kauza server and display the response
    if st.button("Send") and user_message:
        st.session_state['chat_history'].append(user_message)
        responses = send_message_to_kauza(user_message)
        
        if responses:
            for response in responses:
                st.session_state['chat_history'].append(response)
        
        st.rerun()

else:
    st.write("Please provide bot's id as URL parameters to start the chat. Example: `?bot=something`")
