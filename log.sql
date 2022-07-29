-- Keep a log of any SQL queries you execute as you solve the mystery.
SELECT description FROM crime_scene_reports WHERE year = 2021 AND month = 7 AND day = 28 AND street = "Humphrey Street";
-- Check what was going on near the bakery at on July 28, 2021 at 10:15
SELECT activity, license_plate FROM bakery_security_logs WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute = 15;
-- Since the previous query didn't give any result, check what was going on near the bakery on July 28, 2021
SELECT hour, minute, activity, license_plate FROM bakery_security_logs WHERE year = 2021 AND month = 7 AND day = 28;
-- Check the transcripts of interviews of witnesses on the date
SELECT id, name, transcript FROM interviews WHERE year = 2021 AND month = 7 AND day = 28;
-- Check the license plates of cars that left the parking lot between 10:15 and 10:25
SELECT license_plate FROM bakery_security_logs WHERE activity = "exit" AND year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute BETWEEN 15 AND 25;
-- Check the account numbers from which a withdaw was made on the date at Leggett Street
SELECT account_number FROM atm_transactions WHERE year = 2021 AND month = 7 AND day = 28 AND transaction_type = "withdraw" AND atm_location = "Leggett Street";
-- Check the persons associated with the account numbers
SELECT person_id FROM bank_accounts WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE year = 2021 AND month = 7 AND day = 28 AND transaction_type = "withdraw" AND atm_location = "Leggett Street");
-- Check the first flight on the next day to find destination airport id
SELECT destination_airport_id FROM flights WHERE year = 2021 AND month = 7 AND day = 29 ORDER BY hour, minute LIMIT 1;
-- Find the city based on the first flight on the next day
SELECT city FROM airports WHERE id = (SELECT destination_airport_id FROM flights WHERE year = 2021 AND month = 7 AND day = 29 ORDER BY hour, minute LIMIT 1);
-- Check the first flight on the next day to find the flight id
SELECT id FROM flights WHERE year = 2021 AND month = 7 AND day = 29 ORDER BY hour, minute LIMIT 1;
-- Check passports of passengers from the flight
SELECT passport_number FROM passengers WHERE flight_id = (SELECT id FROM flights WHERE year = 2021 AND month = 7 AND day = 29 ORDER BY hour, minute LIMIT 1);
-- Check phone calls to find the caller (thief)
SELECT caller FROM phone_calls WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60;
-- Find the thief's name and telephone number as the intersection of person id, license plate, caller and passport number sets
SELECT name FROM (SELECT * FROM people WHERE id IN (SELECT person_id FROM bank_accounts WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE year = 2021 AND month = 7 AND day = 28 AND transaction_type = "withdraw" AND atm_location = "Leggett Street")) INTERSECT SELECT * FROM (SELECT * FROM people WHERE license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE activity = "exit" AND year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute BETWEEN 15 AND 25) INTERSECT SELECT * FROM people WHERE phone_number IN (SELECT caller FROM phone_calls WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60))) WHERE passport_number IN (SELECT passport_number FROM passengers WHERE flight_id = (SELECT id FROM flights WHERE year = 2021 AND month = 7 AND day = 29 ORDER BY hour, minute LIMIT 1));
-- Find accomplice's name as the receiver called by the thief
SELECT name FROM people WHERE phone_number = (SELECT receiver FROM phone_calls WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60 AND caller = "(367) 555-5533");

