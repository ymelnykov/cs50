-- Keep a log of any SQL queries you execute as you solve the mystery.
SELECT description FROM crime_scene_reports WHERE year = 2021 AND month = 7 AND day = 28 AND street = "Humphrey Street";
-- Check what was going on near the bakery at on July 28, 2021 at 10:15
SELECT activity, license_plate FROM bakery_security_logs WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute = 15;
-- Since the previous query didn't give any result, check what was going on near the bakery on July 28, 2021
SELECT hour, minute, activity, license_plate FROM bakery_security_logs WHERE year = 2021 AND month = 7 AND day = 28;
-- Check the transcripts of interviews of witnesses on the date
SELECT id, name, transcript FROM interviews WHERE year = 2021 AND month = 7 AND day = 28;
-- Check the license plate of the car that left the parking lot between 10:15 and 10:25 (optional)
SELECT license_plate FROM bakery_security_logs WHERE activity = "exit" AND year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute BETWEEN 15 AND 25;
-- Check the account number from whiche a withdaw was made on the date at Leggett Street (optional)
SELECT account_number FROM atm_transactions WHERE year = 2021 AND month = 7 AND day = 28 AND transaction_type = "withdraw" AND atm_location = "Leggett Street";
-- Check the person associated with the account number
SELECT person_id FROM bank_accounts WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE year = 2021 AND month = 7 AND day = 28 AND transaction_type = "withdraw" AND atm_location = "Leggett Street");
-- Check the first flight on the next day to find destination airport id
SELECT destination_airport_id FROM flights WHERE year = 2021 AND month = 7 AND day = 29 ORDER BY hour, minute LIMIT 1;
-- Check the city based on the first flight on the next day
SELECT city FROM airports WHERE id = (SELECT destination_airport_id FROM flights WHERE year = 2021 AND month = 7 AND day = 29 ORDER BY hour, minute LIMIT 1);
-- Check the first flight on the next day to find the flight id
SELECT flight_id FROM flights WHERE year = 2021 AND month = 7 AND day = 29 ORDER BY hour, minute LIMIT 1;
-- Check passports of passengers from the flight
SELECT passport_number FROM passengers WHERE flight_id = (SELECT flight_id FROM flights WHERE year = 2021 AND month = 7 AND day = 29 ORDER BY hour, minute LIMIT 1);
-- Find the thief's name and telephone number as the intersection of person ids, license plate and passport number sets
SELECT * FROM people WHERE id IN (SELECT person_id FROM bank_accounts WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE year = 2021 AND month = 7 AND day = 28 AND transaction_type = "withdraw" AND atm_location = "Leggett Street")) INTERSECT SELECT * FROM people WHERE license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE activity = "exit" AND year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute BETWEEN 15 AND 25) INTERSECT SELECT * FROM people WHERE passport_number IN (SELECT passport_number FROM passengers WHERE flight_id = (SELECT flight_id FROM flights WHERE year = 2021 AND month = 7 AND day = 29 ORDER BY hour, minute LIMIT 1));
SELECT * FROM people WHERE id IN (SELECT person_id FROM bank_accounts WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE year = 2021 AND month = 7 AND day = 28 AND transaction_type = "withdraw" AND atm_location = "Leggett Street")) INTERSECT SELECT * FROM (SELECT * FROM people WHERE license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE activity = "exit" AND year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute BETWEEN 15 AND 25) INTERSECT SELECT * FROM people WHERE passport_number IN (SELECT passport_number FROM passengers WHERE flight_id = (SELECT flight_id FROM flights WHERE year = 2021 AND month = 7 AND day = 29 ORDER BY hour, minute LIMIT 1)));
SELECT * FROM people WHERE id IN (SELECT person_id FROM bank_accounts WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE year = 2021 AND month = 7 AND day = 28 AND transaction_type = "withdraw" AND atm_location = "Leggett Street")) INTERSECT SELECT * FROM (SELECT * FROM people WHERE license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE activity = "exit" AND year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute BETWEEN 15 AND 25) INTERSECT SELECT * FROM people WHERE phone_number IN (SELECT caller FROM phone_calls WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60));

SELECT * FROM people WHERE id IN (SELECT person_id FROM bank_accounts WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE year = 2021 AND month = 7 AND day = 28 AND transaction_type = "withdraw" AND atm_location = "Leggett Street"))
INTERSECT
SELECT * FROM (SELECT * FROM people WHERE license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE activity = "exit" AND year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute BETWEEN 15 AND 25)
INTERSECT
SELECT FROM ((SELECT * FROM people WHERE passport_number IN (SELECT passport_number FROM passengers WHERE flight_id = (SELECT flight_id FROM flights WHERE year = 2021 AND month = 7 AND day = 29 ORDER BY hour, minute LIMIT 1))
INTERSECT
SELECT caller FROM phone_calls WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60)));

-- Check phone calls
SELECT caller FROM phone_calls WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60;