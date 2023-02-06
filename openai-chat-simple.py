#!/usr/bin/env python3

DEFAULT_KEY_FILE = 'api_key'

import sys
import os
import argparse

from openai_chatter import Chatter

def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('prompts', nargs='*', help='Prompts to send.')
  parser.add_argument('-k', '--key-file', help='Use another key file instead of api_keys/key')
  return parser.parse_args()

def find_key(args):
  if args.key_file:
    try:
      with open(args.key_file) as fin:
        sys.stderr.write(f'Using given key file: {args.key_file}\n')
        return fin.readline().strip()
    except IOError as e:
      print(e, file=sys.stderr)
      sys.stderr.write(f'Fatal: fail to load key from key file {args.key_file}')
      sys.exit(2)

  key = os.getenv("OPENAI_API_KEY")
  if key:
    sys.stderr.write(f'Using key from environment variable OPENAI_API_KEY\n')
    return key
  
  try:
    repo_path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(repo_path, DEFAULT_KEY_FILE)) as fin:
      sys.stderr.write(f'Using default key file: {DEFAULT_KEY_FILE}\n')
      return fin.readline().strip()
  except IOError as e:
    print(e, file=sys.stderr)

  sys.stderr.write(f'Fatal: neither key file given in the default location ("{DEFAULT_KEY_FILE}") or specified with "-k" option, nor key given with variable OPENAI_API_KEY. ABORT!')
  sys.exit(2)

def interactive_mode(chatter):
  is_terminal = os.isatty(sys.stdout.fileno())
  TC_GREEN = is_terminal and '\033[1;32m' or ''
  TC_YELLOW = is_terminal and '\033[1;33m' or ''
  TC_BLUE = is_terminal and '\033[1;34m' or ''
  TC_NONE = is_terminal and '\033[0m' or ''

  i = 0
  while True:
    try:
      prompt = input(TC_YELLOW + f'You[{i}]: ' + TC_NONE)
      print(TC_BLUE + f'ChatGPT[{i}]: ', end = '')
      sys.stdout.flush()
      print(TC_GREEN + chatter.interact(prompt) + TC_NONE + '\n')
    except KeyboardInterrupt or EOFError:
      print('\n')
      return 0
    except Exception as e:
      print(e)
      break
    i += 1
  return 0

def main():
  args = parse_args()
  chatter = Chatter(find_key(args))
  if len(args.prompts) == 0:
    return interactive_mode(chatter)
  else:
    chatter.talk(args.prompts)
  return 0

if __name__ == '__main__':
  sys.exit(main())
