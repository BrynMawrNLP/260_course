class Pie:
  """TODO - add doc
  """

  #Pie() - java
  # self is the python version of this
  def __init__(self, name: str, num_slices: int):
    """Constructs a new Pie with a name (str) and number of slices (int)"""
    self.name = name
    self.num_slices = num_slices

  def __str__(self) -> str:
    return f"{self.name} has {self.num_slices} left"


  def __private_method(): # this is how we specify private mthods, though nothing is actually private in python
