# README #

The goal is to spend 90 minutes and build out the flow to create an appointment against a doctor. Doctors don't have tightly controlled schedules; they're very unlike a Google calendar. Rather, doctors open up certain times during the day, and patients can book only into those free areas - the rest is assumed to be unavailable.

This is like seeing a movie at the theater. You can't arbitrarily see a movie at any time; there are published start times, and you get tickets.

Therefore this problem is to:

* Create a way to model a doctor's free times (availability)
* Create a way to book an appointment against that free time

This repository contains the outlines of a FastAPI web API. FastAPI docs are available at https://fastapi.tiangolo.com/

We've built two skeletons for this project. One uses a SQL database (sqlite, without an ORM),
and one is entirely in-memory using data structures that mimic a database.

Decide which skeleton you'd like to use, and extend it (we do prefer the SQL version). In the settings.py file, you can set `in_database` to false to trigger
the skeleton to use an in-memory service. *Don't* do both ways - we have two implementations just as an example.

When you've finished, please *open a PR* with your changes against the main branch.

## IMPORTANT

If you do this as a "take home", prior to your interview, do not spend too much time on it. Aim for 90 mins. 

Part of the exercise is to see what tradeoffs you make, and explain them when talking through the solution. How did you prioritize what to build first? What, if anything, would you do differently if you had to put this code into production?

## Problem statement

We would like to build a simple service for managing doctors and their schedules.
Requirements:

* For each doctor we would initially like to store the following:
    * id
	* name
	* locations - represented as a collection of address strings
	* schedule - weekly schedule indicating the hours they are available each day of the week
* CRUD operations for doctors
	* This is mostly done already to set some patterns - feel free to add another endpoint or two as a warm-up, but try to focus more on the availability aspect
* Ability to book an appointment with a doctor (a tuple of (doctor, location, time))
* Ability to get all appointments for a doctor
* Ability to cancel an appointment with a doctor

Expectations/assumptions:

* The API will be internally-facing and used by other applications/services that we trust
* The API will be single-tenant (it only contains data for a single hospital)
* A doctor is available at any of their locations for any of their available times
* A doctor can only have one appointment at a time
* A doctor can travel instantaneously between locations
* No UI/front-end is expected

## Prerequisites/Running It

Whatever you choose from this list, the app will come up at `localhost:8000` with some swagger docs.

### Docker

If you prefer, you can run the app in Docker. Simply run `docker-compose up` and you should get a hot-reloading server running on port 8000. You can set the
`in_database` flag in the `docker-compose.yaml` file, if desired.

### Native

Alternatively, you're welcome to run the app natively. We've developed it against Python 3.11 - once you have that installed, you should only need to run:
```
pip install -r requirements.txt
python server.py
```

#### Extra questions ####

Below are a few questions which expand the scope of the service. Please pick one and describe your approach.

* What are some real-world constraints to booking appointments that would add complexity to this API and how would they impact the design.
* How would our design change if this API was opened up to external users?
* What concerns are there with multi-tenant data management and how could we modify the design to increase data security?

#### Suggestions ####

* Start simple
* Document your assumptions and their impact on the design
* Stub out areas that are not related to core functionality and describe their expected behavior
* You may choose any means of persistence (ex: database, third-party service, etc.) or choose to exclude it (e.g. in-memory only). We recognize that integrating with a persistence layer may be time-consuming and by omitting it, more time can be allocated to service development.
* You may use any third-party libraries you feel are appropriate

## What we’re looking for

A Software Craftsperson at Incubyte is a person who has a strong commitment to the craft of software development.
Someone who is passionate about software, knows their tools well, and is able to use them effectively to create carefully crafted software.
Ultimately, a person who has a strong sense of what they are doing and is self-motivated to learn and grow.

TDD is a core practice for all of us at Incubyte.
We strongly believe that well-written software is a lot more valuable for the business and end users, as compared to software that is hacked together (but works!).

Through this assessment, we want to evaluate how readable and testable your code is. We want to see the Software Craftsperson in you.

As software developers, searching the internet is something of a necessity and is a vital tool for being effective problem solvers.
We encourage you to Google away!
You can also visit our [inspiration](https://incubyte.co/inspiration/) page to find some useful talks and references that will help you sail through this assessment.

With that, let's jump right in!

## Things to keep in mind

1. Host your solution on a **public** GitHub/GitLab repository.
2. Follow best practices for TDD. Watch [this video](https://youtu.be/qkblc5WRn-U) to understand TDD better.
3. Commit your changes frequently, ideally after every change to show how your code evolves with every step of TDD.
4. Send us the link to your repo once you’re happy with what you have done.

### Tips:

- Start with the simplest test case and move to complex
- Remember to solve problems in a simple manner so that you force yourself to write tests you did not think about.
- Remember to refactor after each passing test.


### Who do I talk to? ###
* If you have any questions prior to your interview, please reach out to your designated Incubyte recruiting contact and he/she will get back to you as soon as possible.
* If you have any feedback on the interview question after you're done, let us know, we're always looking into improving the interview process. Thanks!
