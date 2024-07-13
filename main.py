from flask import Flask, render_template, request,jsonify
import requests
import json
import smtplib
from email.mime.text import MIMEText
posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()
OWN_EMAIL = 'Your Email'
OWN_PASSWORD = "YOUR CODE PASSWORD"
app = Flask(__name__)


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/form-entry",methods=['GET', 'POST'])
def receive_data():
    if request.method == "POST":
        username = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']
        data = {
                'username': username,
                'email': email,
                'phone': phone,
                'message': message
            }
        json_data = json.dumps(data, indent=4)
        
        # Save the JSON data to a file
        with open('data.json', 'w') as json_file:
            json_file.write(json_data)
        
        # Print the JSON data to the console
        print(json_data)
        recipients = ['asded@gmail.com','nchjedj6@gmail.com', 'hajddccu14@gmail.com']
        send_email(username, email, phone, message,recipients)
        
        return "Successfully Sent"

def send_email(name, email, phone, message,recipients):
    subject = "New Message"
    body = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = OWN_EMAIL
    msg['To'] =  ', '.join(recipients) 
    
    # Send email using SMTP
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(OWN_EMAIL, OWN_PASSWORD)
        smtp_server.sendmail(OWN_EMAIL, recipients, msg.as_string())

    print("Email sent!")

@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)




if __name__ == "__main__":
    app.run(debug=True, port=5001)
