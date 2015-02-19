import re
import random
import itertools
import collections

# some MIDI instrument codes:

INSTRUMENT_PIANO = 1
INSTRUMENT_GUITRAR = 25
INSTRUMENT_EBASS = 36
INSTRUMENT_ROCK_DRUMS = 255    # not an actual MIDI code, this is an internal value
INSTRUMENT_STRINGS = 48

## Flattens nested lists.

flatten = lambda *n: (e for a in n
  for e in (flatten(*a) if isinstance(a, (tuple, list)) else (a,)))

## Serves for random generation of various things.

class RandomGenerator:
  ## Generates a composition structure (a sequence of section names) from
  #  composition structure string (a regular expression-like string, see
  #  the composition file format specification for details).
  #
  #  @param cs_string composition structure string (see the composition
  #         file specification)
  #  @param seed integer random seed
  #  @return randomly generated composition structure as a list of
  #          section names represented as strings

  def generate_composition_structure(self, cs_string, seed):
    # remove extra spaces:
    cs_string = re.sub('\s+',' ',cs_string).lstrip().rstrip()
    cs_string = re.sub('\s*\(\s*',' ( ',cs_string)
    cs_string = re.sub('\s*\)\s*',' ) ',cs_string)
    cs_string = re.sub('\s*\{\s*',' { ',cs_string)
    cs_string = re.sub('\s*\}\s*',' } ',cs_string)
    cs_string = re.sub('\s*\[\s*',' [ ',cs_string)
    cs_string = re.sub('\s*\]\s*',' ] ',cs_string)
    tokens = cs_string.split()

    random.seed(seed)

    return self.__parse_composition_structure(tokens,seed)

  ## Private function that recursively parses the composition structure
  #  string.
  #
  #  @param tokens list of string tokens representing the structure to
  #         be parsed
  #  @param seed seed for random generation
  #  @return list of generated section names as strings

  def __parse_composition_structure(self, tokens, seed):
    def is_text(what):
      return what not in ["(",")","[","]","{","}"]

    square_brackets = False
    result = []
    helper_list = []

    position = 0

    while position < len(tokens):
      if tokens[position] == "[":
        square_brackets = True
        helper_list = []
      elif tokens[position] == "]":
        result.append(random.choice(helper_list))
        square_brackets = False
      elif tokens[position] == "{":
        helper_string = ""        # read the stuff between { and }
        while True:
          position += 1

          if tokens[position] == "}":
            break

        # TODO: use helper_string here to generate random number and repeat previous section
      else:                                   # ( or a section name
        item = tokens[position]

        if tokens[position] == "(":           # recurse
          position2 = position
          bracket_count = 0

          while True:
            if tokens[position2] == "(":
              bracket_count += 1
            elif tokens[position2] == ")":
              bracket_count -= 1
              if bracket_count == 0:
                break

            position2 += 1

          item = self.__parse_composition_structure(tokens[position + 1:position2],seed)

          position = position2

        if square_brackets:
            helper_list.append(item)
        else:
            result.append(item)

      position += 1

    return list(flatten(result))

## Represents a section, or more accurately a section definition
#  (not a section instance), that can be loaded from the compositor
#  file.

class Section:
  def init_attributes(self):
    ## section name
    self.name = ""

  def __init__(self):
    self.init_attributes()

## Represents a section instance, i.e. a concrete section with its own
#  parameter values and music pattern generated

class SectionInstance:
  def init_attributes(self):
    ## a reference to Section object of which this section is an
    #  instance
    self.definition = None
    ## holds the section tracks with musical notes
    self.tracks = []
    ## section length in bars
    self.length_bars = 4

  def __init__(self):
    self.init_attributes()

  ## Adds given track to the section.
  def add_track(self,track):
    self.tracks.append(track)

  def __str__(self):
    result = "       "

    for i in range(self.length_bars):
      result += "|..............."

    result += "\n"

    for track in self.tracks:
      result += str(track) + "\n"

    return result

## Represents a musical note.

class Note:
  def init_attributes(self):
    ## on what time the note starts, the value is in bars (float)
    self.start = 0.0
    ## duration of the note in bars (float)
    self.length = 0.25
    ## note "strength", integer 0 - 127
    self.velocity = 100
    ## MIDI note code (C3 = 60)
    self.note = 60

  def __init__(self):
    self.init_attributes()

  def __init__(self, start, length, note, velocity):
    self.init_attributes()
    self.start = start
    self.length = length
    self.velocity = velocity
    self.note = note

  def __str__(self):
    remainder = self.note % 12

    if remainder == 0:
      return "C"
    elif remainder == 1:
      return "d"
    elif remainder == 2:
      return "D"
    elif remainder == 3:
      return "e"
    elif remainder == 4:
      return "E"
    elif remainder == 5:
      return "F"
    elif remainder == 6:
      return "g"
    elif remainder == 7:
      return "G"
    elif remainder == 8:
      return "a"
    elif remainder == 9:
      return "A"
    elif remainder == 10:
      return "b"
    elif remainder == 11:
      return "B"

## Represents a track used by a section. The track holds the music
#  patern (notes) and an information about it such as its instrument.

class SectionTrack:
  def init_attributes(self):
    ## track instrument
    self.instrument = INSTRUMENT_PIANO
    ## track length in bars
    self.length_bars = 4
    ## number of beats in a bar
    self.signature = 4
    ## list of Note objects representing a musical pattern of the track
    self.notes = []

  def __init__(self):
    self.init_attributes()

  ## Sorts the notes list so they are in order in which the start
  #  playing.

  def sort_notes(self):
    self.notes.sort(key = lambda note: note.start)

  def add_note(self,note):
    self.notes.append(note)
    self.sort_notes()

  def __str__(self):
    number_string = str(self.instrument)
    result = number_string + ": "

    for i in range(3 - len(number_string)):
      result += " "

    result += ": "

    i = 0

    while i <= self.length_bars:
      nothing = True

      for note in self.notes:
        if i >= note.start and i <= note.start + note.length:
          result += str(note)
          nothing = False
          break

      if nothing:
        result += "."

      i += 0.0625

    return result

## Represents a composition composed of ordered section instances.

class Composition:
  def init_attributes(self):
    ## a list of section instances that make up the composition
    self.section_instances = []

  def __init__(self):
    self.init_attributes()

  def save_as_midi():
    return

#instance = SectionInstance()
#track = SectionTrack()
#track2 = SectionTrack()
#track2.instrument = INSTRUMENT_ROCK_DRUMS

#track2.add_note(Note(0.5,1,120,100))
#track2.add_note(Note(2.0,1,100,50))

#track.add_note(Note(1,0.6,120,100))
#track.add_note(Note(3.0,0.25,100,50))

#instance.add_track(track)
#instance.add_track(track2)
#print(instance)

r = RandomGenerator()
print(r.generate_composition_structure(" aaaa [bbb ccccc dddddddd (XXXXXX YYYYYYY) ]{uniform(2,3)} (xxxx [(fufufu sesese) (popopo mumumu)]) eeeeeee{ uniform(2,3) } ffffff ",12315))
#r.generate_composition_structure("    rock (   (rock_chorus   | pop_chorus)[  uniform(2,3) ]  |   rock_bridge[10])   (rock_chorus(pop_chorus) ) ",12314)
