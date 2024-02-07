## How to use senseHat module?

Based on: https://projects.raspberrypi.org/en/projects/getting-started-with-the-sense-hat

use in program:

```python
from sense_hat import SenseHat
sense = SenseHat()
sense.show_message(str(sense.get_humidity()))
```

More documentation:
* https://sense-hat.readthedocs.io/en/latest/
* 