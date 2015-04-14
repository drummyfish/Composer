try:
  # for Python2
  from Tkinter import *
except ImportError:
  # for Python3
  from tkinter import *

import composer
import random

class Gui:

  def __init__(self, master):
    frame = Frame(master)
    master.wm_title("little composer")
    master.resizable(width=FALSE, height=FALSE)
    frame.pack()

    self.var_tempo = IntVar(master)
    self.var_key = StringVar(master)
    self.var_length = IntVar(master)
    self.var_signature = StringVar(master)
    self.var_seed = IntVar(master)
    self.var_drums = BooleanVar(master)
    self.var_drums_speed = IntVar(master)
    self.var_drums_strength = IntVar(master)
    self.var_melody = BooleanVar(master)
    self.var_melody_speed = IntVar(master)
    self.var_melody_range = IntVar(master)
    self.var_melody_base_note = IntVar(master)
    self.var_melody_disharmonies = IntVar(master)
    self.var_melody_instrument = StringVar(master)
    self.var_chords = BooleanVar(master)
    self.var_chords_pattern_length = IntVar(master)
    self.var_chords_seventh_factor = IntVar(master)
    self.var_chords_speed = IntVar(master)
    self.var_chords_fullness = IntVar(master)
    self.var_chords_instrument = StringVar(master)
    self.var_harmony = BooleanVar(master)
    self.var_harmony_speed = IntVar(master)
    self.var_harmony_range = IntVar(master)
    self.var_harmony_fullness = IntVar(master)
    self.var_harmony_base_note = IntVar(master)
    self.var_harmony_harmony_factor = IntVar(master)
    self.var_harmony_instrument = StringVar(master)
    self.var_bass = BooleanVar(master)
    self.var_bass_speed = BooleanVar(master)
    self.var_bass_strength = BooleanVar(master)

    self.instrument_options = ["piano", "guitar", "strings", "brass"]

    # default values:
    self.var_drums.set(True)
    self.var_melody.set(True)
    self.var_harmony.set(True)
    self.var_chords.set(True)
    self.var_bass.set(True)
    self.var_length.set(30)
    self.var_tempo.set(120)
    self.var_drums_speed.set(65)
    self.var_drums_strength.set(85)
    self.var_melody_speed.set(80)
    self.var_melody_range.set(30)
    self.var_melody_base_note.set(60)
    self.var_melody_disharmonies.set(5)
    self.var_chords_speed.set(50)
    self.var_chords_fullness.set(80)
    self.var_chords_pattern_length.set(4)
    self.var_chords_seventh_factor.set(10)
    self.var_harmony_speed.set(75)
    self.var_harmony_range.set(30)
    self.var_harmony_base_note.set(70)
    self.var_harmony_harmony_factor.set(95)
    self.var_bass_strength.set(80)
    self.var_bass_speed.set(40)

    # general:
    general_column = 0
    Label(frame, text="general").grid(
        row=1, column=general_column, sticky=W)
    Label(frame, text="tempo").grid(row=2, column=general_column, sticky=W)
    Scale(frame, from_=50, to=300, var=self.var_tempo, orient=HORIZONTAL).grid(
        row=2, column=general_column + 1, sticky=W)
    Label(frame, text="key").grid(row=3, column=general_column, sticky=W)

    self.key_options = [
        "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    self.var_key.set(self.key_options[0])
    OptionMenu(frame, self.var_key, self.key_options[0],
               self.key_options[1], self.key_options[2], self.key_options[3],
               self.key_options[4], self.key_options[5], self.key_options[6],
               self.key_options[7], self.key_options[8], self.key_options[9],
               self.key_options[10], self.key_options[11]).grid(row=3, column=1, sticky=W)

    Label(frame, text="signature").grid(
        row=4, column=general_column, sticky=W)

    self.signature_options = ["4/4", "3/4"]
    self.var_signature.set(self.signature_options[0])
    OptionMenu(frame, self.var_signature, self.signature_options[0], self.signature_options[
               1]).grid(row=4, column=general_column + 1, sticky=W)

    Label(frame, text="length (beats)").grid(
        row=5, column=general_column, sticky=W)
    Scale(frame, from_=1, to=100, orient=HORIZONTAL, var=self.var_length).grid(
        row=5, column=general_column + 1, sticky=W)

    Label(frame, text="filename").grid(
        row=6, column=general_column, sticky=W)
    self.text_filename = Text(frame, height=1, width=20)
    self.text_filename.grid(row=6, column=general_column + 1, sticky=W)
    self.text_filename.insert(END, "output.midi")

    Label(frame, text="seed").grid(row=7, column=general_column, sticky=W)
    Scale(frame, from_=0, to=65535, orient=HORIZONTAL, var=self.var_seed).grid(
        row=7, column=general_column + 1, sticky=W)

    Button(frame, text="generate", command=self.button_clicked).grid(
        row=8, columnspan=2, sticky=W)

    # drums column:
    drum_column = 2
    Checkbutton(frame, text="drums", var=self.var_drums).grid(
        row=1, column=drum_column, sticky=W)

    Label(frame, text="speed").grid(row=2, column=drum_column, sticky=W)
    Scale(frame, from_=0, to=100, orient=HORIZONTAL, var=self.var_drums_speed).grid(
        row=2, column=drum_column + 1, sticky=W)

    Label(frame, text="strength").grid(row=3, column=drum_column, sticky=W)
    Scale(frame, from_=0, to=100, orient=HORIZONTAL, var=self.var_drums_strength).grid(
        row=3, column=drum_column + 1, sticky=W)

    # melody column:
    melody_column = 4

    Checkbutton(frame, text="melody", var=self.var_melody).grid(
        row=1, column=melody_column, sticky=W)

    Label(frame, text="base note").grid(
        row=2, column=melody_column, sticky=W)
    Scale(frame, from_=20, to=120, orient=HORIZONTAL, var=self.var_melody_base_note).grid(
        row=2, column=melody_column + 1, sticky=W)

    Label(frame, text="range").grid(row=3, column=melody_column, sticky=W)
    Scale(frame, from_=0, to=100, orient=HORIZONTAL, var=self.var_melody_range).grid(
        row=3, column=melody_column + 1, sticky=W)

    Label(frame, text="speed").grid(row=4, column=melody_column, sticky=W)
    Scale(frame, from_=0, to=100, orient=HORIZONTAL, var=self.var_melody_speed).grid(
        row=4, column=melody_column + 1, sticky=W)

    Label(frame, text="disharmonies").grid(
        row=5, column=melody_column, sticky=W)
    Scale(frame, from_=0, to=100, orient=HORIZONTAL, var=self.var_melody_disharmonies).grid(
        row=5, column=melody_column + 1, sticky=W)

    Label(frame, text="instrument").grid(
        row=7, column=melody_column, sticky=W)

    self.var_melody_instrument.set(self.instrument_options[0])
    OptionMenu(frame, self.var_melody_instrument, self.instrument_options[0], self.instrument_options[
               1], self.instrument_options[2], self.instrument_options[3]).grid(row=7, column=melody_column + 1, sticky=W)

    # chords column:
    chords_column = 6
    Checkbutton(frame, text="chords", var=self.var_chords).grid(
        row=1, column=chords_column, sticky=W)

    Label(frame, text="pattern length (bars)").grid(
        row=2, column=chords_column, sticky=W)
    Scale(frame, from_=0, to=100, orient=HORIZONTAL, var=self.var_chords_pattern_length).grid(
        row=2, column=chords_column + 1, sticky=W)

    Label(frame, text="speed").grid(row=3, column=chords_column, sticky=W)
    Scale(frame, from_=0, to=100, orient=HORIZONTAL, var=self.var_chords_speed).grid(
        row=3, column=chords_column + 1, sticky=W)

    Label(frame, text="fullness").grid(
        row=4, column=chords_column, sticky=W)
    Scale(frame, from_=0, to=100, orient=HORIZONTAL, var=self.var_chords_fullness).grid(
        row=4, column=chords_column + 1, sticky=W)

    Label(frame, text="seventh factor").grid(
        row=5, column=chords_column, sticky=W)
    Scale(frame, from_=0, to=100, orient=HORIZONTAL, var=self.var_chords_seventh_factor).grid(
        row=5, column=chords_column + 1, sticky=W)

    Label(frame, text="instrument").grid(
        row=7, column=chords_column, sticky=W)

    self.var_chords_instrument.set(self.instrument_options[2])
    OptionMenu(frame, self.var_chords_instrument, self.instrument_options[0], self.instrument_options[
               1], self.instrument_options[2], self.instrument_options[3]).grid(row=7, column=chords_column + 1, sticky=W)

    # harmony column:
    harmony_column = 8

    Checkbutton(frame, text="harmony", var=self.var_harmony).grid(
        row=1, column=harmony_column, sticky=W)

    Label(frame, text="base note").grid(
        row=2, column=harmony_column, sticky=W)
    Scale(frame, from_=20, to=120, orient=HORIZONTAL, var=self.var_harmony_base_note).grid(
        row=2, column=harmony_column + 1, sticky=W)

    Label(frame, text="speed").grid(row=3, column=harmony_column, sticky=W)
    Scale(frame, from_=0, to=100, orient=HORIZONTAL, var=self.var_harmony_speed).grid(
        row=3, column=harmony_column + 1, sticky=W)

    Label(frame, text="fullness").grid(
        row=4, column=harmony_column, sticky=W)
    Scale(frame, from_=0, to=100, orient=HORIZONTAL, var=self.var_harmony_fullness).grid(
        row=4, column=harmony_column + 1, sticky=W)

    Label(frame, text="harmony range").grid(
        row=5, column=harmony_column, sticky=W)
    Scale(frame, from_=0, to=100, orient=HORIZONTAL, var=self.var_harmony_range).grid(
        row=5, column=harmony_column + 1, sticky=W)

    Label(frame, text="harmony factor").grid(
        row=6, column=harmony_column, sticky=W)
    Scale(frame, from_=0, to=100, orient=HORIZONTAL, var=self.var_harmony_harmony_factor).grid(
        row=6, column=harmony_column + 1, sticky=W)

    Label(frame, text="instrument").grid(
        row=7, column=chords_column, sticky=W)

    self.var_harmony_instrument.set(self.instrument_options[3])
    OptionMenu(frame, self.var_harmony_instrument, self.instrument_options[0], self.instrument_options[
               1], self.instrument_options[2], self.instrument_options[3]).grid(row=7, column=harmony_column + 1, sticky=W)

    # bass column:
    bass_column = 10

    Checkbutton(frame, text="bass", var=self.var_bass).grid(
        row=1, column=bass_column, sticky=W)

    Label(frame, text="base speed").grid(
        row=2, column=bass_column, sticky=W)
    Scale(frame, from_=0, to=100, orient=HORIZONTAL, var=self.var_bass_speed).grid(
        row=2, column=bass_column + 1, sticky=W)

    Label(frame, text="base strength").grid(
        row=3, column=bass_column, sticky=W)
    Scale(frame, from_=0, to=100, orient=HORIZONTAL, var=self.var_bass_strength).grid(
        row=3, column=bass_column + 1, sticky=W)

    # create the MIDI image:

    self.midi_image_size = (800,160)
    self.midi_image = PhotoImage(width=self.midi_image_size[0], height=self.midi_image_size[1])
    self.canvas = Canvas(frame, width=self.midi_image_size[0], height=self.midi_image_size[1], bg="#000000")
    self.canvas.grid(row=8, column=1, columnspan=6)
    self.canvas.create_image((self.midi_image_size[0]/2 + 2, self.midi_image_size[1]/2 + 2), image=self.midi_image, state="normal")

    self.__redraw_midi_image(None)

    Label(frame, text="Miloslav 'tastyfish' Ciz, 2015").grid(
        row=9, column=1, sticky=W)

    Button(frame, text="randomize", command=self.randomize).grid(
        row=9, column=0, sticky=W)

  def fill(self, image, color):
    r,g,b = color
    width = image.width()
    height = image.height()
    hexcode = "#%02x%02x%02x" % (r,g,b)
    horizontal_line = "{" + " ".join([hexcode]*width) + "}"
    image.put(" ".join([horizontal_line]*height))

  def randomize(self):
    self.var_drums.set(random.random() < 0.5)
    self.var_melody.set(random.random() < 0.5)
    self.var_harmony.set(random.random() < 0.5)
    self.var_chords.set(random.random() < 0.5)
    self.var_bass.set(random.random() < 0.5)
    self.var_length.set(random.randint(10,60))
    self.var_tempo.set(random.randint(80,140))
    self.var_drums_speed.set(random.randint(0,100))
    self.var_drums_strength.set(random.randint(30,100))
    self.var_melody_speed.set(random.randint(0,100))
    self.var_melody_range.set(random.randint(0,100))
    self.var_melody_base_note.set(random.randint(0,100))
    self.var_melody_disharmonies.set(random.randint(0,100))
    self.var_chords_speed.set(random.randint(0,100))
    self.var_chords_fullness.set(random.randint(0,100))
    self.var_chords_pattern_length.set(random.randint(2,6))
    self.var_chords_seventh_factor.set(random.randint(0,100))
    self.var_harmony_speed.set(random.randint(0,100))
    self.var_harmony_range.set(random.randint(0,100))
    self.var_harmony_fullness.set(random.randint(0,100))
    self.var_harmony_base_note.set(random.randint(0,100))
    self.var_harmony_harmony_factor.set(random.randint(70,100))
    self.var_bass_strength.set(random.randint(0,100))
    self.var_bass_speed.set(random.randint(0,100))
    self.var_seed.set(random.randint(0,65535))

    self.var_key.set(random.choice(self.key_options))
    self.var_signature.set(random.choice(self.signature_options))
    self.var_melody_instrument.set(random.choice(self.instrument_options))
    self.var_chords_instrument.set(random.choice(self.instrument_options))
    self.var_harmony_instrument.set(random.choice(self.instrument_options))

  def __redraw_midi_image(self, section_instance):
    self.fill(self.midi_image,(255,255,255))

    if section_instance == None:
      return

    colors = ["#E31717", "#27D613", "#3160EB", "#EBDB31", "#DF61ED"]
    color_index = 0

    next_bar = section_instance.beats_in_bar

    for i in range(self.midi_image_size[0]):
      position = i / float(self.midi_image_size[0] - 1) * section_instance.length_beats

      if position >= next_bar:
        next_bar += section_instance.beats_in_bar

        for j in range(self.midi_image_size[1]):
          self.midi_image.put("#C9C9C9", (i,j))

      color_index = 0

      for track in section_instance.tracks:
        color = colors[color_index]

        color_index = (color_index + 1) % len(colors)

        notes = track.notes_at(position)

        for note in notes:
          y = self.midi_image_size[1] - note

          if y >= 0 and y < self.midi_image_size[1]:
            self.midi_image.put(color, (i,y))

  def __string_to_instrument(self, instrument_string):
    if instrument_string == "guitar":
      return composer.INSTRUMENT_GUITAR
    elif instrument_string == "strings":
      return composer.INSTRUMENT_STRINGS
    elif instrument_string == "brass":
      return composer.INSTRUMENT_BRASS

    return composer.INSTRUMENT_PIANO

  def button_clicked(self):
    generator = composer.RandomGenerator()
    composition = composer.Composition()
    section_instance = composer.SectionInstance()

    section_instance.add_meta_event(0, composer.EVENT_TEMPO_CHANGE, self.var_tempo.get())

    if self.var_signature.get() == "3/4":
      section_instance.beats_in_bar = 3

    track1 = composer.SectionTrack()
    track2 = composer.SectionTrack()
    track3 = composer.SectionTrack()
    track4 = composer.SectionTrack()
    track5 = composer.SectionTrack()

    track1.instrument = composer.INSTRUMENT_ROCK_DRUMS
    track2.instrument = self.__string_to_instrument(
        self.var_chords_instrument.get())
    track3.instrument = self.__string_to_instrument(
        self.var_melody_instrument.get())
    track4.instrument = self.__string_to_instrument(
        self.var_harmony_instrument.get())
    track5.instrument = composer.INSTRUMENT_EBASS

    section_instance.add_track(track1)
    section_instance.add_track(track2)
    section_instance.add_track(track3)
    section_instance.add_track(track4)
    section_instance.add_track(track5)

    section_instance.length_beats = self.var_length.get()

    if self.var_key.get() == "C":
      key = composer.KEY_C_NOTES
    elif self.var_key.get() == "C#":
      key = composer.KEY_DB_NOTES
    elif self.var_key.get() == "D":
      key = composer.KEY_D_NOTES
    elif self.var_key.get() == "E":
      key = composer.KEY_E_NOTES
    elif self.var_key.get() == "F":
      key = composer.KEY_F_NOTES
    elif self.var_key.get() == "F#":
      key = composer.KEY_GB_NOTES
    elif self.var_key.get() == "G":
      key = composer.KEY_G_NOTES
    elif self.var_key.get() == "G#":
      key = composer.KEY_AB_NOTES
    elif self.var_key.get() == "A":
      key = composer.KEY_A_NOTES
    elif self.var_key.get() == "A#":
      key = composer.KEY_BB_NOTES
    elif self.var_key.get() == "B":
      key = composer.KEY_B_NOTES
    else:
      key = composer.KEY_C_NOTES

    generator.generate_rock_beat(section_instance, 0, self.var_seed.get(
    ), self.var_drums_speed.get() / 100.0, self.var_drums_strength.get() / 100.0)
    generator.generate_chords(section_instance, 1, key, self.var_seed.get(), self.var_chords_pattern_length.get(
    ), self.var_chords_seventh_factor.get() / 100.0, self.var_chords_fullness.get() / 100.0, self.var_chords_speed.get() / 100.0)
    generator.generate_melody(section_instance, 2, key, self.var_seed.get(), self.var_melody_base_note.get(
    ), self.var_melody_range.get() / 100.0, self.var_melody_speed.get() / 100.0, self.var_melody_disharmonies.get() / 100.0)
    generator.generate_harmonies(section_instance, 3, 1, key, self.var_seed.get(), self.var_harmony_base_note.get(), self.var_harmony_harmony_factor.get(
    ) / 100.0, self.var_harmony_range.get() / 100.0, self.var_harmony_speed.get() / 100.0, self.var_harmony_fullness.get() / 100.0)
    generator.generate_bass(section_instance, 4, 1, key, self.var_seed.get(), self.var_bass_speed.get() / 100.0, self.var_bass_strength.get() / 100.0)

    if not self.var_drums.get():
      section_instance.remove_track(track1)

    if not self.var_chords.get():
      section_instance.remove_track(track2)

    if not self.var_melody.get():
      section_instance.remove_track(track3)

    if not self.var_harmony.get():
      section_instance.remove_track(track4)

    if not self.var_bass.get():
      section_instance.remove_track(track5)

    composition.add_section_instance(section_instance)

    composition.save_as_midi(self.text_filename.get("1.0", END)[:-1])

    self.__redraw_midi_image(section_instance)

root = Tk()
app = Gui(root)
root.mainloop()
