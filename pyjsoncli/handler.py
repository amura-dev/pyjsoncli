import json
import logging

import help



class JSONHandler():
  def __init__(self, fpath_abs):
    self.fpath_abs = fpath_abs
    self.arg_accumulator = []
    self.func_accumulator = [] # [(func, [arg])]
    self.found_default = False

  
  def parse(self):
    data = None
    with open(self.fpath_abs, 'r') as fh:
      data = json.load(fh)
      if not isinstance(data, dict):
        raise help.Error("Syntax error: Outermost structure must be a \
                         dictionary")
      # TODO: detect duplicate flags
      for entry in data.values():
        help.dbg_print("new entry")
        recur = True
        while recur:
          help.dbg_print(entry)
          recur, entry = self.parse_entry(entry)
      help.dbg_print("END:", self.func_accumulator)


  def parse_entry(self, entry):
    if not isinstance(entry, dict):
      # TODO: indicate location of erroneous code.
      help.dbg_print(entry)
      raise help.Error("Syntax error: Flag value is not an object")
    
    args = None
    flag = None
    func = None
    next_entry = None
    for key, val in entry.items():
      # doesnt check for function if flags found or vice versa
      # check if functions exist
      # TODO: add directory support
      if key == 'args':
        help.dbg_print("args case", val)
        help.dbg_print("ARGS FOUND:", key, val)
        args = val

      elif key.startswith('-'):
        help.dbg_print("FLAG FOUND", key, val)
        flag = key
        next_entry = val

      elif key == 'func':
        help.dbg_print("FUNC FOUND", key, val)
        func = val

      elif key == '_COMMENT':
        continue

      elif key == 'default' and self.found_default == False:
        help.dbg_print("DEFAULTS SET")
        self.found_default = True
        return (True, val)

      elif key == 'default' and self.found_default == True:
        raise help.Error(f"Syntax error: Defaults set multiple times")

      else:
        raise help.Error(f"Syntax error: Unsupported key found: {key}")
    
    if args != None:
      self.arg_accumulator += args
      if flag != None and func != None:
        raise help.Error("Syntax error: A flag and a function were specified together")
      elif flag == None and func != None:
        func_n_args = (func, self.arg_accumulator)
        self.arg_accumulator = []
        self.func_accumulator.append(func_n_args)
        return (False, -1)
      elif func == None and flag != None:
        return (True, next_entry)
      else:
        raise help.Error("Syntax error: No flag or function found")

    return (False, -1)
    

  def gen_script(self, save_path_abs):
    pass