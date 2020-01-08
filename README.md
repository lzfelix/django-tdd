# Test Driven Development with Django

_So, I decided to actually learn TDD by reading a book. You can find it on
[Amazon.com](https://www.amazon.com/Test-Driven-Development-Python-Selenium-JavaScript/dp/1449364829) or you can [read it online for free](https://www.obeythetestinggoat.com/pages/book.html)._

* Chapter 01: Setting up;
* Chapter 02: Describing a user story as a functional test file;
* Chapter 03: Writing first unit test and tying application with the routing part;
* Chapter 04: Starting to use templates, progressing in the functional test;
* Chapter 05: Starting to use ORM, testing persistence, displaying multiple
    items, functional test refactoring;
* Chapter 06: MVP, each todo item is assigned to a todo list, each view has a
    single responsibility, the proposed functional test is now passing.
* Chapter 07: Application styling, handling static files. Just a basic
    test to ensure that the layout if fine and static files are working.


# Update notes

_The book uses Django `1.x`, which is slightly incompatible with version `2.x`.
I noted below the changes that made make so everything worked as expected. After
reaching Chapter 07, I've notice that I was using Selenium `3.x`, and not `2.x`,
thus explaining some weird occasional complains about "Stale elements", to solve
that use the method `wait_for_page_load()` in the functional test_

## Chapter 03

- Use `from django.urls import resolve` instead of
    `from django.core.urlresolvers import resolve`;
- There's no need to use `^` and `$` in URL regexes anymore.

## Chapter 05

- To work around the CSRF token for testing, remove if from the HTML before
    asserting.
- Use `functional_tests::_wait_todo_item_appear()` to avoid Selenium complaining
    about stale elements. This happens because the page is refreshed, while
    selenium probably has an instance of a previous DOM element.

## Chapter 06

- In the functional test, I swapped the order between checking for Francis' milk
    and comparing his URL to Edith's since Selenium has to wait the page to
    reload. Another option would be to use `WebDriverWait()` following
    `wait_for_page_load()`;
- Django `2.x` ORM requires `on_delete` attribute when creating FKs, the most
    reasonable choice is `models.CASCADE` in this case;

## Chapter 07

- I've used the CDN version of Bootstrap instead of downloading the static
    content, further, HTML has to be slightly adapter for some reason;

## Chapter 08

- Using environment variable instead of command line argument to run functional
    tests against a real server. This avoids `unittest` trying to load a
    non-existing module with the name of the url
