import sys
import wfdb

def edf2wfdb(inname,outname):
    "Converts a EDF File to a WFDB Header,Data File"
    try:
        #Liest Header und Signal der EDF Datei
        towrite_edf = wfdb.edf2mit(inname)

        #Helfer Variablen
        zero_array = [0 for _  in range(towrite_edf.n_sig)]

        #Vereinfachte Annahme ADC_Zero = 0 Baseline = 0
        towrite_edf.adc_zero = zero_array
        towrite_edf.baseline = zero_array

        # Ausgabe Namen Festlegen
        towrite_edf.record_name = outname
        towrite_edf.file_name = [outname+".dat" for _ in range(towrite_edf.n_sig)]

        towrite_edf.adc(inplace = True)
        #Write both necessary Files
        towrite_edf.wrheader()
        towrite_edf.wrsamp()

    except OSError as fehler:
        print(fehler)
    except:
        print("Something Unexpected Happened")


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