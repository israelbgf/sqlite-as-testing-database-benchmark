# SQLite as testing database Benchmark

This is a (very) simple benchmark to validate an hypothesis. Assuming that we use MySQL or other relational persistence backend for our production code, would it be REALLY a bad idea to run all our tests using SQLite?

```sh
time python benchmark.py <numeber_of_tests>
```

## Context

When doing Unit tests you can do basically 3 things:

- Classicist Approach
    - Use the real implementation for the collaborators of the SUT.
    - Use an alternate implementation but faster implementation for the collaborators of the SUT.
- Mockist Approach
    - Do interaction testing to check for the calls to the collaborators.

In my experience, the collaborators related to the persistence layer are the most common ones used and the main target of Faking/Mocking. 

Generally, we hear that we should "mock the database" because it's, slow and too cumbersome to maintain in a test. What if it's not?

## Problem

- Using mocks your tests are more tightly coupled to the implementation code, so refactoring sometimes can get difficult.
- Using an real implementation is not always straight forward because you have to create/destroy the database and also the setup is not so fast.
- Creating an alternate in-memory implementation is more work to do and maintain.

## Solution

Use the real implementation (assuming that your persistence is a reational database) with an abstraction as SQLAlchemy and go with an SQLite backend for testing.

**Benefits**
    - Speed.
    - Don't need to maintain two implementations.
    - A test that's more blackbox, which is generally a good thing.
    - It's very easy to test all the app with the real backend (MySQL for example) if needed.

## General Comments

When you are implementing a new feature like `CreateClientUsecase`, the unit tests for that feature are going to be executed in less than a second (In my machine, I runned 100 tests in less than 0.9 seconds), and that's more than enough for a great feedback loop while doing TDD. I assume that very unlikely to one single feature to have more than 100 tests (my experience).

In a real application that I worked we had 1500 tests for the core rules of the system that took 5 seconds to run in a similar hardware than mine, and those tests were written using the Mock framework from python. Running 1500 tests with sqlite took around 17 seconds, a very slow time for doing TDD but an excelent time for the CI. Besides that, I don't think that you need to run all your unit tests while doing TDD for a new feature, just run the tests related to your feature (and in that case, the total time will be less than 1 second) and only after finishing that you'll run all your tests (or the CI will do it for you anyway).

And there's a plus, as you can see in the `multithread.sh`, you can have a gain in speed of 40% just for parallelizing your tests, so there's a whole world of optimization to do in that sense (CI with multiple workers for running tests).

## Downsides

When creating you application with an architecture as CleanArchitecture or HexagonalArchitecture your application tests would need to have the concrete implementation of something external. This is a bad thing if you plan to share your application as a library, but for all the commercial apps that I've worked that never would be an issue. If we needed an desktop client and wanted to use our core as a library, we could just strip the tests in the build step.

## Disclaimer

Of course, this is not the silver bullet. Remember, the only silver bullet in software development is having the notion that there aren't silver bullets in software development. This assumes, that your are using relational persistence (that's indeed very common, even more now that the hype of NoSQL is over and people are killing each other for Functional Programming and Containers now). This also assumes, that you don't attach business rules to your database (which is a good thing[but polemic one]), so you shouldn't use constraints besides foreign keys (no NOT NULLs, that could make hard to create some fixtures). Anyway, even if you don't follow this advice, wouldn't be hard to disable those kind of checks for testing and still have all the benefits above.
