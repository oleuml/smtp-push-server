from email.message import Message
from notification import Notification
import base64

SUPPORTED_MAIL_TYPES = ['standard', 'reolink']

class MailType:
  def __init__(self, mail_type):
    if mail_type not in SUPPORTED_MAIL_TYPES:
      raise Exception(f"Unknown mail type. MailType must be one of these: {SUPPORTED_MAIL_TYPES}")
    self.mail_type = mail_type
  def __str__(self):
    return self.mail_type
  def __eq__(self, o):
    return self.mail_type == o.mail_type

STANDARD = MailType('standard')
REOLINK = MailType('reolink')

def mail_to_ntfy_format(message: Message, mail_type: MailType) -> [Notification]:
  match mail_type.mail_type:
    case STANDARD.mail_type:
      return _standard_to_ntfy(message)
    case REOLINK.mail_type:
      return _reolink_to_ntfy(message)
    case _:
      raise Exception(f"Unknown mail type. MailType must be one of these: {SUPPORTED_MAIL_TYPES}")

def _standard_to_ntfy(message: Message) -> [Notification]:
  return [Notification(message.get_payload(), {})]

def _reolink_to_ntfy(message: Message):
  messages: [Message] | str = message.get_payload()

  notifications = []
  if type(messages) == list:
    for _message in messages:
      payload = _message.get_payload()
      if _message.get('Content-Transfer-Encoding') == 'base64':
        payload = base64.b64decode(payload)
      notifications.append(Notification(payload, {"Title": message.get("subject"), "Priority": "urgent", "Tags": "warning,skull", "Filename": _message.get_filename()}))
  else:
    payload = messages
    if payload.get('Content-Transfer-Encoding') == 'base64':
      payload = base64.b64decode(payload)
    notifications.append(Notification(payload, {"Title": message.get("subject"), "Priority": "urgent", "Tags": "warning,skull" }))

  return notifications
  
