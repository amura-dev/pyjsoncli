class Error():
  def __init__(self, msg):
    print(msg)
    show_mini_help()
    exit(0)



def show_mini_help():
  print("Use 'pycli --help' for more information")


def show_full_help():
  with open('HELP.txt', 'r') as fh:
    for line in fh:
      print(line, end='')


def dbg_print(*msgs, end_str='\n'):
  print(f"DEBUG:", end='')
  for msg in msgs:
    print(' ', end='')
    print(msg, end='')
  print('\n')
