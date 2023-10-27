#!/usr/bin/env python
import asyncio
import logging
import email
import requests
import sys

from dotenv import dotenv_values
from aiosmtpd.controller import Controller
from aiosmtpd.smtp import SMTP as SMTPServer
from aiosmtpd.smtp import Envelope as SMTPEnvelope
from aiosmtpd.smtp import Session as SMTPSession
from email.message import Message
import base64

from utils import parse_ntfy_url

from mapper import mail_to_ntfy_format, MailType
from notification import Notification

global config
global mail_type
global username
global password
global ntfy_url

class PushHandler:
  async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
    if not address.endswith('@example.com'):
      return '550 not relaying to that domain'
    envelope.rcpt_tos.append(address)
    return '250 OK'

  async def handle_DATA(self, server: SMTPServer, session: SMTPSession, envelope: SMTPEnvelope):
    email_content = email.message_from_bytes(envelope.content)
    
    notifications: [Notification] = mail_to_ntfy_format(email_content, mail_type=mail_type)    
    for n in notifications:
      send_notfication(n, username, password)
    return '250 Message accepted for delivery'

def send_notfication(notification: Notification, url: str, username: str, password: str) -> requests.Response:
  auth_basic_credentials = (username + ':' + password).encode('utf-8')
  auth_basic_credentials = base64.b64encode(auth_basic_credentials)
  notification.headers["Authorization"] = f"Basic {auth_basic_credentials.decode('utf-8')}"
  return requests.post(url, data=notification.data, headers=notification.headers)


async def main(loop):
  cont = Controller(PushHandler(), hostname=config["HOST"], port=config["PORT"])
  cont.start()


if __name__ == '__main__':
  config = dotenv_values("config/.env")
  mail_type = MailType(config["TYPE"])
  username = config['NTFY_USER']
  password = config['NTFY_PASSWORD']
  ntfy_url = parse_ntfy_url(config.get("NTFY_HOST"), config.get("NTFY_TOPIC"))
  logging.basicConfig(level=logging.DEBUG)

  register_notification = Notification(data=f"SMTP SinkPush User '{username}' authorized!", headers={"Title": "SMTP SinkPush Server"})
  response = send_notfication(register_notification, ntfy_url, username, password)
  if response.status_code >= 400:
    logging.error(msg=f"{response.status_code}: {response.reason}")
    sys.exit(1)

  loop = asyncio.get_event_loop()
  loop.create_task(main(loop=loop))
  try:
    loop.run_forever()
  except KeyboardInterrupt:
    pass