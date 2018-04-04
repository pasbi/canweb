#!/usr/bin/env python3

import binascii

class MidiController:
  def __init__(self, channel, device):
    self.channel = channel # midi channel
    self.device = device # e.g. '/dev/midiX' 
    self.cable = 0

  def sendMidiMessage(self, device, codeIndexNumber, data1, data2):
    data = bytes([ 
      0xb0 | (self.channel & 0xf), 
      ((self.cable & 0xf) << 4) | (codeIndexNumber & 0xf),
      data1,
      data2
    ])
    device.write(data)
    print("Sent midi command '{}'".format(binascii.hexlify(data).decode('utf-8')))

  def sendMidiControlChange(self, device, function, value):
    self.sendMidiMessage(device, 0xb, function, value);


  def sendMidiProgramChange(self, device, program):
    self.sendMidiMessage(device, 0xc, program, 0);


  def applyProgram(self, program):
    if program['isValid']:
      if program['type'] == "NS2":
        bank = program['bank']
        program = program['program']  + 5 * program['page']
        try:
          with open(self.device, 'r+b') as midi:  # don't create the file if it does not exist
              self.sendMidiControlChange(midi, 32, bank)
              self.sendMidiProgramChange(midi, program)
              return True
        except FileNotFoundError:
          return False
      else:
        print("Unrecognized program type: '{}'".format(program['type']))

if __name__ == "__main__":
  print("Testing midi...")
  channel = 1
  program = 1
  bank = 1
  page = 1
  mc = MidiController(1)
  r = mc.applyProgram({
      "type": "NS2",
      "isValid": True,
      "program": program,
      "bank": bank,
      "page": page 
    })
  print(r)