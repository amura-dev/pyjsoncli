import os
import sys

import help
from handler import JSONHandler

VERSION = '0.0.0'
INPUT_FLAG = '-i'
INPUT_FLAG_EXT = '--input'
OUTPUT_FLAG = '-o'
OUTPUT_FLAG_EXT = '--output'
FLAGS = [
  INPUT_FLAG,
  INPUT_FLAG_EXT,
  OUTPUT_FLAG,
  OUTPUT_FLAG_EXT
]


def main():
  find_HELP()
  find_VERSION()
  # find_VERBOSE

  handler = None
  found_INPUT, value_INPUT = find_INPUT()
  if found_INPUT:
    handler = JSONHandler(value_INPUT)
    handler.parse()
    pass

  found_OUTPUT, value_OUTPUT = find_OUTPUT()
  if found_OUTPUT:
    pass
    # see if dir exists
    # create file there
    # generate into specified file


def find_HELP():
  for arg in sys.argv:
    if arg == '--help':
      help.show_full_help()
      exit(0)


def find_VERSION():
  if sys.argv[1] == '--version':
    print(f'pyjsoncli {VERSION}')


def find_INPUT():
  try:
    fpath = sys.argv[1]
  except Indexhelp.Error:
    help.show_mini_help()
    exit(1)
  
  if not_flag(fpath):
    fpath_abs = os.path.abspath(fpath)
    if os.path.exists(fpath_abs) and os.path.isfile(fpath_abs):
      return (True, fpath_abs)
    else:
      raise help.Error(f"Specified input file does not exist: {fpath}")

  idxs = find_many(sys.argv, INPUT_FLAG, INPUT_FLAG_EXT)
  if len(idxs) == 0:
    raise help.Error("No input file specified")
  elif len(idxs) > 1:
    raise help.Error(f"Multiple input flags found: {INPUT_FLAG}, {INPUT_FLAG_EXT}")
  elif len(idxs) == 1:
    try:
      fpath = sys.argv[idxs[0] + 1]
    except Indexhelp.Error:
      raise help.Error("No input file specified")
    else:
      fpath_abs = os.path.abspath(fpath)
      if os.path.exists(fpath_abs) and os.path.isfile(fpath_abs):
        return (True, fpath_abs)
      else:
        raise help.Error(f"Specified input file does not exist: {fpath}")
    

def find_OUTPUT():
  try:
    fpath = sys.argv[1]
  except Indexhelp.Error:
    help.show_mini_help()
    exit(1)
  
  if not_flag(fpath):
    fpath_abs = os.path.abspath(fpath)
    fpath_dir = os.path.dirname(fpath_abs)
    if os.path.exists(fpath_dir):
      return (True, fpath_abs)

  idxs = find_many(sys.argv, OUTPUT_FLAG, OUTPUT_FLAG_EXT)
  if len(idxs) == 0:
    raise help.Error("No output file specified")
  elif len(idxs) > 1:
    raise help.Error(f"Multiple output flags found: {OUTPUT_FLAG}, {OUTPUT_FLAG_EXT}")
  elif len(idxs) == 1:
    try:
      fpath = sys.argv[idxs[0] + 1]
    except Indexhelp.Error:
      raise help.Error("No input output specified")
    else:
      fpath_abs = os.path.abspath(fpath)
      fpath_dir = os.path.dirname(fpath_abs)
      if os.path.exists(fpath_dir):
        return (True, fpath_abs)


def not_flag(fpath):
  if fpath.startswith('-'):
    return False
  return True


def find_many(xs, *args):
  idxs = []
  for i, x in enumerate(xs):
    if x in args:
      idxs.append(i)

  return idxs


if __name__ == '__main__':
  main()
