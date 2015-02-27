import re
import random
import itertools
import collections
import traceback

# some MIDI instrument codes:

INSTRUMENT_PIANO = 1
INSTRUMENT_GUITRAR = 25
INSTRUMENT_EBASS = 36
INSTRUMENT_ROCK_DRUMS = 255    # not an actual MIDI code, this is an internal value
INSTRUMENT_STRINGS = 48
EVENT_TEMPO_CHANGE = 1000

## Flattens nested lists.

flatten = lambda *n: (e for a in n
  for e in (flatten(*a) if isinstance(a, (tuple, list)) else (a,)))

#=======================================================================

## Serves for random generation of various things.

class RandomGenerator:

  ## Evaluates a build-in function for random value generation of the
  #  composer file language and returns the generated value.
  #
  #  @param function_string a string representing the function and its
  #         parameters, such as "uniform(0,10)"
  #  @param seed seed that is used to generate the random values
  #  @return the generated value represented as a string (even if it's
  #          a number) or None if there was an error

  def evaluate_function(self,function_string,seed):
    try:
      # remove the spaces
      function_string = re.sub('\s*','',function_string)
      position = function_string.find("(")
      name = function_string[0:position]
      parameters = function_string[position + 1:-1].split(",")

      random.seed(seed)

      if name == "uniform":
        return str(random.randrange(int(parameters[0]),int(parameters[1]) + 1))
      elif name == "values_uniform":
        return random.choice(parameters)
      elif name == "normal":
        return str(int(random.normalvariate(int(parameters[0]),int(parameters[1]))))
      elif name == "yes_no":
        return "yes" if random.randrange(0,100) < int(parameters[0]) else "no"
      elif name == "values":
        calculate_last = False

        if len(parameters) % 2 != 0:
          parameters.append("0")
          calculate_last = True

        values = []
        probabilities = []
        probability_sum = 0

        for i in range(0,len(parameters),2):
          values.append(parameters[i])
          probabilities.append(int(parameters[i + 1]))
          probability_sum += probabilities[-1]

        if calculate_last:
          probabilities[-1] = 100 - probability_sum
          probability_sum += probabilities[-1]

        if probabilities[-1] < 0 or probability_sum != 100: # bad values
          return None

        random_value = random.randrange(0,100)

        probability_sum = 0
        index = 0

        for i in range(len(probabilities)):
          probability_sum += probabilities[i]

          if random_value < probability_sum:
            index = i
            break

        return values[index]

    except Exception:
      print (traceback.format_exc())
      return None

  ## Generates a composition structure (a sequence of section names) from
  #  composition structure string (a regular expression-like string, see
  #  the composition file format specification for details).
  #
  #  @param cs_string composition structure string (see the composition
  #         file specification)
  #  @param seed integer random seed
  #  @return randomly generated composition structure as a list of
  #          section names represented as strings or None if there was
  #          an error parsing the string

  def generate_composition_structure(self, cs_string, seed):
    try:
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
    except Exception:
      return None

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

#=======================================================================

## Represents a list of key-value pairs. Each parameter is stored in
#  formt: name const1 value1 operator const2 value2.

class ParameterList:
  OPERATOR_PLUS = 0
  OPERATOR_MINUS = 1

  ## A class method that makes a parameter list with default values for
  #  a section.
  #
  #  @return ParameterList object with default values initialised

  def make_default_parameter_list():
    result = ParameterList()

    result.set_parameter("tempo",True,"uniform(90,120)")
    result.set_parameter("signature",True,"values(4/4,90,3/4,10)")
    result.set_parameter("instrument-piano",True,"no")

    return result

  def __init__(self):
    self._parameter_dict = {}

  ## Gets the parameter.
  #
  #  @name name of the parameter to be returned (string)
  #  @return parameter as a list in format [const1 (bool), value1,
  #          operator, const2 (bool), value2]

  def get_parameter(self, name):
    try:
      return self._parameter_dict(name)
    except Exception:
      return None

  ## Sets a parameter value.
  #
  #  @param name parameter name (string)
  #  @param const1 whether value1 flag should be set to const (bool)
  #  @param value1 first value (string or integer or None)
  #  @param operator operator to be used between value1 and value2
  #         (see the class constants), if None is set for the operator,
  #         value2 will be ignored
  #  @param const2 whether value2 flag should be set to const (bool)
  #  @param value2 second value (string or integer or None)

  def set_parameter(self, name, const1 = False, value1 = "inherit", operator = None, const2 = False, value2 = None):
    self._parameter_dict[name] = [const1, value1, operator, const2, value2]

  def __str__(self):
    result = ""

    for parameter_name in self._parameter_dict:
      parameter = self._parameter_dict[parameter_name]
      result += parameter_name + ": " + ("C " if parameter[0] else "")
      result += "'" + str(parameter[1]) + "' "

      if parameter[2] != None:
        if parameter[2] == ParameterList.OPERATOR_PLUS:
          result += "+ "
        else:
          result += "- "

        result += ("C " if parameter[3] else "")

        result += "'" + str(parameter[4]) + "'"

      result += "\n"

    return result

#=======================================================================

## Represents a section, or more accurately a section definition
#  (not a section instance), that can be loaded from the compositor
#  file.

class Section:
  def init_attributes(self):
    ## section name
    self.name = ""
    ## name of the parent section in inheritance context, None = no parent
    self.parent_name = None
    ## error explanation string, None = no error
    self._error_string = None
    ## stores parameter values
    self.parameters = ParameterList()

  def __init__(self):
    self.init_attributes()

  ## Gets an error explanation string that occured during the section
  #  loading from string.
  #
  #  @return error explanation string or None if there was no error

  def get_error_string(self):
    return self._error_string

  ## Initialises the section from given string (for the string format
  #  see the composer file format reference).
  #
  #  @string section_string to read the section from

  def load_from_string(self,section_string):
    lines = section_string.split("\n")

    pair = lines[0].split(":")

    self.name = pair[0].rstrip().lstrip()

    if len(pair) == 2:  # parent specified
      self.parent_name = pair[1].rstrip().lstrip()

    if lines[1].lstrip().rstrip() != "{":
      self._error_string = "'{' expected"
      return

    for line in lines[2:]:
      pair = line.split(":")

      pair[0] = pair[0].lstrip().rstrip()

      if len(pair) == 1 and pair[0] == "}":
        return
      elif len(pair) != 2:
        self._error_string = "'wrong value-pair line: " + line
        return

      # parse the parameter value:
      value_split = pair[1].split()

      position = 0
      const1 = False
      const2 = False
      operator = None
      value1 = ""
      value2 = None

      try:
        if value_split[position] == "const":
          const1 = True
          position += 1

        value1 = value_split[position]

        position += 1

        if value_split[position] == "+":
          operator = ParameterList.OPERATOR_PLUS
          position += 1
        elif value_split[position] == "-":
          operator = ParameterList.OPERATOR_MINUS
          position += 1

        if value_split[position] == "const":
          const2 = True
          position += 1

        value2 = value_split[position]
      except Exception:
         pass

      self.parameters.set_parameter(pair[0],const1,value1,operator,const2,value2)

    # if we get here, there was no '{'
    self._error_string = "'}' expected"

  def __str__(self):
    result = "name: " + self.name + "\n"
    result += "parent: " + str(self.parent_name) + "\n"
    result += "parameters:\n"
    result += str(self.parameters)
    return result

#=======================================================================

## Represents a section instance, i.e. a concrete section with its own
#  parameter values and music pattern generated

class SectionInstance:
  def init_attributes(self):
    ## a reference to Section object of which this section is an
    #  instance
    self.definition = None
    ## holds the section tracks with musical notes
    self.tracks = []
    ## section length in beats
    self.length_beats = 4
    ## how many beats are in one bar
    self.beats_in_bar = 4
    ## stores parameter values
    self.parameters = ParameterList()
    ## stores meta events for the section such as tempo change, it is
    #  a list of tuples (time in beats, event type, parameter)
    self.meta_events = []

  ## Converts a beat offset, i.e. a float type time in beats, to real time
  #  in seconds, taking the tempo changes of the section into account.
  #
  #  @param beat_offset input value
  #  @return converted value

  def beat_offset_to_time_offset(self, beat_offset):
    current_beat_offset = 0
    previous_beat_offset = 0
    current_event_event_index = 0
    current_event_index = 0
    accumulated_time = 0
    current_tempo = 100        # default value

    while True:
      if current_event_index >= len(self.meta_events):
        break

      event = self.meta_events[current_event_index]
      current_event_index += 1

      if event[1] != EVENT_TEMPO_CHANGE:    # skip the events that aren't tempo change
        continue

      current_beat_offset = event[0]

      if current_beat_offset >= beat_offset:
        break

      accumulated_time += (current_beat_offset - previous_beat_offset) * 60.0 / current_tempo

      current_tempo = event[2]
      previous_beat_offset = current_beat_offset

    # now there is only a section between the last event and given beat offset

    accumulated_time += (beat_offset - previous_beat_offset) * 60.0 / current_tempo

    return accumulated_time

  def __init__(self):
    self.init_attributes()

  ## Adds a meta event for the track such as a tempo change.
  #
  #  @param time time in beats (float)
  #  @param event_type event type (int, see constants)
  #  @param parameter parameter of the event such as the tempo value

  def add_meta_event(self,time,event_type,parameter):
    self.meta_events.append((time,event_type,parameter))

  ## Adds given track to the section.
  def add_track(self,track):
    self.tracks.append(track)

  def __str__(self):
    result = "events: "

    for event in self.meta_events:
      result += str(event) + ", "

    result += "\n       "

    for i in range(self.length_beats):
      result += "|..............."

    result += "\n"

    for track in self.tracks:
      result += str(track) + "\n"

    return result

#=======================================================================

## Represents a musical note.

class Note:
  def init_attributes(self):
    ## on what time the note starts, the value is in beats (float)
    self.start = 0.0
    ## duration of the note in beats (float)
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

#=======================================================================

## Represents a track used by a section. The track holds the music
#  patern (notes) and an information about it such as its instrument.

class SectionTrack:
  def init_attributes(self):
    ## track instrument
    self.instrument = INSTRUMENT_PIANO
    ## track length in beats
    self.length_beats = 4
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

    while i <= self.length_beats:
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

#=======================================================================

## Represents a composition composed of ordered section instances.

class Composition:
  def init_attributes(self):
    ## a list of section instances that make up the composition
    self.section_instances = []

  def __init__(self):
    self.init_attributes()

  def add_section_instance(self,section_instance):
    self.section_instances.append(section_instance)

  def __str__(self):
    result = ""

    for section in self.section_instances:
      result += str(section) + "\n\n"

    return result

  def save_as_midi():
    return

#=======================================================================

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

#r = RandomGenerator()
#print(r.generate_composition_structure(" aaaa [bbb ccccc dddddddd (XXXXXX YYYYYYY) ]{uniform(2,3)} (xxxx [(fufufu sesese) (popopo mumumu)]) eeeeeee{ uniform(2,3) } ffffff ",12315))
#r.generate_composition_structure("    rock (   (rock_chorus   | pop_chorus)[  uniform(2,3) ]  |   rock_bridge[10])   (rock_chorus(pop_chorus) ) ",12314)

c = Composition()
s = SectionInstance()
t1 = SectionTrack()
t2 = SectionTrack()
t3 = SectionTrack()
t4 = SectionTrack()

t1.add_note(Note(1.0,2.0,60,100))
t1.add_note(Note(3.0,1.5,62,100))
t2.add_note(Note(3.0,1.5,62,100))
t2.add_note(Note(0.0,1,70,80))
t3.add_note(Note(3.5,0.1,58,100))

s.add_track(t1)
s.add_track(t2)
s.add_track(t3)
s.add_track(t4)

s.add_meta_event(0.0,EVENT_TEMPO_CHANGE,60);

c.add_section_instance(s)

print(c)

print(s.beat_offset_to_time_offset(3))
