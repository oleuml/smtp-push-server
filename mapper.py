from email.message import Message
from notification import Notification

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
  notifications = []
  if type(messages) == list:
    for message in messages:
      message: Message = message
      payload = message.get_payload()
      print(message.get('Content-Transfer-Encoding'))
      if message.get('Content-Transfer-Encoding') == 'base64':
        payload = base64.b64decode(payload)
      notifications.append(Notification(payload, {"Title": email_content.get("subject"), "Priority": "urgent", "Tags": "warning,skull", "Filename": message.get_filename()}))
  else:
    payload = messages
    if email_content.get('Content-Transfer-Encoding') == 'base64':
      payload = base64.b64decode(payload)
    notifications.append(Notification(payload, {"Title": email_content.get("subject"), "Priority": "urgent", "Tags": "warning,skull" }))

  return notifications
  
test = mail_to_ntfy_format(None, REOLINK)
