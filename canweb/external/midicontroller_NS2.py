
def statusByte(statusType, channel):
  def statusByte(statusType):
    if statusType == "ControlChange":
      return 0xB0
    elif statusType == "ProgramChange":
      return 0xC0
    else:
      raise ValueError("Unimplemented status type: '" + statusType + "'.")

  if channel & 0x0F != channel:
    raise ValueError("Program must be in range [0, 15] but is ", program)
  return bytes([ statusByte(statusType) | channel ])


def selectProgram(songprogram, channel):
  def selectProgram(program, channel):
    data = b''
    data += statusByte('ProgramChange', channel)

    if program & 0x7F != program:
      raise ValueError("Program must be in range [0, 127] but is ", program)

    data += bytes([program])
    return data

  def selectBank(bank, channel):
    data = b''
    data += statusByte('ControlChange', channel)

    data += b'\x00' # select Bank
    if bank & 3 != bank:
      raise ValueError("Bank must be in range [0, 3] but is ", bank)
    data += bytes([ 0 ])

    data += statusByte('ControlChange', channel)
    data += b'\x20' # select Bank
    if bank & 3 != bank:
      raise ValueError("Bank must be in range [0, 3] but is ", bank)

    data += bytes([ bank ])
    return data

  data = b''
  data += selectBank(songprogram['bank'], channel)

  # there are 20 pages each of which has 5 programs.
  program = songprogram['program'] + 5 * songprogram['page'] 
  data += selectProgram(program, channel)
  return data



  
