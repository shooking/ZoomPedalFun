#!/bin/bash
#
# I meed to transform
# host	4.1.3	[something] => SEND: [something]
# host	4.1.3	 => remove the line
# 4.1.4	host	[something] => RECV:	[something]
# host	4.1.0 => remove line but to be fair I only proecess SEND:
# so I only need change those lines?
export PATH="/cygdrive/C/Program Files/Wireshark":${PATH}
#
# Oh and I need to inject
# f052006e50f7
# f052006e5802f7
# f052006e52f7
for pedal in A1Four A1XFour B1Four B1XFour B3n G1Four G1XFour G3n G3Xn G5n
do
	MYFILE=Clean${pedal}.pcapng
	tempFile=ChangeTo${pedal}.txt
	rm -f ${tempFile}
	touch ${tempFile}
	echo "SEND: f052006e50f7" >> ${tempFile} 
	echo "SEND: f052006e5802f7" >> ${tempFile}
	echo "SEND: f052006e52f7" >> ${tempFile}
	tshark -r ${MYFILE} -2 -T fields -e usb.src -e usb.dst -e usbaudio.sysex.reassembled.data \
		| sed -e 's/\r//' \
		| sed -e '/^host\t4.1.0\t$/d' \
		| sed -e '/^host\t4.1.3\t$/d' \
		| sed -e '/^host\t4.1.4\t$/d' \
		| sed -e '/^4.1.0\thost\t$/d' \
		| sed -e '/^4.1.3\thost\t$/d' \
		| sed -e '/^4.1.4\thost\t$/d' \
		| sed -e 's/^host\t4.1.3\tf/SEND: f/' \
		| sed -e 's/^4\.1\.4\thost\tf/RECV: f/' \
		>> ${tempFile}
done

