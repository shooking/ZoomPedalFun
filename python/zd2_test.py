import zoomzt2_shooking
# Read file, parse and print details
with open("mypedal/RACKCOMP.ZD2", "rb") as binfile:
    bindata = binfile.read()
    binconfig=zoomzt2_shooking.ZD2.parse(bindata)
    print(binconfig)