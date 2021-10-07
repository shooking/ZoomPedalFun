import time
import json
import os


# g5_params was pdf -> text then editing
with open("g5_params.json", "r") as fxFile:
    model=fxFile.read()

json_fx=json.loads(model)

# fxs.dat was observation of sysex FX id -> fx, coupled with zoom id
with open("fxs.dat", "r") as fxFile:
    model=fxFile.read()

rawFX=json.loads(model)



for fx in rawFX:
    print(fx['name'])
    for otherFX in json_fx:
        if fx['name'] == otherFX['name']:
            print("match {} {}".format(fx['name'], otherFX['name']))
            print(fx)
            print(otherFX)
            try:
                filename="{}.json".format(fx['name'])
                print("Filename {} {}".format(filename, os.path.isfile(filename)))
                with open(filename, 'r') as fxFile:
                    m = fxFile.read()
                currJSON = json.loads(m)
                #print(currJSON)
                for currp in range(len(currJSON['Parameters'])):
                    p = currJSON['Parameters'][currp]
                    print("Checking for {}".format(p['name']))
                    for currq in range(len(otherFX['Parameters'])):
                        q = otherFX['Parameters'][currq]
                        print("\t against {}".format(q['name']))
                        if p['name'] ==q['name']:
                            print("MATCHED PARAM")
                            (otherFX['Parameters'][currq]).update({'mdefault': p['mdefault'], 'mmax': p['mmax']})
                            # we matched, so we can break
                            break
                #print(otherFX['Parameters'])
                # later we want to merge fx['p_id'] into otherFX
            except:
                print("missing file [{}]".format(filename))
            (otherFX).update({'p_id': fx['p_id']})
            print(otherFX)
            # we found a match so break
            break

# write out the merged files
with open('g5_merged_pedal_params.json', 'w') as outFile:
    json.dump(json_fx, outFile)


# g5_zpedal.json was  was pdf -> text then editing
with open("g5_zpedal.json", "r") as fxFile:
    model=fxFile.read()

json_fx=json.loads(model)

# so far not found the Sysex to load a Z Pedal?
for otherFX in json_fx:
    try:
        filename="{}.json".format(otherFX['name'])
        print("Filename {} {}".format(filename, os.path.isfile(filename)))
        with open(filename, 'r') as fxFile:
            m = fxFile.read()
        currJSON = json.loads(m)
        #print(currJSON)
        for currp in range(len(currJSON['Parameters'])):
            p = currJSON['Parameters'][currp]
            print("Checking for {}".format(p['name']))
            for currq in range(len(otherFX['Parameters'])):
                q = otherFX['Parameters'][currq]
                print("\t against {}".format(q['name']))
                if p['name'] ==q['name']:
                    print("MATCHED PARAM")
                    (otherFX['Parameters'][currq]).update({'mdefault': p['mdefault'], 'mmax': p['mmax']})
                    # we matched, so we can break
                    break
        # later we want to merge fx['p_id'] into otherFX
    except:
        print("missing file [{}]".format(filename))
    (otherFX).update({'p_id': fx['p_id']})
    print(otherFX)
    # we found a match so break
    break

# write out the merged files
with open('g5_merged_zpedal_params.json', 'w') as outFile:
    json.dump(json_fx, outFile)
