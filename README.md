# Test Driven Development with Django

_So, I decided to actually learn TDD by reading a book. You can find it on
[Amazon](https://www.amazon.com/Test-Driven-Development-Python-Selenium-JavaScript/dp/1449364829)._

* Chapter 01: Setting up;
* Chapter 02: Describing a user story as a (functional) test file;
* Chapter 03: Writing first unit test and tying application with the routing part


# Update notes

## Chapter 03

- Use `from django.urls import resolve` instead of
    `from django.core.urlresolvers import resolve`;
- There's no need to use BOL and EOL in URL regexes anymore.