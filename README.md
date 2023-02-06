# Simple command-line interface for ChatGPT

## Usage

The most simple way to run is to store your key in `api_key` file and run `openai-chat-simple.py`.

Alternatively, specify key file with `-k` option or in the `OPENAI_API_KEY` environment variable.

## Injection to other Python scripts

Add this directory to path, and import `Chatter` class from `openai_chatter` file. For example:

```
import sys
sys.path.insert(0, '/path/to/this/repo')
from openai_chatter import Chatter
```

Then the `Chatter` class might be useful. Enjoy!
