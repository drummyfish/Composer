try:
  # for Python2
  from Tkinter import *
except ImportError:
  # for Python3
  from tkinter import *

import composer


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

    instrument_options = ["piano", "guitar", "strings", "brass"]

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

    key_options = [
        "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    self.var_key.set(key_options[0])
    OptionMenu(frame, self.var_key, key_options[0],
               key_options[1], key_options[2], key_options[3],
               key_options[4], key_options[5], key_options[6],
               key_options[7], key_options[8], key_options[9],
               key_options[10], key_options[11]).grid(row=3, column=1, sticky=W)

    Label(frame, text="signature").grid(
        row=4, column=general_column, sticky=W)

    signature_options = ["4/4", "3/4"]
    self.var_signature.set(signature_options[0])
    OptionMenu(frame, self.var_signature, signature_options[0], signature_options[
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
        row=6, column=melody_column, sticky=W)

    self.var_melody_instrument.set(instrument_options[0])
    OptionMenu(frame, self.var_melody_instrument, instrument_options[0], instrument_options[
               1], instrument_options[2], instrument_options[3]).grid(row=6, column=melody_column + 1, sticky=W)

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
        row=6, column=chords_column, sticky=W)

    self.var_chords_instrument.set(instrument_options[2])
    OptionMenu(frame, self.var_chords_instrument, instrument_options[0], instrument_options[
               1], instrument_options[2], instrument_options[3]).grid(row=6, column=chords_column + 1, sticky=W)

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
        row=4, column=harmony_column, sticky=W)
    Scale(frame, from_=0, to=100, orient=HORIZONTAL, var=self.var_harmony_range).grid(
        row=4, column=harmony_column + 1, sticky=W)

    Label(frame, text="instrument").grid(
        row=6, column=chords_column, sticky=W)

    self.var_harmony_instrument.set(instrument_options[3])
    OptionMenu(frame, self.var_harmony_instrument, instrument_options[0], instrument_options[
               1], instrument_options[2], instrument_options[3]).grid(row=6, column=harmony_column + 1, sticky=W)

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

    section_instance.add_meta_event(0,composer.EVENT_TEMPO_CHANGE,self.var_tempo.get())

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

    if self.var_key.get == "C":
      key = composer.KEY_C_NOTES
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

root = Tk()
app = Gui(root)
root.mainloop()
