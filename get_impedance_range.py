
def get_impedance_state(impedance):
    if impedance > 50_000:
        return "AIR"
    elif impedance > 7_500:
        return "RESIDUE"
    elif impedance > 1_000:
        return "LIQUID"
    else:
        return "ERROR"
