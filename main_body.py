from main import *
import logging 

logging.basicConfig(level=logging.DEBUG)
song_chords = [["hamsadwani", returnNotes("Hamsadwani.wav")],["Kalyani", returnNotes("Kalyani.wav")],
               ["Mayamalavagowla", returnNotes("mayamalavagowla.wav")]]
nm = input("Enter the file name of the wav file: ")+".wav"
notes = returnNotes(nm)
#outer loop: going through elements of song_chords[].
#max_compat = 0, c==0
#Inner loop 1: x = len(notes). Going through all notes of pitches in groups of x. y= abs(pitch[c]-notes[j]), compat+y, c++. if compat<max_compat, max_compat = compat.
max_compat = 0
most_compat = song_chords[0][0]
c=0
compat = 0
for song in range(0, len(song_chords)):
      for i in range(0, len(song_chords[1])-len(notes), 10):
          for j in range(i, len(notes)):
              len_snippet = len(notes)
              diff = abs(song_chords[1][c] - notes[j])
              compat += diff
          if compat<max_compat:
              max_compat = compat
              most_compat = song_chords[song][0]
          compat = 0
          c+=1
print("Your song is probably:",most_compat)