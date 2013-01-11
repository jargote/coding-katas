from numpy.distutils.system_info import numarray_info

__author__ = 'jargote'

def fizzbuzz(number):
    out = ''
    row = 0
    for i in xrange(number):

        if i % 3 == 0:
            out += 'fizz'
        if i % 5 == 0:
            out += 'buzz'
        else:
            out += str(i)

        row += 1
        if row == 20:
            out += '\n'
        else:
            out += ' '

    print out

def main():
    print 'Fizz Buzz Game\n'

    while True:
        while True:
            number = raw_input('\nPlease type a number:')
            if number.isdigit():
                break
            print 'Type a valid number.'

        # Play!
        fizzbuzz(int(number))

        # Replay ?
        while True:
            replay = raw_input('\nDo you want to play again? (y/n)')
            if replay.lower() == 'n':
                return 0
            elif replay.lower() == 'y':
                break

            print('Type y=Yes and n=No.')


if __name__ == '__main__':
    main()
