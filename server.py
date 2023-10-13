#!/usr/bin/env python
import asyncio
import logging
import email
import requests
import base64

from dotenv import dotenv_values

from aiosmtpd.controller import Controller
from aiosmtpd.smtp import SMTP as SMTPServer
from aiosmtpd.smtp import Envelope as SMTPEnvelope
from aiosmtpd.smtp import Session as SMTPSession
from email.message import Message


global config

class PushHandler:
  async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
    if not address.endswith('@example.com'):
      return '550 not relaying to that domain'
    envelope.rcpt_tos.append(address)
    return '250 OK'

  async def handle_DATA(self, server: SMTPServer, session: SMTPSession, envelope: SMTPEnvelope):
    email_content = email.message_from_bytes(envelope.content)
    messages: [Message] | str = email_content.get_payload()

    if type(messages) == list:
      for message in messages:
        message: Message = message
        payload = message.get_payload()
        print(message.get('Content-Transfer-Encoding'))
        if message.get('Content-Transfer-Encoding') == 'base64':
          payload = base64.b64decode(payload)
        requests.post("https://ntfy.sh/fabiundoletestenunifiedpushundntfy",
          data=payload,
          headers={
              "Title": email_content.get("subject"),
              "Priority": "urgent",
              "Tags": "warning,skull",
              "Filename": message.get_filename()
          })

    else:
      payload = messages
      if message.get('Content-Transfer-Encoding') == 'base64':
        payload = base64.b64decode(payload)
      requests.post("https://ntfy.sh/fabiundoletestenunifiedpushundntfy",
        data=payload,
        headers={
            "Title": email_content.get("subject"),
            "Priority": "urgent",
            "Tags": "warning,skull",
        })


    return '250 Message accepted for delivery'

async def main(loop):
  cont = Controller(PushHandler(), hostname=config["HOST"], port=1025)
  cont.start()


if __name__ == '__main__':
  config = dotenv_values("config/.env")
  logging.basicConfig(level=logging.DEBUG)
  loop = asyncio.get_event_loop()
  loop.create_task(main(loop=loop))
  try:
    loop.run_forever()
  except KeyboardInterrupt:
    pass