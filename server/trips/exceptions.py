class ColumnNotFoundException(Exception):
  def __init__(self, message="The specified column does not exist"):
    self.message = message
    super().__init__(self.message)

