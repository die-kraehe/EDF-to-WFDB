import wfdb

#Wenn die edf2mit Funktion funktioniert läuft das ganze ohne Probleme und ohne zu hässlichen Code
#109.edf -> Einziges Beispiel Datei mit dem das ganze funktioniert
edf_record = wfdb.edf2mit("109.edf")

#Hier sind nur die notwendigen Parameter gesetzt
#Würde man das ganze richtig Implementieren müsste man noch ADC_Gain usw setzten
edf_record.baseline = [0,0]
edf_record.adc(inplace=True)
edf_record.wrheader(write_dir="tmp")
edf_record.wrsamp(write_dir="tmp")