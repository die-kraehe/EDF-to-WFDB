import sys
import pyedflib as pedf
import numpy as np
import math
import wfdb

def edf2wfdb(inname,outname):
    "Converts a EDF File to a WFDB Header,Data File"
    try:
        #Liest Header und Signal der EDF Datei
        Reader = pedf.EdfReader(inname)
        #Dient als Record Obj zum schreiben der WFDB header und data File
        edf_record= wfdb.Record()

        #Helfer Variablen
        n_signals = len(Reader.getSignalLabels())
        p_max = Reader.getPhysicalMaximum()
        p_min = Reader.getPhysicalMinimum()
        d_max = Reader.getDigitalMaximum()
        d_min = Reader.getDigitalMinimum()

        #Make Digital Signals
        digital_signals = [Reader.readSignal(i,digital= True) for i in range(n_signals)]
        d_signals = np.stack(digital_signals,axis=1)

        #Dummy Record Obj mit allen wichtigen Infos der EDF beladen
        #Signal Data
        edf_record.d_signal = d_signals
        edf_record.fs = Reader.getSampleFrequencies()[0]
        edf_record.sig_name = Reader.getSignalLabels()
        edf_record.n_sig = n_signals
        edf_record.sig_len = Reader.getNSamples()[0]
        edf_record.block_size = n_signals * [0]
        edf_record.units = [Reader.getPhysicalDimension(i) for i in range(n_signals)]
        edf_record.init_value = [d_signals[x][0] for x in range(n_signals)]
        edf_record.checksum = [int(np.sum(v) % 65536) for v in np.transpose(d_signals)]

        #ADC -Einstellungen
        adc_gain_all = ((d_max - d_min) / (p_max - p_min))
        edf_record.adc_gain = [float(format(a,'.12g')) for a in adc_gain_all]
        edf_record.fmt = ['16' for _ in range(n_signals)]
        edf_record.skew = n_signals * [None]
        edf_record.byte_offset = n_signals * [None]
        edf_record.adc_res = [int(math.log2(f)) for f in (d_max - d_min)]
        edf_record.adc_zero = [0 for _  in range(n_signals)]
        edf_record.baseline = [0 for _ in range(n_signals)]

        # Ausgabe Namen Festlegen
        edf_record.record_name = outname
        edf_record.file_name = [outname+".dat" for _ in range(n_signals)]

        #Write both necessary Files
        edf_record.wrheader(write_dir="tmp")
        edf_record.wrsamp(write_dir="tmp")

    except OSError as fehler:
        print(fehler)
    except:
        print("Something Unexpected Happened")
    finally:
        Reader.close()

def _main(args):
    if args:
        if '-o' in args and '-i' in args:

            split_index = args.index('-o')
            i_names = args[1:split_index]
            o_names = args[split_index+1:]

            if len(i_names) == len(o_names):
                for i_name, o_name in zip(i_names,o_names):
                    edf2wfdb(i_name,o_name)
            else:
                print("Eingabe Dateien können nicht zu output gematched werden")
        else:
            print("Eingabe von -i oder -o vergessen")

    else:
        print(f"Usage: {sys.argv[0]} -i input.edf [...] -o output [...]")

if __name__ == '__main__':
    _main(sys.argv[1:])