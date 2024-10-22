import requests
import time

# Base URL and pages to check
base_url = "https://chatgpt.com/"
pages = ["console/", "test.aspx"]
webhook_url = "https://your-webhook-url.com"
interval = 10  # in seconds, can be customized

# Custom messages for each page
custom_messages = {
    "console/": "Console page status: ",
    "test.aspx": "Test.aspx page status: "
}

# Function to check the status of each page
def check_pages_status():
    status_messages = []
    
    for page in pages:
        try:
            url = base_url + page
            response = requests.get(url)
            
            if response.status_code == 200:
                status_messages.append(custom_messages.get(page, "Page") + "OK")
            else:
                status_messages.append(custom_messages.get(page, "Page") + f"Error: {response.status_code}")
        except Exception as e:
            status_messages.append(custom_messages.get(page, "Page") + f"Failed: {str(e)}")
    
    # Send status messages to the webhook
    post_to_webhook("\n".join(status_messages))

# Function to send the status to a webhook
def post_to_webhook(message):
    data = {
        "text": message
    }
    try:
        response = requests.post(webhook_url, json=data)
        if response.status_code != 200:
            print(f"Error sending message to webhook: {response.status_code}")
    except Exception as e:
        print(f"Failed to send to webhook: {str(e)}")

# Main loop to check status periodically
def monitor_pages():
    while True:
        check_pages_status()
        time.sleep(interval)

if __name__ == "__main__":
    monitor_pages()
