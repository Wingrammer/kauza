import streamlit as st
import requests
import base64

# Title of the app
st.title("Chat with Kauza Bots")

# Retrieve URL parameters
query_params = st.query_params
bot_id = query_params.get("bot", "ZGJiZjQ4ZWQtM2I2ZC00YTIwLWEwOTEtNjA2ZDBiZDZhNDcwLTY1ZTllZjBkN2FlOGNlMDhlMDcxYjRlMg==")
decoded_data = base64.b64decode(bot_id).decode()
parts = decoded_data.split('-')
agent_id = parts.pop()
tenant_id = "-".join(parts)

# Display the retrieved tenant_id and agent_id
st.write(f"Tenant ID: {tenant_id}")
st.write(f"Agent ID: {agent_id}")

if tenant_id and agent_id:
    # Input field for the user to enter their message
    user_message = st.text_input("You: ", "")

    # Display the chat history
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    for chat in st.session_state['chat_history']:
        st.write(chat)

    # If the user enters a message, send it to the Rasa server and display the response
    if st.button("Send") and user_message:
        sender_id = "test_user"  # You can set this to a unique ID for each user

        # Define the URL of your custom Rasa REST endpoint
        url = f"http://kauza.serveo.net/webhooks/rest/webhook/{tenant_id}/agents/{agent_id}"
        
        payload = {
            "sender": sender_id,
            "message": user_message
        }
        
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            responses = response.json()
            bot_responses = [r['text'] for r in responses if 'text' in r]
            for bot_response in bot_responses:
                st.session_state['chat_history'].append(f"Bot: {bot_response}")
        else:
            st.write("Error: Could not reach the Rasa server.")
        
        st.session_state['chat_history'].append(f"You: {user_message}")
        st.experimental_rerun()  # Rerun to update the chat history
else:
    st.write("Please provide both Tenant ID and Agent ID as URL parameters to start the chat. Example: `?tenant_id=your_tenant_id&agent_id=your_agent_id`")
