# Importing necessary libraries
import customtkinter
import requests
import clipboard
import validators
from CTkMessagebox import CTkMessagebox

# Access token for the URL shortening service
access_token = "MxPGzuo5zkvXkFmcAqhd0uOnS9uiOnaY4o4axDzkQAbFVddxNuiDrXEIjaTq"
# API URL for the URL shortening service
api_url = "https://t.ly/api/v1/link/shorten"

# Function to handle the URL shortening process
def show_url():
    # Retrieve the URL from the entry field
    url = url_entry.get()

    # Validate the URL using the validators library
    if not validators.url(url):
        # Display an error message if the URL is invalid
        CTkMessagebox(title="Error",
                      message="Invalid URL, Please enter a valid URL \n For Example: https://www.google.com",
                      icon="cancel")
        return

    # Headers for the API request, including the access token and content type
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }

    # Data to be sent in the API request
    data = {
        'long_url': url,
    }

    try:
        # Send a POST request to the URL shortening service to shorten the URL
        response = requests.post(api_url, json=data, headers=headers)
        # Extract the shortened URL from the API response
        shortened_url = response.json().get('short_url')
        # Update the short url label with the shortened URL
        short_url.configure(text=f"Short URL: {shortened_url}")
        # Update the clipboard icon command to copy the shortened URL
        clipboard_icon.configure(text=f"📋", command=lambda: copy_url(shortened_url))
    except requests.RequestException as e:
        # Display an error message if there was an issue with the API request
        customtkinter.CTkLabel(app, text=f"Error: {e}", font=("sans", 18), fg_color="transparent").pack()
        print(e)


# Function to copy the shortened URL to the clipboard
def copy_url(url):
    clipboard.copy(url)
    url_entry.delete('0', 'end')


# Set the appearance mode and default color theme for customtkinter
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme('blue')

# Create the main application window
app = customtkinter.CTk()
app.geometry("550x250")
app.title("URL Shortener")

# Create a label for the URL entry field
url_label = customtkinter.CTkLabel(app, text="Please Enter Your URL Here: ", font=("sans", 18), fg_color="transparent")
url_label.pack(pady=5)

# Create an entry field for the URL
url_entry = customtkinter.CTkEntry(app, placeholder_text="Enter Your URL Here: ", fg_color="transparent", width=300)
url_entry.pack()

# Create a button to trigger the URL shortening process
url_button = customtkinter.CTkButton(app, text="Get Your Link", corner_radius=5, command=show_url)
url_button.pack(pady=10)

# Create a label to display the shortened URL
short_url = customtkinter.CTkLabel(app, text='', font=("sans", 20))
short_url.pack()

# Create a button to copy the shortened URL to the clipboard
clipboard_icon = customtkinter.CTkButton(app, text='', font=("sans", 30), width=1, fg_color='transparent')
clipboard_icon.pack(pady=10)

# Start the main event loop of the application
app.mainloop()
