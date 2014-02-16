# Colour

Add colour to command line application's output using config file.

e.g. nodetool status

```
xss =  -ea -javaagent:/usr/share/cassandra/lib/jamm-0.2.5.jar -XX:+UseThreadPriorities -XX:ThreadPriorityPolicy=42 -Xms3971M -Xmx3971M -Xmn800M -XX:+HeapDumpOnOutOfMemoryError -Xss256k
Datacenter: DC1
======================
Status=Up/Down
|/ State=Normal/Leaving/Joining/Moving
--  Address      Load       Tokens  Owns   Host ID                               Rack
UN  10.0.200.9   26.11 GB   256     5.4%   613d2143-0829-4fcc-8614-c2aa24007805  I6
UL  10.0.201.5   29.42 GB   256     5.1%   eb1b2b11-6856-4562-9c7c-03862fb5480f  G0
DN  10.0.202.8   32.29 GB   256     5.1%   7ecc8db9-9e9e-4000-98f4-e2441744a94b  I7
DL  10.0.203.6   25.27 GB   256     4.5%   114ba6d6-2c4e-4dd5-8cac-96725ec9a6ed  I6
```

using

```
<?xml version="1.0"?>
<input>
    <!--Datacenter label-->
    <line match="^Datacenter: (.+)">
        <part colour="default">1</part>
    </line>

    <!-- UP NORMAL -->
    <line match="^(UN)(.+)">
        <part colour="green">1</part>
        <part colour="default">2</part>
    </line>

    <!-- UP NOT NORMAL -->
    <line match="^(U[^N])(.+)" colour="yellow"/>

    <!--DOWN-->
    <line match="^(D[A-Z])(.+)" colour="red"/>
</input>
```

will colour down nodes fully red, non-normal nodes fully yellow and just the status of up nodes green.

## Usage

    nodetool status | ./colour --cfg=cfg/nodetool_status.xml