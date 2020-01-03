# Test Driven Development with Django

_So, I decided to actually learn TDD by reading a book. You can find it on
[Amazon](https://www.amazon.com/Test-Driven-Development-Python-Selenium-JavaScript/dp/1449364829)._

* Chapter 01: Setting up;
* Chapter 02: Describing a user story as a (functional) test file;
* Chapter 03: Writing first unit test and tying application with the routing part;
* Chapter 04: Starting using templates, progressing in the functional test;


# Update notes

_The book uses Django `1.x`, which is slightly incompatible with version `2.0`.
I noted below the changes that I had to make so everything worked as expected._

## Chapter 03

- Use `from django.urls import resolve` instead of
    `from django.core.urlresolvers import resolve`;
- There's no need to use BOL and EOL in URL regexes anymore.

## Chapter 05

- To work around the CSRF token remove if from the HTML before asserting.