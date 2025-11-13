........................................................ Hi, this is Sudhanshu Gautam ..............................................................
1. Install Dependencies:

    Run these commands in your terminal:

        pip install selenium
        pip install pymongo
        pip install flask

2. Start MongoDB by running mongod in a terminal.

3. Update app.py:

        Update the credentials in the script:

                username_field.send_keys("your_username")               in app.py file    LINE - 53
                email_field.send_keys("your_email")                     in app.py file    LINE - 64
                password_field.send_keys("your_password")               in app.py file    LINE - 74

4. Run Flask App:

    Start Flask by running:
                        python app.py

5. Visit http://127.0.0.1:5000/ to interact with the page.
