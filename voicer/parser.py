import winsound

stringClient = input("Номер тикета (Х-YYY): ")
lstClient = []
stringCabinet = input("Номер кабинета (ХXX): ")
stringWindow = input("Номер окна (Х): ")

for letter in stringClient:
    lstClient.append(letter)

print(lstClient)
print(stringCabinet)
print(stringWindow)

play(client.wav)
play()
play(cabinet.wav)
play()
play(window.wav)
play()
