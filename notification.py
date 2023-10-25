class Notification():
  def __init__(self, data, headers: dict):
    self.data = data
    self.headers = headers


x = Notification("test", {"a": "b"})
print(x.data)
  