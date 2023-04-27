# RegexFinder


<img src="https://user-images.githubusercontent.com/108073687/221195981-8381352d-1465-4753-884b-0a522fe52fbf.jpg" width="450">

## This is a 3-day zero-dependency project that finds regular expression for any piece of text

### How to install:

    pip install regexfinder


### How to import:

```python
from regexfinder import RegexFinder
```
  
### How to use:

#### Call **RegexFinder**, type inside the string you want to be regular expressed, and **find()** !

```python
RegexFinder(text).find()
```

This module contains some parameters that you have to understand before using properly:

- **descriptive** - default is True. This means that the program will generate a regexp based on the format and length of the string, any minor change in format will not work adaptively. If you want a regexp that will work dynamically in other situations, turn this to False and utilize the below parameters as explained.
    

- **document** - paste here the full text if you want to find regexp of string based on actual environment

    - **constantPrecedingText** - turn this to True if you have inserted a document, to create a regexp that is based on the text **before** the pattern you want to find, that never changes.

    - **constantSucceedingText** - turn this to True if you have inserted a document, to create a regexp that is based on the text **after** the pattern you want to find, that never changes.

- **constantChars** - To be able to find general regexp for a pattern of a string, you should declare one or more characters which will always appear in string, as constants. For example, if you want to find regexp of this string `'test="123"'`, which represents a key and a value, you should add as constantChar the `=`, and both the `"`, so the program can grasp from atleast somewhere what's going on and what the objective of the user is. This parameter takes as input list which contains indexes of characters that you want to be declared constant. Index of character starts from 0, as the first char of string, and goes on for the length of it. If you have trouble finding this indexes, call the ```help()``` function of this class and it will display the indexes for you. For the above example the input would look like this: `constantChars=[4, 5, 9]`. 

```python
RegexFinder('riflosnake', descriptive=False, document='best programmer of the year: riflosnake', constantPrecedingText='year: ').find()

> UNIQUE REGEX PATTERN: (?<=: )[a-zA-Z]*
```

### Reason for these parameters is that finding and generating Regular Expressions programmatically without A.I is almost impossible, because the code can't deduct the purpose of the regex itself, it doesn't have logic, so the only solution is if you and the program work together, you throw the hints, RegexFinder does the heavy duty.

### So if you want a proper RegExp, make sure to do atleast one of these, while **_descriptive=False_**:
1. add constants to constantChars
2. add the document where string is located and specify if the text before or after is constant

### Code illustrations:

  <img src="https://user-images.githubusercontent.com/108073687/221011994-73c0dc54-8914-4ecc-b3ae-c07219379a07.jpg" width="600" height="200">

  <img src="https://user-images.githubusercontent.com/108073687/221011998-fbfc5977-6ac1-4a73-bee3-2ea3410b749c.jpg" width="850" height="200">

  <img src="https://user-images.githubusercontent.com/108073687/221012005-1a4aa582-3297-4d65-8445-e67ab27b776f.jpg" width="600" height="200">
  
  
### For any idea or problem comment on this repo.

