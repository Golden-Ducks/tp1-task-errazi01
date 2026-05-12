# line 11
your `numbers_dict` is missing `"0"`

# line 24
use `string.punctuation`
import the `string` module to avoid typing out punctuation manually

# line 27
avoid using `.replace()` inside a loop.. it creates a new string every time
no need for iterating over the entire text too many times, just use a single loop for characters
