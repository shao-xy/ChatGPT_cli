#!/usr/bin/env python3

import os
import openai

class Chatter:
  def __init__(self, key, model='text-davinci-003'):
    self._key = key
    self._model = model

  def _chat_one(self, prompt, text_only):
    assert(type(prompt) == str)
    openai.api_key = self._key
    response = openai.Completion.create(
      model = self._model,
      prompt = prompt,
      max_tokens = 1024,
      n = 1,
      stop = None,
      temperature = 0.5,
      )
    return text_only and response.choices[0].text or response

  def interact(self, prompt, text_only=True):
    if type(prompt) == str:
      return self._chat_one(prompt, text_only)
    elif type(prompt) == list or type(prompt) == tuple:
      return [ self._chat_one(p, text_only) for p in prompt ]

  def talk(self, prompt):
    response = self.interact(prompt)
    if type(response) == str:
      print(response)
    else:
      for r in response:
        print(r)

if __name__ == '__main__':
  Chatter().talk('Hello!')
