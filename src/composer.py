import re
import random
import itertools
import collections
import traceback
import sys
from MidiFile3 import MIDIFile

# instrument codes, these may not correspond to actual midi codes,
# bacause these internal values include also a way to play the
# instruments, so for example rock drums and metal drums may map to
# the same MIDI instrument in the end

INSTRUMENT_PIANO = 1
INSTRUMENT_GUITAR = 25
INSTRUMENT_EBASS = 36
INSTRUMENT_ROCK_DRUMS = 255       # internal value
INSTRUMENT_STRINGS = 48
EVENT_TEMPO_CHANGE = 1000

# these correspond to MIDI codes:
NOTE_DRUM_BASS = 35
NOTE_DRUM_SIDE_STICK = 37
NOTE_DRUM_SNARE = 38
NOTE_DRUM_TOM_HIGH = 50
NOTE_DRUM_TOM_MID = 48
NOTE_DRUM_TOM_LOW = 45
NOTE_DRUM_HIHAT_CLOSED = 42
NOTE_DRUM_HIHAT_PEDAL = 44
NOTE_DRUM_CYMBAL_CRASH = 49
NOTE_DRUM_CYMBAL_RIDE = 51
NOTE_DRUM_CYMBAL_RIDE_BELL = 53
NOTE_DRUM_CYMBAL_SPLASH = 55
NOTE_DRUM_CLAP = 39

KEY_C_NOTES = [i * 12 for i in range(11)]                # contains all key codes for the C key
KEY_C_NOTES += [i * 12 + 2 for i in range(11)]
KEY_C_NOTES += [i * 12 + 4 for i in range(11)]
KEY_C_NOTES += [i * 12 + 5 for i in range(11)]
KEY_C_NOTES += [i * 12 + 7 for i in range(11)]
KEY_C_NOTES += [i * 12 + 9 for i in range(11)]
KEY_C_NOTES += [i * 12 + 11 for i in range(10)]
KEY_C_NOTES.sort()

KEY_DB_NOTES  = [i + 1 for i in KEY_C_NOTES]
KEY_D_NOTES   = [i + 2 for i in KEY_C_NOTES]
KEY_EB_NOTES  = [i + 3 for i in KEY_C_NOTES]
KEY_E_NOTES   = [i + 4 for i in KEY_C_NOTES]
KEY_F_NOTES   = [i + 5 for i in KEY_C_NOTES]
KEY_GB_NOTES  = [i + 6 for i in KEY_C_NOTES]
KEY_G_NOTES   = [i + 7 for i in KEY_C_NOTES]
KEY_AB_NOTES  = [i + 8 for i in KEY_C_NOTES]
KEY_A_NOTES   = [i + 9 for i in KEY_C_NOTES]
KEY_BB_NOTES  = [i + 10 for i in KEY_C_NOTES]
KEY_B_NOTES   = [i + 11 for i in KEY_C_NOTES]

## Flattens nested lists.

flatten = lambda *n: (e for a in n
  for e in (flatten(*a) if isinstance(a, (tuple, list)) else (a,)))

## Converts internal instrumen code to MIDI instrument code
#
#  @param instrument internal instrument value (see constants)
#  @return mapped MIDI instrument code

def instrument_to_midi(instrument):
  return instrument

#=======================================================================

## Serves for random generation of various things.

class RandomGenerator:

  ## Generates a random melody into given track of given section
  #  instance.
  #
  #  @param section_instance SectionInstance object that holds a track
  #         into which the melody will be generated
  #  @param track_number number of track into which the melody will be
  #         generated
  #  @param key list of note codes, sets the melody key
  #  @param seed random seed
  #  @param base_note sets the base note around which the melody will be
  #         built
  #  @param offset_factor double in range <0,1>, says how much the note
  #         pitch will be different between the generated notes, higher
  #         number will generate a melody with higher pitch range
  #  @param division_factor double in range <0,1>, affects how many
  #         times the melody line will be split into two, bigger number
  #         will produce a faster melody
  #  @param disharmonies double in range <0,1>, says how many
  #         disharmonies there will be

  def generate_melody(self,section_instance,track_number,key,seed,base_note = 40,offset_factor = 0.3,division_factor = 0.4,disharmonies = 0.02):
    random.seed(seed)

    probability_bar   = 0.55    # probability of generating a split at a bar start
    probability_bar2  = 0.2     # probability of generating a split at multiples of bar half
    probability_bar4  = 0.1     # probability of generating a split at multiples of bar quarter
    probability_skip  = 0.1     # probability of skipping a note
    probability_alter = 0.1     # probability of altering notes in repeating melody

    # sometimes make the melody repeat a little if possible:

    possible_repeat_counts = [1]

    for i in range(2,5):
      if section_instance.length_beats % i == 0:
        possible_repeat_counts.append(i)

    repeat_count = random.choice(possible_repeat_counts)  # by how many bars the melody will be repeated
    repeat_length = int(section_instance.length_beats / repeat_count)
    split_times = [0,repeat_length]       # will contain times of note starts

    for i in range(1,repeat_length * 4):  # go by quarters of a bar

      if i % 4 == 0:            # whole bar
        generate_split = random.random() <= probability_bar
      elif i % 2 == 0:          # bar half
        generate_split = random.random() <= probability_bar2
      else:                     # bar quarter
        generate_split = random.random() <= probability_bar4

      if generate_split:
        split_times.append(i * 0.25)

    split_times.sort()

    # generate the notes
    note_value = Note.closest_note_value(base_note + random.randint(-15,15),key)

    for i in range(len(split_times) - 1):
      if random.random() <= probability_skip:    # sometimes skip a note
        continue

      transpose_by = random.randint(-4,4)

      for j in range(repeat_count):
        new_note = Note(split_times[i] + j * repeat_length,split_times[i + 1] - split_times[i],note_value,100)
        new_note.transpose(key,transpose_by)

        if random.random() <= probability_alter:    # sometimes alter the note
          if random.random() <= 0.1:
            continue                                      # drop the note
          else:
            new_note.transpose(key,random.randint(-3,3))  # alter the pitch

        section_instance.tracks[track_number].add_note(new_note)

  ## Generates chords in to given track of given section instance.
  #
  #  @param section_instance section instance containing the track to
  #         generate the track into
  #  @param track_number number of track to generate the chords to
  #  @param key list of note codes, sets the key
  #  @param seed random seed
  #  @param repeat_after_bars after how many bars the chord pattern
  #         should be repeated

  def generate_chords(self,section_instance,track_number,key,seed,repeat_after_bars = 4):
    random.seed(seed)

    chord_bases = []     # will contain generated chord base notes
    current_note = Note.closest_note_value(random.randint(48,59),key)   # C to B

    # generate the base notes:
    for i in range(repeat_after_bars * section_instance.beats_in_bar):
      change_probability = 0.98 if i % section_instance.beats_in_bar == 0 else 0.07

      if random.random() < change_probability:   # change note
        current_note = Note.closest_note_value(random.randint(48,59),key)

      chord_bases.append(current_note)

    print("sasasa")
    print(chord_bases)

    # generate the actual notes:
    i = 0
    while i < len(chord_bases):
      if chord_bases[i] == None:
        continue

      time_start = i

      j = i + 1
      while j < len(chord_bases) and chord_bases[j] == chord_bases[i]:
        j += 1

      time_end = j

      upper_note = chord_bases[i] + 7

      middle_note = chord_bases[i] + 3

      if not middle_note in key:     # changes minor to major if needed
        middle_note += 1

      section_instance.tracks[track_number].add_note(Note(time_start,time_end - time_start,chord_bases[i],100))
      section_instance.tracks[track_number].add_note(Note(time_start,time_end - time_start,upper_note,100))
      section_instance.tracks[track_number].add_note(Note(time_start,time_end - time_start,middle_note,100))

      i = j

  ## Generates a rock beat track.
  #
  #  @param section_instance section instance containing the track to
  #         generate the track into
  #  @param track_number number of track to generate the beat to
  #  @param seed random seed
  #  @param speed how fast the beat will be (float, 0 - 1)
  #  @param strength how strong the beat will be (float, 0 - 1)

  def generate_rock_beat(self,section_instance,track_number,seed,speed = 0.5,strength = 0.8):
    random.seed(seed)

    # track beat pattern that will be repeated throughout the section:
    pattern_track = []

    # how many times the pattern will be repeated
    pattern_repeat = int(section_instance.length_beats / section_instance.beats_in_bar)

    hihat_cymbal = random.choice([NOTE_DRUM_HIHAT_CLOSED,NOTE_DRUM_HIHAT_PEDAL,NOTE_DRUM_CYMBAL_RIDE])

    if speed < 0.2:
      hihat_rythms = [2,4]
    elif speed < 0.5:
      hihat_rythms = [2]
    elif speed < 0.8:
      hihat_rythms = [1,2]
    else:
      hihat_rythms = [1]

    hihat_rythm = random.choice(hihat_rythms)

    for i in range(section_instance.beats_in_bar * 4):  # quarter-beat resolution
      pattern_track.append([])

      # assign probabilities:
      bass_probability = (0.8 if i == 0 else 0.08) + speed * 0.6
      snare_probability = (0.6 if (i + 4) % 8 == 0 else 0.03) + speed * 0.6
      hihat_probability = 0.99 if i % hihat_rythm == 0 else 0.02

      if i < 4:
        interchange_snare_and_bass = False
      else:
        interchange_snare_and_bass = True if random.random() < 0.2 else False

      # generate the pattern:
      if random.random() < bass_probability:
        pattern_track[-1].append(NOTE_DRUM_BASS if not interchange_snare_and_bass else NOTE_DRUM_SNARE)

      if random.random() < snare_probability:
        pattern_track[-1].append(NOTE_DRUM_SNARE if not interchange_snare_and_bass else NOTE_DRUM_BASS)

      if random.random() < hihat_probability:
        if random.random() < 0.98:                  # mostly hit the hihat but sometimes hit something else
          pattern_track[-1].append(hihat_cymbal)
        else:
          pattern_track[-1].append(random.choice([NOTE_DRUM_CYMBAL_RIDE,NOTE_DRUM_CYMBAL_RIDE_BELL]))

    # generate actual notes:

    for i in range(len(pattern_track)):
      for j in range(pattern_repeat):
        for note in pattern_track[i]:
          if random.random() < 0.05:    # sometimes drop the note to make the pattern a bit different
            continue

          section_instance.tracks[track_number].add_note(Note(j * section_instance.beats_in_bar + i / 4.0,0.1,note,int(strength * 128)))

    # add some cymbals:

    if strength >= 0.6:
      if random.random() < 0.8:
        start = random.choice([0,1])
        section_instance.tracks[track_number].add_note(Note(start,0.1,random.choice([NOTE_DRUM_CYMBAL_CRASH,NOTE_DRUM_CYMBAL_SPLASH]),80))
    elif strength >= 0.8:
      if random.random() < 0.99:
        start = random.choice([0,1])
        section_instance.tracks[track_number].add_note(Note(start,0.1,NOTE_DRUM_CYMBAL_CRASH,80))

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
    track.length_beats = self.length_beats
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
  ## Class method, gets a closest note value in given key to a given
  #  value.
  #
  #  @param value note value
  #  @param key key, a list of note values
  #  @return integer note value that is the closest to given value and
  #          is in given key

  def closest_note_value(value, key):
    if value in key:
      return value

    for i in range(100):
      if value + i in key:
        return value + i
      elif value - i in key:
        return value - i

    return 0

  def init_attributes(self):
    ## on what time the note starts, the value is in beats (float)
    self.start = 0.0
    ## duration of the note in beats (float)
    self.length = 0.25
    ## note "strength", integer 0 - 127
    self.velocity = 100
    ## MIDI note code (C3 = 60)
    self.note = 60

  ## Transposes the note respecting given key.
  #
  #  @param key key (the list of note values, see constants), the note
  #         must be in this key, otherwise nothing happens
  #  @param offset how many notes the note should be transposed,
  #         can be positive or negative integer

  def transpose(self,key,offset):
    increment_by = 1 if offset >= 0 else -1
    offset = abs(offset)

    while offset > 0:
      self.note += increment_by

      if not self.note in key:
        self.note += increment_by

      offset -= 1
    return

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

  ## Gets number of tracks that will be needed for the MIDI file
  #  (this is equal to number of instruments in the composition plus
  #  one for a special drum channel).
  #
  #  @return number of tracks for the composition

  def number_of_tracks(self):
    instrument_set = set()

    for section_instance in self.section_instances:
      for section_track in section_instance.tracks:
        instrument_set.add(section_track.instrument)

    return len(instrument_set) + 1

  ## Private function, maps track numbers to channels.

  def __track_number_to_channel(self,track_number):
    if track_number == 0:   # drums, channel 10 by MIDI specification
      return 9    # = 10 - 1
    elif track_number >= 10:
      return track_number   # = track_number - 1 + 1

    return track_number - 1

  def save_as_midi(self,filename):
    # it seems the midiutil library doesn't support time signature event so far :/

    number_of_tracks = self.number_of_tracks()
    midi = MIDIFile(number_of_tracks)
    section_offset = 0   # current section offset in beats
    track_instruments = [None for i in range(number_of_tracks)]         # holds track instruments

    # process all section instances:
    for section_instance in self.section_instances:
      for event in section_instance.meta_events:      # write events
        if event[1] == EVENT_TEMPO_CHANGE:
          for t in range(number_of_tracks):
            midi.addTempo(t,section_offset + event[0],event[2])

      for section_track in section_instance.tracks:
        track_number = 1   # which midi track to write the notes to

        if section_track.instrument == INSTRUMENT_ROCK_DRUMS:
          track_number = 0         # 0 is reserved for drums
        else:
          while track_number < number_of_tracks:      # find the appropriate track
            if track_instruments[track_number] == None:   # empty track - take it
              track_instruments[track_number] = section_track.instrument  # set the track to given instrument
              midi.addProgramChange(track_number,self.__track_number_to_channel(track_number),0,instrument_to_midi(section_track.instrument))
              break
            elif track_instruments[track_number] == section_track.instrument:  # appropriate track (the same instrument) - take it
              break

            track_number += 1

        # here we have the track number

        track_channel = self.__track_number_to_channel(track_number)

        for note in section_track.notes:
          midi.addNote(track_number,track_channel,note.note,section_offset + note.start,note.length,note.velocity)

      section_offset += section_instance.length_beats

    midi_file = open(filename,'wb')
    midi.writeFile(midi_file)
    midi_file.close()

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

r = RandomGenerator()
#print(r.generate_composition_structure(" aaaa [bbb ccccc dddddddd (XXXXXX YYYYYYY) ]{uniform(2,3)} (xxxx [(fufufu sesese) (popopo mumumu)]) eeeeeee{ uniform(2,3) } ffffff ",12315))
#r.generate_composition_structure("    rock (   (rock_chorus   | pop_chorus)[  uniform(2,3) ]  |   rock_bridge[10])   (rock_chorus(pop_chorus) ) ",12314)

c = Composition()

s = SectionInstance()
s2 = SectionInstance()

t1 = SectionTrack()
t2 = SectionTrack()
t3 = SectionTrack()
t4 = SectionTrack()

t1.instrument = INSTRUMENT_PIANO
t2.instrument = INSTRUMENT_STRINGS
t3.instrument = INSTRUMENT_STRINGS
t4.instrument = INSTRUMENT_ROCK_DRUMS

s.length_beats = 30

s.add_track(t1)
s.add_track(t2)
s.add_track(t3)
s.add_track(t4)

seed = 20

r.generate_melody(s,0,KEY_C_NOTES,seed)
r.generate_rock_beat(s,3,seed,0.6,0.8)
r.generate_chords(s,2,KEY_C_NOTES,seed)

t5 = SectionTrack()
t6 = SectionTrack()

t5.instrument = INSTRUMENT_EBASS
t6.instrument = INSTRUMENT_EBASS

s2.add_track(t5)
s2.add_track(t6)

s.add_meta_event(0.0,EVENT_TEMPO_CHANGE,60)
s2.add_meta_event(1.0,EVENT_TEMPO_CHANGE,120)

c.add_section_instance(s)
c.add_section_instance(s2)

print(c)
print(c.number_of_tracks())

c.save_as_midi("test.mid")
