# Test Driven Development with Django

_So, I decided to actually learn TDD by reading a book. You can find it on
[Amazon.com](https://www.amazon.com/Test-Driven-Development-Python-Selenium-JavaScript/dp/1449364829) or you can [read it online for free](https://www.obeythetestinggoat.com/pages/book.html)._

Commits in parenthesis indicate end of chapter.
* Chapter 01: Setting up;
* Chapter 02: Describing a user story as a functional test file;
* Chapter 03: Writing first unit test and tying application with the routing part `(8bb3256)`;
* Chapter 04: Starting to use templates, progressing in the functional test `(c6db2e7)`;
* Chapter 05: Starting to use ORM, testing persistence, displaying multiple
    items, functional test refactoring `(ede0f67)`;
* Chapter 06: MVP, each todo item is assigned to a todo list, each view has a
    single responsibility, the proposed functional test is now passing `(286a00b)`.
* Chapter 07: Application styling, handling static files. Just a basic
    test to ensure that the layout if fine and static files are working `(2f377a7)`.
* Chapter 08: Manual deployment. I read and implemented most of the chapter,
    except for this that really require a domain `(3d412a5)`
* Chapter 09: Shamelessly skipped it because we have Docker nowadays.


# Update notes

* The book uses Django `1.x`, which is slightly incompatible with version `3.x`.
I noted below the changes that made make so everything worked as expected.
* After reaching Chapter 07, I've notice that I was using Selenium `3.x`, and not `2.x`,
thus explaining some weird occasional complains about "Stale elements", to solve
that use the method `wait_for_page_load()` in the functional test.

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

- Using an environment variable instead of command line argument to run functional
    tests against a real server. This avoids `unittest` trying to load a
    non-existing module with the name of the url
- Updating `setUpClass()` from the functional test, so when the test is executed
    against a live server it doesn't run `tearDownClass()`, thus not crashing.
- I didn't properly finish this chapter because we have Docker nowadays, but
    most deployment configs, steps can be found in `deployment/`
