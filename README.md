# CTFd REST API Python Module

## Overview
This Python module is designed to interact with the CTFd platform, a popular framework for Capture The Flag (CTF) competitions. It provides a set of tools to automate various tasks such as retrieving challenge IDs, submitting flags, and more.

## Main Functions
- get_awards: This function retrieves awards from the CTFd platform. It could
  be used to find out which hints were taken by which players.

- get_submissions: This function retrieves both correct and incorrect
  submissions made by players. It can be used for monitoring or analyzing the
  submissions to the challenges.

- post_flag: This function is designed for adding flags to challenges in the
  CTFd platform. It's essential for automating the setup.

- delete_flag: This function deletes a flag from the platform. It could be used
  in administrative or testing scenarios where flags need to be managed or
  removed.

- patch_flag: This function updates/modifies an existing flag. It can be used
  for correcting or changing flag details after their initial submission.

- post_challenge: This function is used to create a new challenge on the CTFd
  platform. It is very useful for admins or challenge creators to automate
  challenge setup.

- post_hint: Similar to post_challenge, this function creates new hints
  associated with challenges. 

- get_players: This function retrieves a list of players participating in the
  CTF. It could be used for monitoring player activity or for administrative
  purposes.

- post_player: This function likely adds a new player to the platform. It's
  essential for automating the registration or addition of participants in a
  CTF event by admins.

- post_attempt: This function designed for submitting a flag to a challenge by
  players. 

- get_scoreboard: As the name suggests, this function retrieves the scoreboard
  data from the CTFd platform. It's used for monitoring the scores and
  standings of participants in real-time.

## Aux Functions
- read_file: This function reads and returns the content of a specified file.
  Mainly used for reading token files needed for authentication.

- get_chall_id: This function retrieves the unique identifier for a challenge,
  either by name or directly by its ID. It essential for operations related to
  creating challenges in the CTFd platform.

- get_flag_id: Similar to get_chall_id, this function fetches the unique
  identifier for a flag. It's used for submitting or managing flags associated
  with challenges.

- get_hint_ids: This function is designed to retrieve identifiers for hints
  associated with challenges. It could be used to automate hint retrieval or
  management.

- get_player_id: This function obtains the unique identifier of a player. It
  can be used in contexts where user-specific operations are needed, such as
  scoring or submissions.

- parse: This function formats the hints in the get_awards function.
