## Optimising your program for the ISS

More info with link: https://projects.raspberrypi.org/en/projects/mission-space-lab-creator-guide/3

### Important: Update your main.py file to make use of the datetime library to stop your program before the 10-minute time slot has finished.

sample code:

```python
from datetime import datetime, timedelta
from time import sleep

# Create a variable to store the start time
start_time = datetime.now()
# Create a variable to store the current time
# (these will be almost the same at the start)
now_time = datetime.now()
# Run a loop for 1 minute
while (now_time < start_time + timedelta(minutes=1)):
    print("Hello from the ISS")
    sleep(1)
    # Update the current time
    now_time = datetime.now()
# Out of the loop — stopping
```