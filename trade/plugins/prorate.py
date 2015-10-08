"""prorate: Commissions pro rata on the OperationContainer.

http://trade.readthedocs.org/
https://github.com/rochars/trade
License: MIT

Copyright (c) 2015 Rafael da Silva Rocha

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from __future__ import division


def prorate_commissions(container):
    """Prorates the container's commissions by its operations.

    This method sum the discounts in the commissions dict of the
    container. The total discount value is then prorated by the
    position operations based on their volume.
    """
    for position_value in container.positions.values():
        for position in position_value.values():
            if position.update_position:
                prorate_commissions_by_position(container, position)
            else:
                for operation in position.operations:
                    prorate_commissions_by_position(container, operation)


def prorate_commissions_by_position(container, operation):
    """Prorates the commissions of the container for one position.

    The ratio is based on the container volume and the volume of
    the position operation.
    """

    if operation.volume != 0 and container.volume != 0:
        percent = operation.volume / container.volume * 100
        for key, value in container.commissions.items():
            operation.commissions[key] = value * percent / 100