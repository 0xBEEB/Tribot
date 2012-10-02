# Tribot

by Thomas Schreiber <thomas@ubiquill.com>

Copyright (c) 2012 Thomas Schreiber


## License

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


## Description

An IRC bot that relates Trimet (public transit in Portland, Oregon) arrival,
gps, and stop information. Tribot utilizes the Trimet developer API, and the
Google Maps geocode API.

## Usage

Tribot currently resides on Freenode IRC with the nick "trimetbot" and on 
irc.cat.pdx.edu with the nick "tribot". Tribot can be messaged for information.

### Commands

    STOPSBY <address>

Returns a list of stops near the given address.

Example:

    /msg trimetbot STOPSBY 1900 sw main

Response:

    ID: 9820, Southbound on Kings Hill/SW Salmon St MAX Station
    ID: 9553, Southbound on SW 18th & Salmon
    ID: 5006, Eastbound on SW Salmon & 19th
    ID: 5019, Eastbound on SW Salmon & 20th
    ID: 5018, Westbound on SW Salmon & 20th

-

    ARRIVALS <stopID>

Returns the upcoming arrivals for the given stops. If gps data is available,
then the arrival time is estimated based off of the vehicles current location.

Example:

    /msg trimetbot ARRIVALS 9820

Response:

    MAX  Blue Line to Hillsboro arriving in 9 minutes
    MAX  Red Line to City Center & Beaverton TC arriving in 13 minutes
    MAX  Blue Line to Hillsboro arriving in 13 minutes

-

    LASTSEEN <stopID> <route#>

If gps data is available for the next bus with route# arriving at stopID, then
a human readable address is returned along with the length of time that has
passed since the gps reading was taken.

Example:

    /msg trimetbot LASTSEEN 5020 15

Response:

    Your bus was last seen on 22 NW 23rd Ave, Portland, OR 97210, USA 0 minutes and 55 seconds ago

-

    HELP

Returns a list of commands.

Example:

    /msg trimetbot HELP

Response:

    help, about, arrivals <stopid>, stopsby <address>, lastSeen <stopID> <BusRoute>

-

    ABOUT

Returns information about Tribot.

Example:

    /msg trimetbot ABOUT

Response:

    Tribot by Thomas Schreiber <thomas@ubiquill.com>
    Find me on github at http://github.com/ubiquill/tribot
    Try '\msg tribot help' for a list of commands
 
