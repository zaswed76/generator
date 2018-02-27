
a="""Event: Newstate
Privilege: call,all
Channel: SIP/105-0007be79
ChannelState: 6
ChannelStateDesc: Up"""

import yaml
#------------

b = """Event: RTCPSent
Privilege: reporting,all
To: 192.168.0.7:16429
OurSSRC: 722615561
SentNTP: 1319652944.0257110016
SentRTP: 110384776
SentPackets: 28241
SentOctets: 4518560
ReportBlock:
FractionLost: 0
CumulativeLoss: 0
IAJitter: 0.0001
TheirLastSR: 0
DLSR: 65517.7580 (sec)"""

#----------------
dct = yaml.load(b)
