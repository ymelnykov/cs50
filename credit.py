from cs50 import get_string
import re

// Input card number
card = str()
while not card.isdigit():
    card = get_string("Card: ")

// Checksum card number
sum = 0
card = card[::-1]
for i in range(len(card)):
    if i % 2 == 0:
        sum += int(card[i])
    else:
        if int(card[i])*2 > 9:
            sum += int(card[i]) * 2 % 10 + 1
        else:
            sum += int(card[i]) * 2

// Check card validity by checksum
card = card[::-1]
if sum % 10 != 0:
    print('INVALID')

// Check card type using regular expressions
if re.match(r'3[47]\d{13}', card):
    print('AMEX')
elif re.match(r'5[1-5]\d{14}', card):
    print('MASTERCARD')
elif re.match(r'4\d{12|15}', card):
    print('VISA')
else:
    print('INVALID')

