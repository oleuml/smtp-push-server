#!/usr/bin/env python
import asyncio
import logging

from aiosmtpd.controller import Controller
from aiosmtpd.handlers import Debugging
from smtplib import SMTP
import requests


class PushHandler:
  async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
    if not address.endswith('@example.com'):
      return '550 not relaying to that domain'
    envelope.rcpt_tos.append(address)
    return '250 OK'

  async def handle_DATA(self, server, session, envelope):
    requests.post("https://ntfy.sh/fabiundoletestenunifiedpushundntfy", data=envelope.content)
    return '250 Message accepted for delivery'

async def main(loop):
  cont = Controller(PushHandler(), hostname='127.0.0.1', port=1025)
  cont.start()


if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG)
  loop = asyncio.get_event_loop()
  loop.create_task(main(loop=loop))
  try:
    loop.run_forever()
  except KeyboardInterrupt:
    pass