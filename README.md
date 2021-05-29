# Diceroll bot

Discord bot that rolls dice.

Specifically, at the moment it rolls following the rules for Vampire: the Masquerade.

## Commands

* `/v {n}`: rolls *n* dice with the default difficulty (6).
* `/v {n} {d}`: rolls *n* dice at difficulty *d*.

## Setup

1) Install dependencies. 
2) Add a variable `TOKEN` to the environment containing the bot's token from [Discord developer portal](https://discord.com/developers).
3) Run the application.
4) Roll!

A Dockerfile is included too to conveniently build.