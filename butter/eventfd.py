#!/usr/bin/env python
"""eventfd: maintain an atomic counter inside a file descriptor"""

from __future__ import print_function

from .utils import Eventlike as _Eventlike

from ._eventfd import EFD_CLOEXEC, EFD_NONBLOCK, EFD_SEMAPHORE
from ._eventfd import str_to_events, event_to_str
from ._eventfd import eventfd
import os as _os

class Eventfd(_Eventlike):
    def __init__(self, inital_value=0, flags=0):
        """Create a new Eventfd object

        Arguments
        ----------
        :param int inital_value: The inital value to set the eventfd to
        :param int flags: Flags to specify extra options
        
        Flags
        ------
        EFD_CLOEXEC: Close the eventfd when executing a new program
        EFD_NONBLOCK: Open the socket in non-blocking mode
        EFD_SEMAPHORE: Provide semaphore like semantics for read operations
        """
        super(self.__class__, self).__init__()
        self._fd = eventfd(inital_value, flags)
        
    def increment(self, value=1):
        """Increment the counter by the specified value
        
        :param int value: The value to increment the counter by (default=1)
        """
        packed_value = event_to_str(value)
        _os.write(self.fileno(), packed_value)

    def _read_events(self):
        """Read the current value of the counter and zero the counter

        Returns
        --------
        :return: The current count of the timer
        :rtype: int
        """
        data = _os.read(self.fileno(), 8)
        events = str_to_events(data)

        return events


    def __int__(self):
        return self.read_event()


def _main():
    ev = Eventfd(30)
    
    print('First Read:', int(ev))
    # read blocks if 0
    #print('Second Read:', int(ev))
    
    print("Adding 30 to zero'd counter")
    ev.increment(30)
    
    print("Read value back:", int(ev))

    print("Incrementing value 5 times")
    ev.increment(30)
    ev.increment(30)
    ev.increment(30)
    ev.increment(30)
    ev.increment(30)
    
    print("Read value back:", int(ev))

    print("Closing FD")    
    ev.close()
    try:
        ev.close()
    except ValueError:
        print("Could not close closed FD, OK")
    else:
        print("Closed closed FD, this is bad")
    
if __name__ == "__main__":
    _main()
