# Issue Table

| Issue | Type | Line(s) | Description | Fix Approach |
| :--- | :--- | :--- | :--- | :--- |
| **Use of eval** | Security | 59 | eval("...") can execute arbitrary code (Bandit B307). This is a major security vulnerability. | Removing the eval call. |
| *Mutable Default Argument* | Bug | 8 | logs=[] is a mutable default argument. This list will be shared and persist across all calls to addItem. | Changing the default to logs=None and initializing logs = [] inside the function. |
| *Missing Input Validation* | Bug / Robustness | 8, 51 | addItem accepts invalid types (like 123, "ten") and negative quantities, which can corrupt the stock_data. | Adding type checks (isinstance) and value checks (qty >= 0) and raise a ValueError. |
| **Potential KeyError** | Bug | 23 | getQty directly accesses stock_data[item], which will crash if the item doesn't exist. | Use of stock_data.get(item, 0) to safely return 0 for missing items. |
| **Bare except** | Reliability | 19-20 | except: pass catches all exceptions (including SystemExit) and silently ignores them, hiding bugs. | Catching the specific exception you expect (e.g., KeyError). |
| *Unsafe File Handling* | Reliability | 26-34 | open() is used without a with block, risking resource leaks if an error occurs. No file encoding ("utf-8") is specified. | Using the with open(file, mode, encoding="utf-8") as f: context manager. |
| *Global Variable* | Design | 6, 28 | The code relies on a mutable global stock_data. loadData rebinds it with the global keyword. This makes the code hard to test and reason about. | Passing stock_data as a parameter to functions that need it. Having loadData return the dictionary. |
| *PEP8 Naming* | Style | 8, 14, 22... | Functions use camelCase (e.g., addItem) instead of the PEP8 standard snake_case (e.g., add_item). | Renaming all functions to snake_case. |
| *Missing Docstrings* | Maintainability | All | No module or function docstrings exist, making the code's purpose and usage unclear. | Adding a module docstring and docstrings to all functions describing their purpose, arguments, and return values. |
| *Unused Import* | Style | 2 | import logging is included but the logging module is never used. | Removing the import (or, preferably, use it for logging errors instead of print). |
| *Old-Style Formatting* | Style | 12 | Uses old %-style string formatting, which is less readable than f-strings. | Converting "%s: Adding %d..." to an f-string. |


# Answers

1) The easiest issues to fix were the self-contained, single-line changes. For example, removing the eval call was a simple line deletion that instantly solved a major security risk. Similarly, fixing the potential KeyError in getQty by changing stock_data[item] to stock_data.get(item, 0) was a straightforward, standard Python idiom. These were easy because they were local fixes that didn't affect any other part of the code.

   The hardest issue by far was refactoring the code to remove the global stock_data variable. This was not a local fix but an architectural change that had a ripple effect across the entire module. It required modifying the function signature of almost every function to accept stock_data as a parameter and then updating the main() function to manage and pass this state variable, fundamentally changing the program's data flow.

2) The static analysis tools did not report any false positives. Every issue flagged by tools like Pylint and Bandit pointed to a genuine, tangible problem. The eval call was a real security risk, the mutable default argument was a subtle but critical bug, the bare except was hiding errors, and the global variable was a poor design choice. All style violations, like naming and missing docstrings, correctly identified code that was less readable and maintainable.

3) I would integrate static analysis tools into a real workflow at two key points. First, for local development, I would install extensions for tools like Pylint and Flake8 directly into my code editor (like VS Code). This provides real-time feedback as I type. I would also use pre-commit hooks to run a quick linter on staged files, acting as a local quality gate before I even commit. Second, I would configure a "Static Analysis" job in the Continuous Integration (CI) pipeline. This job would run on every pull request and would be set to fail the build if it detected any high-severity issues, ensuring no problematic code gets merged into the main branch.

4) The improvements to the code after applying the fixes were dramatic. The most significant improvement was in robustness. The original brittle code, which would crash from a missing item or file, can now gracefully handle those exact scenarios. Input validation prevents data corruption, and proper error handling in file I/O means it no longer crashes on a FileNotFoundError. The security was critically improved by removing the eval vulnerability. Finally, readability and maintainability are night-and-day. By removing the global variable, the data flow is now explicit and easy to follow. Using standard naming conventions and docstrings makes the code professional and understandable to any developer.
