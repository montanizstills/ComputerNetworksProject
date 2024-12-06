from flask import Flask, request, render_template_string

app = Flask(__name__)

# Store chat messages in a global list (temporary storage for simplicity)

chat_messages = []

# HTML template for the chat room

HTML_TEMPLATE = """

<!DOCTYPE html>

<html>

<head>

    <title>Chat Room</title>

    <style>

        body {

            font-family: Arial, sans-serif;

            background-color: #f0f8ff; /* Light blue background */

            color: #333; /* Dark gray text */

            text-align: center;

            margin: 0;

            padding: 0;

        }

        h1 {

            color: #4CAF50; /* Green text for the title */

            margin-top: 20px;

        }

        form {

            margin: 20px auto;

            max-width: 400px;

            padding: 20px;

            background: #ffffff; /* White background for the form */

            border: 2px solid #007BFF; /* Blue border */

            border-radius: 10px;

            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Subtle shadow */

        }

        input {

            width: 90%;

            padding: 10px;

            margin: 10px 0;

            border: 1px solid #ccc;

            border-radius: 5px;

            box-sizing: border-box;

        }

        button {

            padding: 10px 20px;

            background-color: #007BFF; /* Blue button */

            color: #ffffff; /* White text */

            border: none;

            border-radius: 5px;

            cursor: pointer;

        }

        button:hover {

            background-color: #0056b3; /* Darker blue on hover */

        }

        #messages {

            margin-top: 20px;

            max-width: 400px;

            padding: 10px;

            background: #ffffff; /* White background for messages */

            border: 1px solid #ccc;

            border-radius: 5px;

            text-align: left;

            margin-left: auto;

            margin-right: auto;

            overflow-y: auto;

            max-height: 300px; /* Limit height for scrollable area */

            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Subtle shadow */

        }

        .message {

            margin: 5px 0;

            padding: 5px 10px;

            background: #f9f9f9; /* Light gray for message background */

            border-radius: 5px;

        }

        .message span {

            font-weight: bold;

            color: #007BFF; /* Blue for usernames */

        }

    </style>

</head>

<body>

    <h1>Welcome to Chat Room</h1>

    <form method="post" action="/send_message">

        <label for="username">Username:</label><br>

        <input type="text" id="username" name="username" placeholder="Enter your username" required><br><br>

        <label for="message">Message:</label><br>

        <input type="text" id="message" name="message" placeholder="Type your message" required><br><br>

        <button type="submit">Send</button>

    </form>

    <div id="messages">

        <h2>Conversation</h2>

        {% for message in messages %}

        <p class="message"><span>{{ message.username }}</span>: {{ message.text }}</p>

        {% endfor %}

    </div>

</body>

<script>

    // JavaScript for handling the form submission

        document.getElementById('Chat Room').addEventListener('submit', async function(event) {

            event.preventDefault(); // Prevent the form from submitting traditionally



            // Get form data

            const username = document.getElementById('username').value.trim();

            const message = document.getElementById('message').value.trim();


            // Check for empty inputs

            if (!username || !message) {

                alert('Both fields are required!');

                return;

            }

try {

                // Send the data to the server using fetch

                const response = await fetch('/', {

                    method: 'POST',

                    headers: {

                        'Content-Type': 'application/json'

                    },

                    body: JSON.stringify({ username, message })

                });

<script>

</html>

"""


@app.route('/')
def chat_room():
    # Render the HTML template with current chat messages

    return render_template_string(HTML_TEMPLATE, messages=chat_messages)


@app.route('/send_message', methods=['POST'])
def send_message():
    username = request.form['username']

    message = request.form['message']

    # Print the submitted message to the terminal

    print(f"New message from {username}: {message}")

    # Append the new message to the global chat_messages list

    chat_messages.append({'username': username, 'text': message})

    # Limit the conversation to the last 50 messages

    if len(chat_messages) > 50:
        chat_messages.pop(0)

    return render_template_string(HTML_TEMPLATE, messages=chat_messages)


if __name__ == '__main__':
    # Start the TCP server in a separate thread

    # threading.Thread(target=start_tcp_server, daemon=True).start()

    # Run the Flask application

    app.run(debug=True, host='localhost', port=1000)