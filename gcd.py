__author__ = 'jargote'

import time
import decimal


def gcd(a, b):
    q = a % b

    print q
    if q == 0:
        return b

    return gcd(b, q)


def main():
    while True:
        print 'Calcule Greatest Common Divisor for 2 numbers\n'
        a = raw_input('Type value for 1st number:')
        b = raw_input('Type value for 2nd number:')

        t1 = time.time()
        res = gcd(int(a), int(b))
        t2 = time.time()
        exec_time = decimal.Decimal(t2 - t1)

        print '\nfor %s and %s the GCD is: %s. It took %s segs\n' % (a, b, res,
                                                                     exec_time)


if __name__ == '__main__':
    main()