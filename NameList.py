class NameList:
    def __init__(self):
        self.name_list = "TIME,REAL 1,IMAGINARY 1,PHASE 1,SYSTEM PHASE 1,IMPEDANCE 1,REAL 2,IMAGINARY 2,PHASE 2,SYSTEM PHASE 2," \
                         "IMPEDANCE 2,REAL 3,IMAGINARY 3,PHASE 3,SYSTEM PHASE 3,IMPEDANCE 3,REAL 4,IMAGINARY 4,PHASE 4," \
                         "SYSTEM PHASE 4,IMPEDANCE 4,REAL 5,IMAGINARY 5,PHASE 5,SYSTEM PHASE 5,IMPEDANCE 5,REAL 6," \
                         "IMAGINARY 6,PHASE 6,SYSTEM PHASE 6,IMPEDANCE 6,REAL 7,IMAGINARY 7,PHASE 7,SYSTEM PHASE 7," \
                         "IMPEDANCE 7,REAL 8,IMAGINARY 8,PHASE 8,SYSTEM PHASE 8,IMPEDANCE 8,REAL 9,IMAGINARY 9,PHASE 9," \
                         "SYSTEM PHASE 9,IMPEDANCE 9,REAL 10,IMAGINARY 10,PHASE 10,SYSTEM PHASE 10,IMPEDANCE 10,REAL 11," \
                         "IMAGINARY 11,PHASE 11,SYSTEM PHASE 11,IMPEDANCE 11,REAL 12,IMAGINARY 12,PHASE 12,SYSTEM PHASE 12," \
                         "IMPEDANCE 12,REAL 13,IMAGINARY 13,PHASE 13,SYSTEM PHASE 13,IMPEDANCE 13,REAL 14,IMAGINARY 14,PHASE 14," \
                         "SYSTEM PHASE 14,IMPEDANCE 14,REAL 15,IMAGINARY 15,PHASE 15,SYSTEM PHASE 15,IMPEDANCE 15,REAL 16," \
                         "IMAGINARY 16,PHASE 16,SYSTEM PHASE 16,IMPEDANCE 16,REAL 17,IMAGINARY 17,PHASE 17,SYSTEM PHASE 17," \
                         "IMPEDANCE 17,REAL 18,IMAGINARY 18,PHASE 18,SYSTEM PHASE 18,IMPEDANCE 18,REAL 19,IMAGINARY 19," \
                         "PHASE 19,SYSTEM PHASE 19,IMPEDANCE 19,REAL 20,IMAGINARY 20,PHASE 20,SYSTEM PHASE 20,IMPEDANCE 20," \
                         "REAL 21,IMAGINARY 21,PHASE 21,SYSTEM PHASE 21,IMPEDANCE 21,REAL 22,IMAGINARY 22,PHASE 22,SYSTEM PHASE 22," \
                         "IMPEDANCE 22,REAL 23,IMAGINARY 23,PHASE 23,SYSTEM PHASE 23,IMPEDANCE 23,REAL 24,IMAGINARY 24,PHASE 24," \
                         "SYSTEM PHASE 24,IMPEDANCE 24,REAL 25,IMAGINARY 25,PHASE 25,SYSTEM PHASE 25,IMPEDANCE 25,REAL 26," \
                         "IMAGINARY 26,PHASE 26,SYSTEM PHASE 26,IMPEDANCE 26,REAL 27,IMAGINARY 27,PHASE 27,SYSTEM PHASE 27," \
                         "IMPEDANCE 27,REAL 28,IMAGINARY 28,PHASE 28,SYSTEM PHASE 28,IMPEDANCE 28"

    def get_name_string(self):
        column_list = self.name_list.split(sep=",")
        return column_list