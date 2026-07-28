import sys
#
# int __fastcall look_up_customer_id(const char *a1)
#
def customer_to_id(customername):
	if customername == "Iskratel": return 1
	if customername == "Rostelecom": return 2
	if customername == "RostelecomCentr": return 3
	if customername == "RostelecomSouth": return 4
	if customername == "Superonline": return 5
	if customername == "T2": return 6
	if customername == "NorthTexasFiber": return 50
	if customername == "Optima": return 10
	if customername == "OptimaBIZ": return 11
	if customername == "Ukrtelecom": return 7
	if customername == "Uzbektelecom": return 8
	if customername == "Iskon": return 9
	if customername == "Scancom": return 12
	if customername == "Ozone": return 13
	if customername == "TelekomSlovenije": return 14
	if customername == "Moldtelecom": return 15
	if customername == "BHtel": return 16
	if customername == "BHtel2": return 17
	if customername == "Vitis": return 18
	if customername == "Zeop": return 19
	if customername == "Vestra": return 20
	if customername == "TelecomSerbia": return 21
	if customername == "Telemach": return 22
	if customername == "Telfy": return 23
	if customername == "Alsatis": return 24
	if customername == "AlsatisBIZ": return 49
	if customername == "Cetin": return 51
	if customername == "Becactus": return 25
	if customername == "Ultel": return 26
	if customername == "MGTS": return 27
	if customername == "SBB": return 28
	if customername == "Innonet": return 29
	if customername == "Kyrgyztelecom": return 30
	if customername == "Forthnet": return 31
	if customername == "IsraelGeneric": return 32
	if customername == "Klonex": return 33
	if customername == "Vectra": return 34
	if customername == "Bitel": return 35
	if customername == "A1-Croatia": return 36
	if customername == "ERTELECOM": return 37
	if customername == "TARR": return 38
	if customername == "Nordnet": return 39
	if customername == "CommunityFibre": return 40
	if customername == "Beeline": return 41
	if customername == "Benda": return 42
	if customername == "Israel-IBC": return 43
	if customername == "Iskratel_AccessPoint": return 44
	if customername == "Iskratel_Controller": return 45
	if customername == "Zzoomm": return 46
	if customername == "Iskratel_Interop": return 47
	if customername == "SalzburgAG": return 48
	if customername == "Hyperoptics": return 52
	return -1
print( customer_to_id( sys.argv[1] ) )
