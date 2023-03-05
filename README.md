# Caos formatter

It is a script that reformats your code.

## Features

- Parses all numbers it can find (except for those enclosed with single or double quotes) and replaces them with named constants
- Automatically calls `clang-format` on the generated file
- Checks for `printf` statements that don't contain `\n` symbol and prints a warning if found

## Usage

Couple of words before we get to it:

- It is recommended to use `out` file name different from the one you want to reformat. Based on my experience, nothing is being lost during the process of solving tasks. However, code becomes much harder to read after the reformat. So you basically want to have the original intact pretty much always. Thus, the recommended development pipeline looks something like this:
    1) Write code in `solution.c`
    2) Run the tool to obtain `reformatted_solution.c`
    3) Submit `reformatted_solution.c`
    4) Return to the first stage if solution wasn't accepted

    There's a built-in check to ensure that the input and output file are different. It can be disabled with `--force` flag

- Tools supports two dirrent styles of naming constants:
    1) `define` style
    2) `enum` style

    Let's take this piece of of code and run the tool on it.
    ```c
    #include <stdio.h>
    int main() {
        int a, b;
        int sum = 0;
        scanf("%d %d", &a, &b);
        for (int i = a + 1; i < b + 2; ++i) {
            sum += i * 3;
        }
        printf("%d", sum);
        return 0;
    }
    ```

    Produced output:

    <table>
    <tr>
    <td> Defines </td> <td> Enum </td>
    </tr>
    <tr>
    <td style="vertical-align: top;">

    ```c
    #define THREE 3
    #define TWO 2
    #define ONE 1
    #define ZERO 0
    #include <stdio.h>

    int main() {
        int a, b;
        int sum = ZERO;
        scanf("%d %d", &a, &b);
        for (int i = a + ONE; i < b + TWO; ++i) {
            sum += i * THREE;
        }
        printf("%d", sum);
        return ZERO;
    }
    ```

    </td>
    <td style="vertical-align: top;">

    ```c
    enum { ZERO = 0, ONE = 1, TWO = 2, THREE = 3 };

    #include <stdio.h>

    int main() {
        int a, b;
        int sum = ZERO;
        scanf("%d %d", &a, &b);
        for (int i = a + ONE; i < b + TWO; ++i) {
            sum += i * THREE;
        }
        printf("%d", sum);
        return ZERO;
    }
    ```
    </td>
    </tr>
    </table>

- By default, tool will replace all digits with their text representation. E.g. `4` is replaced with `FOUR`. `567` is replaced with `FIVESIXSEVEN`. You can change this behaivour by specifying `--interactive` flag. Tool will then ask you to name every distinct number it identifies.

- If you feel the need to provide some additional context for the constant, you can specify `--with-comments` flag. This will also force `--interactive`. Thus, tool will ask you for both the name of the constant, and for the comment to put near it.

    Example:

    <table>
    <tr>
    <td> Defines </td> <td> Enum </td>
    </tr>
    <tr>
    <td style="vertical-align: top;">

    ```c
    #define TRIO 3     /* 1 + 2 = 3 */
    #define TWO 2      /* just two */
    #define SMOL_GUY 1 /* smol */
    #define ZERO 0     /* none, nothing */
    #include <stdio.h>

    int main() {
        int a, b;
        int sum = ZERO;
        scanf("%d %d", &a, &b);
        for (int i = a + SMOL_GUY; i < b + TWO; ++i) {
            sum += i * TRIO;
        }
        printf("%d", sum);
        return ZERO;
    }

    ```

    </td>
    <td style="vertical-align: top;">

    ```c
    enum {
        ZERO = 0 /* none, nothing */,
        SMOL_GUY = 1 /* smol */,
        TWO = 2 /* just two */,
        TRIO = 3 /* 1 + 2 = 3 */
    };

    #include <stdio.h>

    int main() {
        int a, b;
        int sum = ZERO;
        scanf("%d %d", &a, &b);
        for (int i = a + SMOL_GUY; i < b + TWO; ++i) {
            sum += i * TRIO;
        }
        printf("%d", sum);
        return ZERO;
    }
    ```
    </td>
    </tr>
    </table>

To sum everything up, here's the help message:

```
usage: save_me.py [-h] -o OUT [-f] [-e] [-i] [-w] file

positional arguments:
  file

optional arguments:
  -h, --help           show this help message and exit
  -o OUT, --out OUT    file to print the result into
  -f, --force          allows output file to match the input one
  -e, --enum           use enum style of declaration instead of define one
  -i, --interactive    asks you how to name unique numbers
  -w, --with-comments  provides you with an opportunity to comment the constants, forces --interactive
```
