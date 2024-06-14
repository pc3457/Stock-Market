import yfinance as yf
from flask import request, render_template, jsonify, Flask,redirect,url_for,session,Response,json
import boto3
import uuid
from flask_socketio import join_room, leave_room, send, SocketIO
import random
from string import ascii_uppercase
import pandas as pd
from kafka import KafkaProducer
from time import sleep
from json import dumps
import json


user_id=""
app = Flask(__name__, template_folder='templates')
socketio = SocketIO(app)
app.secret_key = 'abhishek2503'
# AWS S3 credentials
S3_BUCKET_NAME = 'stockmarketstorage'
aws_access_key_id = 'AKIA6ODVAVJ7XETNBL5R'
aws_secret_access_key = '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'
region_name='us-east-1'

# Initialize the S3 client
s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key,
                  region_name=region_name)






rooms = {}

def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        
        if code not in rooms:
            break
    
    return code

@app.route("/chat", methods=["POST", "GET"])
def home():
    user_id = request.args.get("user_id")
    if request.method == "POST":
        name = request.args.get("username")
        user_id= request.args.get("user_id")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if not name:
            return render_template("home.html", error="Please enter a name.", code=code, name=name,user_id=user_id)

        if join != False and not code:
            return render_template("home.html", error="Please enter a room code.", code=code, name=name,user_id=user_id)
        
        room = code
        if create != False:
            room = generate_unique_code(4)
            rooms[room] = {"members": 0, "messages": []}
        elif code not in rooms:
            return render_template("home.html", error="Room does not exist.", code=code, name=name,user_id=user_id)
        
        session["room"] = room
        session["name"] = name
        return redirect(url_for("room"))

    return render_template("home.html",user_id=user_id)

@app.route("/room")
def room():
    room = session.get("room")
    producer = KafkaProducer(bootstrap_servers=['35.174.111.213:9092'], #change ip here
                         value_serializer=lambda x: 
                         dumps(x).encode('utf-8'))
    

    return render_template("room.html", code=room, messages=rooms[room]["messages"])

@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return 
    
    content = {
        "name": session.get("name"),
        "message": data["data"]
    }
    send(content, to=room)
    producer.send('kafkastock', value=content)
    rooms[room]["messages"].append(content)
    print(f"{session.get('name')} said: {data['data']}")

@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return
    
    join_room(room)
    send({"name": name, "message": "has entered the room"}, to=room)
    producer.send({"name": name, "message": "has entered the room"})
    rooms[room]["members"] += 1
    print(f"{name} joined room {room}")

@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]
    
    send({"name": name, "message": "has left the room"}, to=room)
    producer.send({"name": name, "message": "has left the room"})
    print(f"{name} has left the room {room}")




@app.route('/signup', methods=['GET'])
def signup_page():
    return render_template('signup.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if username already exists
        if check_username_exists(username):
            return render_template('signup.html', error='Username already exists')

        # Example: Upload user data to S3 bucket
         # Initialize an empty portfolio for the new user
        empty_portfolio = []
        ticker_list=[]
        user_id = str(uuid.uuid4())  # Generate unique ID for user
        user_data = {'password': password, 'id': user_id}
        store_portfolio_data(username, empty_portfolio,ticker_list)
        s3_client.put_object(Bucket=S3_BUCKET_NAME, Key=f'users/{username}/User_Credentials', Body=str(user_data))

        # Redirect to login page after successful signup
        return redirect(url_for('login_page'))

    return render_template('signup.html')
    

@app.route('/login', methods=['GET'])
def page():
    return render_template('login.html')

@app.route('/logout/<user_id>', methods=['POST','GET'])
def logout(user_id):
    if request.method == 'POST':
        
        
        # Store user's portfolio data in the S3 bucket
        if 'username' in session:
            # Access the ticker list sent from the client
            tickers = request.json.get('tickers', [])
            ticker_list=tickers
            # Perform any necessary operations with the ticker list
            username = session['username']
            portfolio_data = session['portfolio_data']
            store_portfolio_data(username, portfolio_data,ticker_list)
        
        # Clear the session
        session.clear()
        
        # Return a response, such as a redirect or JSON response
        return redirect(url_for('login_page'))
    
    elif request.method == 'GET':
        # Handle GET request separately, if needed
        return redirect(url_for('login_page'))

    
@app.route('/check_login_credentials', methods=['POST'])
def check_login_credentials():
    # Get the username and password from the form data
    username = request.form['username']
    password = request.form['password']
    
    # Retrieve user data from the S3 bucket
    user_data = get_user_data(username)

    # Check if the password matches the stored password
    if user_data and user_data.get('password') == password:
        
        portfolio_data = get_portfolio_data(username)[0]
        ticker_list=get_portfolio_data(username)[1]
        # If the password is correct, create a session for the user
        session['user_id'] = user_data.get('id')
        session['username']=username
        session['portfolio_data'] = portfolio_data
        session['ticker_list']=ticker_list
        user_id=user_data.get('id')
        # Return a success response with a redirect URL to the dashboard
        redirect_url = url_for('index', user_id=user_id)


        # Return a JSON response with the redirection URL and a status code 200
        #return jsonify({'redirect_url': redirect_url}), 200
        return jsonify({'redirect_url': redirect_url, 'portfolio_data': portfolio_data, 'ticker_list': ticker_list,'user_id':user_id}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 403

def get_portfolio_data(username):
    try:
        response = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=f'users/{username}/{username}_portfolio.json')
        portfolio_data_json = response['Body'].read().decode()
        portfolio_data = json.loads(portfolio_data_json)['portfolio_data']
        ticker_list=json.loads(portfolio_data_json)['ticker_list']
        return (portfolio_data,ticker_list)
    except s3_client.exceptions.NoSuchKey:
        return []  # Return empty list if portfolio data doesn't exist


def store_portfolio_data(username, portfolio_data,ticker_list):
    # Prepare the data to be stored in S3
    data_to_store = {
        'portfolio_data': portfolio_data,
        'ticker_list':ticker_list
    }
    
    # Convert data to JSON string
    data_json = json.dumps(data_to_store)
    
    # Upload data to S3 bucket
    s3_client.put_object(Bucket=S3_BUCKET_NAME, Key=f'users/{username}/{username}_portfolio.json', Body=data_json)


def check_username_exists(username):
    # Check if username already exists in S3 bucket
    try:
        s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=f'users/{username}/User_Credentials')
        return True
    except s3_client.exceptions.NoSuchKey:
        return False


def get_user_data(username):
    # Retrieve user data from S3 bucket
    try:
        response = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=f'users/{username}/User_Credentials')
        user_data = response['Body'].read().decode()
        return eval(user_data)  # Convert string to dictionary
    except s3_client.exceptions.NoSuchKey:
        return None


@app.route('/')
def login_page():
    return render_template('login.html')




@app.route('/dashboard/<user_id>',methods=['GET'])
def index(user_id):
    # Get the username from the session
    username = None
    if 'user_id' in session:
        user_id = session['user_id']
        username=session['username']
        ticker_list=session['ticker_list']
        

    # Render the dashboard template with the username
    return render_template('index.html', username=username,ticker_list=ticker_list,user_id=user_id)





@app.route('/<user_id>/sell/<ticker>', methods=['GET'])
def Sell_Stock(ticker,user_id):
    stock = yf.Ticker(ticker)
    
    try:
        data = stock.history(period='1d')
        if data.empty:
            raise ValueError("No data available for the specified ticker: " + ticker)

        current_price = data['Close'].iloc[-1] if 'Close' in data else 'N/A'
        open_price = data['Open'].iloc[-1] if 'Open' in data else 'N/A'
        previous_close = data['Close'].iloc[-1] if 'Close' in data else 'N/A'

        info = stock.info
        context = {
            'ticker': ticker.upper(),
            'currentPrice': current_price,
            'openPrice': open_price,
            'previousClose': previous_close,
            'marketCap': info.get('marketCap', 'N/A'),
            'logo_url': info.get('logo_url', '/static/default-logo.png'),
            'companyName': info.get('shortName', ticker),
            'sector': info.get('sector', 'N/A'),
        }

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify(context)  # Return JSON if it's an AJAX request

         
        return render_template('Sell_Stock.html', **context,user_id=user_id)

    except ValueError as ve:
        print(f"ValueError: {ve}")
        return render_template('error.html', error=str(ve))
    except Exception as e:
        print(f"Unexpected error: {e}")
        return render_template('error.html', error="An unexpected error occurred, please try again later.")

@app.route('/<user_id>/buy/<ticker>', methods=['GET'])
def Buy_Stock(ticker,user_id):
    stock = yf.Ticker(ticker)
    try:
        data = stock.history(period='1d')
        if data.empty:
            raise ValueError("No data available for the specified ticker: " + ticker)

        current_price = data['Close'].iloc[-1] if 'Close' in data else 'N/A'
        open_price = data['Open'].iloc[-1] if 'Open' in data else 'N/A'
        previous_close = data['Close'].iloc[-1] if 'Close' in data else 'N/A'
        print(current_price)
        info = stock.info
        context = {
            'ticker': ticker.upper(),
            'currentPrice': current_price,
            'openPrice': open_price,
            'previousClose': previous_close,
            'marketCap': info.get('marketCap', 'N/A'),
            'logo_url': info.get('logo_url', '/static/default-logo.png'),
            'companyName': info.get('shortName', ticker),
            'sector': info.get('sector', 'N/A'),
        }
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify(context)  # Return JSON if it's an AJAX request

         # Assuming you have a template named 'buy.html' in your 'templates' folder
        return render_template('Buy_Stock.html', **context,user_id=user_id)

    except ValueError as ve:
        print(f"ValueError: {ve}")
        return render_template('error.html', error=str(ve))
    except Exception as e:
        print(f"Unexpected error: {e}")
        return render_template('error.html', error="An unexpected error occurred, please try again later.")

@app.route('/add_to_portfolio/<user_id>', methods=['POST'])
def add_to_portfolio(user_id):
    if request.method == 'POST':
        ticker = request.form['ticker']
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])
        # Retrieve portfolio data from the session
        portfolio_data = session.get('portfolio_data', [])
    # Check if the stock already exists in the portfolio
    stock_exists = False
    for stock in portfolio_data:
        if stock['ticker'] == ticker:
            stock_exists = True
            prev_quantity = stock['quantity']
            stock['quantity'] += quantity
            stock['average_price'] = round((prev_quantity * stock['average_price'] + quantity * price) / stock['quantity'],2)
            val=price * quantity
            stock['Cost_Basis'] += round(val,2)
            break

    # If the stock doesn't exist, add it to the portfolio
    if not stock_exists:
        val=price * quantity
        portfolio_data.append({
            'ticker': ticker,
            'quantity': quantity,
            'Cost_Basis': round(val,2),
            'average_price': round(price,2)
        })
    session['portfolio_data'] = portfolio_data
    # Redirect back to the portfolio page after adding the stock
    return redirect(url_for('portfolio',user_id=user_id))

@app.route('/remove_from_portfolio/<user_id>', methods=['POST'])
def remove_from_portfolio(user_id):
    if request.method == 'POST':
        ticker = request.form['ticker']
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])
        portfolio_data = session.get('portfolio_data', [])
        
        # Check if the stock exists in the portfolio
        stock_index = None
        for i, stock in enumerate(portfolio_data):
            if stock['ticker'] == ticker:
                stock_index = i
                break
        
        if stock_index is None:
            return "Cannot execute sell order: Stock is not in the portfolio"
        
        # Check if the quantity to sell is greater than available quantity
        if quantity > portfolio_data[stock_index]['quantity']:
            return "Cannot execute sell order: Quantity to sell exceeds available quantity"
        
        # If the quantity to sell matches the available quantity, delete the item from the table
        if quantity == portfolio_data[stock_index]['quantity']:
            del portfolio_data[stock_index]
        else:
            # Reduce the quantity and update the average price
            prev_quantity = portfolio_data[stock_index]['quantity']
            portfolio_data[stock_index]['quantity'] -= quantity
            portfolio_data[stock_index]['average_price'] = round(((prev_quantity * portfolio_data[stock_index]['average_price']) - (quantity * price)) / portfolio_data[stock_index]['quantity'], 2)
            portfolio_data[stock_index]['Cost_Basis'] = round(portfolio_data[stock_index]['Cost_Basis'] - (price * quantity), 2)
        
    # Redirect back to the portfolio page after selling the stock
    session['portfolio_data'] = portfolio_data
    return redirect(url_for('portfolio',user_id=user_id))


@app.route('/portfolio/<user_id>')
def portfolio(user_id):
  
    return render_template('portfolio.html', portfolio_data=session['portfolio_data'],user_id=user_id)
    #return portfolio_data
@app.route('/get_stock_data/<user_id>', methods=['POST'])
def get_stock_data(user_id):
    data = request.get_json()
    ticker = data.get('ticker')
    if ticker:  # Ensure that ticker is not an empty string
        stock = yf.Ticker(ticker)
        try:
            # Fetch data, if available
            data = stock.history(period='1y')
            if data.empty:
                raise ValueError('No data available for this ticker.')
            
            # Send the response with the needed data
            return jsonify({
                'currentPrice': data.iloc[-1].Close,
                'openPrice': data.iloc[-1].Open
            })
        except Exception as e:
            # Log the error and send a response indicating failure
            print(f"Error fetching data for {ticker}: {e}")
            response = jsonify({
                'error': 'Could not retrieve stock data.',
                'details': str(e)
            })
            response.status_code = 500
            return response
    else:
        # Handle the case where no ticker is provided
        return jsonify({'error': 'No ticker symbol provided'}), 400

@app.route('/<user_id>/stock/<ticker>', methods=['GET'])
def stock_detail(ticker,user_id):
    stock = yf.Ticker(ticker)
    
    try:
        data = stock.history(period='1d')
        if data.empty:
            raise ValueError("No data available for the specified ticker: " + ticker)

        current_price = data['Close'].iloc[-1] if 'Close' in data else 'N/A'
        open_price = data['Open'].iloc[-1] if 'Open' in data else 'N/A'
        previous_close = data['Close'].iloc[-1] if 'Close' in data else 'N/A'
        print(current_price)
        info = stock.info
        context = {
            'ticker': ticker.upper(),
            'currentPrice': current_price,
            'openPrice': open_price,
            'previousClose': previous_close,
            'marketCap': info.get('marketCap', 'N/A'),
            'logo_url': info.get('logo_url', '/static/default-logo.png'),
            'companyName': info.get('shortName', ticker),
            'sector': info.get('sector', 'N/A'),
        }

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify(context)  # Return JSON if it's an AJAX request

        return render_template('stock_detail.html', **context,user_id=user_id)

    except ValueError as ve:
        print(f"ValueError: {ve}")
        return render_template('error.html', error=str(ve))
    except Exception as e:
        print(f"Unexpected error: {e}")
        return render_template('error.html', error="An unexpected error occurred, please try again later.")




if __name__ == '__main__':
    socketio.run(app, debug=True)
