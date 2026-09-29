"""
ADD YOUR HEADE HERE
"""



def factorial(n: int) -> int:
  """
    Compute the foactorial foa given number

    arguments:
      - n: an integer
    return:
      - factorial of n
  """

  fact = 1
  for i in range(n):
     fact  = fact * (i+1)
  return fact


def main():
  help(factorial)

  print(factorial(10))


if __name__ == '__main__':
  main()
