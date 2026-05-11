from locust import HttpUser, task

"""
You need to run in two separated terminals the following commands:
Terminal1: $ uvicorn protoapp.main:app
Terminal2: $ locust

Open your browser and navigate to http://localhost:8089 to access the web interface of the application.
The web interface is intuitively designed, making it straightforward to:
• Set Concurrent Users: Specify the maximum number of users accessing the service simultaneously
during peak usage.
• Configure Ramp-Up Rate: Determine the rate of new users added per second to simulate
increasing traffic.
After configuring these parameters, click the Start button to initiate a simulation that generates traffic
to the protoapp via the /home endpoint defined in the locustfile.py.
Alternatively, you can simulate traffic using the command line. Here’s how:
    $ locust --headless --users 10 --spawn-rate 1
This command runs Locust in a headless mode to simulate:
• 10 users accessing your application concurrently.
• A spawn rate of 1 user per second.
"""

class ProtoappUser(HttpUser):
    host = "http://localhost:8000"

    @task
    def hello_world(self):
        self.client.get("/home")

    @task
    def get_item(self):
        self.client.get("/item")