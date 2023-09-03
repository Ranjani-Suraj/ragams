import main
import audio_processing

filename = input("Enter the file name: ")
#notes = main.returnNotes(filename)
notes = main.returnNotes("Kalyani.wav")

#carnatic music notes -
#S (Shadjam) - C (261.63Hz) 60
#R (Rishabam) is of three types namely: Shuddha Rishabam, Chatushruti Rishabam and Shatshruti Rishabam. - C#(276) 61, D(293.66) 62, D#(310)63 
#G (Gaandaaram) is of three types namely: Shuddha Gandharam G1, Sadhaarana Gaandaaram G2 and Anthara Gaandaaram G3. -D(293.66)62,  D#(311)63, E(327) 64
#M (Madhyamam) is of two types, Shuddha Madhyamam M1 and Prathi Madhyamam M2. - F(349) 65, F#(368) 66
#D (Daivatham) is of three types, Shuddha Daivatham D1, Chathushruthi Daivatham D2, and shatshruthi daivatham D3. - Ab 68 (415), A(436) 69, A#(446.16) 70
#N (Nishaadam) is of t2 types, Kaakali Nishaadam N3 and Kaishiki Nishaadam N2. - B(493) 71, Bb(466.16)70
#P (Panchamam) - G(392) 67

#remove duplicates in notes[]
notes.sort()
for i in range(len(notes)):
    if notes[i]<60:
        i+=10
        continue
    freq = notes.count(notes[i])
    for j in range(i+1, freq+i):
        notes.remove(notes[i])
    if i == len(notes) - 1 or notes[i]>71:
        break

ragam = []
indu = [('Ratnangi', [60,61,62,65,67,68,70]),('Ganamurti', [60,61,62,65,67,68,71]),('Vanaspati', [60,61,62,65,67,69,70]),('Manavati', [60,61,62,65,67,69,71]),('Tanarupi', [60,61,62,65,67,70,71])]
netra = [('Hanumatodi', [60,61,63,65,67,68,70]),('Dhenuka', [60,61,63,65,67,68,71]),('Natakapriya', [60,61,63,65,67,69,70]),('Kokilapriya', [60,61,63,65,67,69,71]),('Rupavati', [60,61,63,65,67,70,71])]
agni = [('Vakulabharanam', [60,61,64,65,67,68,70]),('Mayamalavagowla', [60,61,64,65,67,68,71]),('Chakravakum', [60,61,64,65,67,69,70]),('Suryakantam', [60,61,64,65,67,69,71]),('Hatakambari', [60,61,64,65,67,70,71])]
veda = [('Natabhairavi', [60,62,63,65,67,68,70]),('Keeravani', [60,62,63,65,67,68,71]),('Kharaharapriya', [60,62,63,65,67,69,70]),('Gowrimanohari', [60,62,63,65,67,69,71]),('Varunapriya', [60,62,63,65,67,70,71])]
bana = [('Charukesi', [60,62,64,65,67,68,70]),('Sarasangi', [60,62,64,65,67,68,71]),('Harikamboji', [60,62,64,65,67,69,70]),('Shankarabaranam', [60,62,64,65,67,69,71]),('Naganandini', [60,62,64,65,67,70,71])]
rutu = [('Ragavardhani', [60,63,64,65,67,68,70]),('Gangeyabhushani', [60,63,64,65,67,68,71]),('Vagadheeshwari', [60,63,64,65,67,69,70]),('Soolini', [60,63,64,65,67,69,71]),('Chalanta', [60,63,64,65,67,70,71])]

rishi = [('Jalarnavam', [60,61,62,66,67,68,70]),('Jhalavarali', [60,61,62,66,67,68,71]),('Navaneetam', [60,61,62,66,67,69,70]),('Pavani', [60,61,62,66,67,69,71]),('Raghupriya', [60,61,62,66,67,70,71])]
vasu =  [('Bhavapriya', [60,61,63,66,67,68,70]),('Subhapantuvarali', [60,61,63,66,67,68,71]),('Shadvidhamargini', [60,61,63,66,67,69,70]),('Suvarnangi', [60,61,63,66,67,69,71]),('Divyamani', [60,61,63,66,67,70,71])]
bhamha =  [('Namanarayani', [60,61,64,66,67,68,70]),('Kamavardini', [60,61,64,66,67,68,71]),('Rampriya', [60,61,64,66,67,69,70]),('Gamanasrama', [60,61,64,66,67,69,71]),('Viswambari', [60,61,64,66,67,70,71])]
dishi = [('Shanmukapriya', [60,62,63,66,67,68,70]),('Simhendramadyamam', [60,62,63,66,67,68,71]),('Hemavati', [60,62,63,66,67,69,70]),('Dharmavati', [60,62,63,66,67,69,71]),('Neetimati', [60,62,63,66,67,70,71])]
rudra = [('Rishabhapriya', [60,62,64,66,67,68,70]),('Latangi', [60,62,64,66,67,68,71]),('Vachaspati', [60,62,64,66,67,69,70]),('Kalyani', [60,62,64,66,67,69,71]),('Chitambari', [60,62,64,66,67,70,71])]
aditya = [('Jyotiswaroopini', [60,63,64,66,67,68,70]),('Dhatuvardini', [60,63,64,66,67,68,71]),('Nasikabhooshini', [60,63,64,66,67,69,70]),('Kosalam', [60,63,64,66,67,69,71]),('Rasikapriya', [60,63,64,66,67,70,71])]

name = ""
if 65 in notes: #if it has shuddha madyamam:
    if 61 in notes: # if it has shuddha rishabham
        if 62 in notes: #if it has shuddha gandharam
            ragam.extend(indu)
        elif 63 in notes: #if it has saadharana gaandharam
            ragam.extend(netra)
        elif 64 in notes: #if it has anthara gaandharam
            ragam.extend(agni)
    elif 62 in notes: # if it has chatushruthi rishabham
        if 63 in notes: #if it has saadharana gaandharam
            ragam.extend(veda)
        elif 64 in notes: #if it has anthara gaandharam
            ragam.extend(bana)
    elif 63 in notes: # if it has shatshruti rishabham
        ragam.extend(rutu)
                
elif 66 in notes: # if it has prathi madhyamum
    if 61 in notes: # if it has shuddha rishabham
        if 62 in notes: #if it has shuddha gandharam
            ragam.extend(rishi)
        elif 63 in notes: #if it has saadharana gaandharam
            ragam.extend(vasu)
        elif 64 in notes: #if it has anthara gaandharam
            ragam.extend(bramha)
    elif 62 in notes: # if it has chatushruthi rishabham
        if 63 in notes: #if it has saadharana gaandharam
            ragam.extend(dishi)
        elif 64 in notes: #if it has anthara gaandharam
            ragam.extend(rudra)
    elif 63 in notes: # if it has shatshruti rishabham
        ragam.extend(aditya)

#finding correct arohanam
for i in ragam:
    if i[1] in notes:
        name = i[0]

print("Ragam name:", name)





