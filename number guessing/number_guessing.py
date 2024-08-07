from flask import Flask, render_template_string, request, session
from random import randint

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/', methods=['GET', 'POST'])
def home():
    if 'random_number' not in session:
        session['random_number'] = randint(1, 10)
        session['attempts'] = 0

    random_number = session['random_number']
    message = ''
    user_guess = ''

    if request.method == 'POST':
        try:
            user_guess = int(request.form['guess'])
            session['attempts'] += 1

            if user_guess > random_number:
                message = 'The number is lower'
            elif user_guess < random_number:
                message = 'The number is higher'
            else:
                message = f'You guessed it in {session["attempts"]} attempts!'
                session.pop('random_number', None)  # Reset the game
                session.pop('attempts', None)
        except ValueError:
            message = 'Please enter a valid number.'

    return render_template_string('''
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Number Guessing Game</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background: linear-gradient(120deg, #a1c4fd, #c2e9fb, #fbc2eb, #a6c1ee, #ff9a9e, #ffdde1);
                    background-size: 400% 400%;
                    animation: gradient 15s ease infinite;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    perspective: 1000px;
                }
                @keyframes gradient {
                    0% { background-position: 0% 50%; }
                    50% { background-position: 100% 50%; }
                    100% { background-position: 0% 50%; }
                }
                .container {
                    background: white;
                    padding: 30px;
                    border-radius: 15px;
                    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
                    text-align: center;
                    transform: rotateY(15deg);
                    transition: transform 0.5s, box-shadow 0.5s;
                }
                .container:hover {
                    transform: rotateY(0deg);
                    box-shadow: 0 30px 60px rgba(0, 0, 0, 0.3);
                }
                h1 {
                    color: #333;
                    font-size: 2em;
                    margin-bottom: 20px;
                    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
                }
                p {
                    color: #666;
                    font-size: 1.2em;
                    margin-bottom: 20px;
                }
                input[type="number"], input[type="submit"] {
                    padding: 10px;
                    margin: 5px 0;
                    font-size: 1em;
                    border-radius: 5px;
                    border: none;
                    box-shadow: 0 5px 10px rgba(0, 0, 0, 0.1);
                    transition: transform 0.3s, box-shadow 0.3s;
                }
                input[type="number"]:focus, input[type="submit"]:hover {
                    transform: scale(1.1);
                    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
                }
                input[type="submit"] {
                    background: linear-gradient(to right, #ff6f61, #de6262);
                    color: white;
                    cursor: pointer;
                }
                input[type="submit"]:hover {
                    background: linear-gradient(to right, #de6262, #ff6f61);
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Guess the Number</h1>
                <p>Guess the number in the range from 1 to 10.</p>
                <form method="post">
                    <input type="number" name="guess" min="1" max="10" required>
                    <input type="submit" value="Guess">
                </form>
                <p>{{ message }}</p>
            </div>
        </body>
        </html>
    ''', message=message)

if __name__ == '__main__':
    app.run(debug=True)