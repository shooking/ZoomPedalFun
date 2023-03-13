import zoomzt2_shooking
# Read file, parse and print details
binfile = open("mypedal/RACKCOMP.ZD2", "rb")
if binfile:
    bindata = binfile.read()
    binfile.close()

    binconfig=zoomzt2_shooking.ZD2.parse(bindata)
    print(binconfig)

