
class RegexFinder:
    def __init__(self, targetText, document='', descriptive=True, constantChars=None, constantPrecedingText=False, constantSucceedingText=False):
        self.__doc = document
        self.__str = targetText
        self.__descriptive = descriptive
        self.__constantChars = constantChars
        self.__constantPrecedingText = constantPrecedingText
        self.__constantSucceedingText = constantSucceedingText

    def find(self):
        target = self.__analyze(self.__str)
        if self.__doc:
            wholeText = self.__analyze(self.__doc)
            if self.__checkPattern(target, wholeText):
                print('UNIQUE REGEX PATTERN: ', self.__regex())
            else:
                if self.__constantPrecedingText:
                    lengthBeforeTarget = len(self.__doc[:self.__doc.find(self.__str) - 1])
                    print('UNIQUE REGEX PATTERN:', self.__regex(preceding=self.__beforeTarget(lengthBeforeTarget)))
                elif self.__constantSucceedingText:
                    lengthAfterTarget = len(
                        self.__doc[:len(self.__doc) - (self.__doc.find(self.__str) + len(self.__str) - 1) - 1])
                    print('UNIQUE REGEX PATTERN:', self.__regex(succeeding=self.__afterTarget(lengthAfterTarget)))
                else:
                    regex = self.__regex()
                    if self.__constantChars:
                        print('UNIQUE REGEX PATTERN:', regex)
                    else:
                        print('GENERAL REGEX PATTERN: ', regex)
        else:
            print('GENERAL REGEX PATTERN:', self.__regex())

    def __regex(self, preceding='', succeeding=''):
        arch = self.__rawRegexOverview()
        regex = ''
        keys = {'a': 'a-zA-Z', 'd': '\d', 'n': '\s', 's': '\W'}

        if not self.__descriptive:
            itemsBetweenConst = []
            if self.__constantChars:
                for x in range(len(self.__constantChars)):
                    if x != 0:
                        itemsBetweenConst.append(arch[arch.index(self.__constantChars[x - 1]) + 1:arch.index(self.__constantChars[x])])
                    else:
                        itemsBetweenConst.append(arch[:arch.index(self.__constantChars[x])])
                new = [[] for _ in itemsBetweenConst]
                index = 0
                for rem in itemsBetweenConst:
                    unique = []
                    for em in rem:
                        if type(em) == list:
                            if em[0][2:3] not in unique:
                                unique.append(em[0][2:3])
                                new[index].append(em)
                        else:
                            if em[2:3] not in unique:
                                unique.append(em[2:3])
                                new[index].append(em)
                    index += 1

                for x in range(len(self.__constantChars)):
                    if new[x]:
                        if x != 0:
                            arch[arch.index(self.__constantChars[x - 1]) + 1:arch.index(self.__constantChars[x])] = [new[x]]
                        else:
                            arch[:arch.index(self.__constantChars[x])] = [new[x]]

        brackets = False
        for part in arch:
            try:
                if ('-' in keys[part[0][2:3]]) or ('-' in keys[part[2:3]]):
                    regex += '['
                    brackets = True
            except KeyError:
                pass
            except TypeError:
                pass
            if type(part) == list:
                if not any(type(part[y]) == list for y in range(len(part))):
                    if part[1] == 1:
                        if self.__descriptive:
                            regex += f'{keys[part[0][2:3]]}'
                        else:
                            regex += f'{keys[part[0][2:3]]}*'
                    else:
                        if self.__descriptive:
                            if brackets:
                                regex += f'{keys[part[0][2:3]]}]{{{part[1]}}}'
                            else:
                                regex += f'{keys[part[0][2:3]]}{{{part[1]}}}'
                        else:
                            if brackets:
                                regex += f'{keys[part[0][2:3]]}]*'
                            else:
                                regex += f'{keys[part[0][2:3]]}*'
                else:
                    optional = '['
                    for element in part:
                        if type(element) == list:
                            optional += keys[element[0][2:3]]
                        else:
                            optional += keys[element[2:3]]
                    regex += optional + ']*?'
            else:
                if self.__constantChars:
                    if part in self.__constantChars:
                        regex += part[0]
                    else:
                        if self.__descriptive:
                            regex += keys[part[2:3]]
                        else:
                            if brackets:
                                regex += f'{keys[part[2:3]]}]*'
                            else:
                                regex += f'{keys[part[2:3]]}*'
                else:
                    if self.__descriptive:
                        regex += keys[part[2:3]]
                    else:
                        if brackets:
                            regex += f'{keys[part[2:3]]}]*'
                        else:
                            regex += f'{keys[part[2:3]]}*'
            brackets = False

        if preceding:
            regex = f'(?<={preceding})' + regex
        elif succeeding:
            regex = regex + f'(?={succeeding})'

        return regex

    def __rawRegexOverview(self):
        target = self.__analyze(self.__str)
        streakList = self.__findStreak(target)
        groupedStreaks = self.__groupByStreak(streakList)
        try:
            if self.__constantChars:
                self.__constantChars = [target[x] for x in self.__constantChars]
                for const in self.__constantChars:
                    if const in streakList:
                        streakList.remove(const)
        except IndexError:
            print('Index out of range')

        overviewGroups = []
        for group in groupedStreaks:
            for item in self.__separateGroupsByOrder(group):
                overviewGroups.append(item)

        finalGroups = overviewGroups
        if self.__constantChars:
            for _ in range(len(self.__constantChars)):
                finalGroups = self.__separateGroupsByConst(finalGroups, self.__constantChars)

        index = 0
        raw_reg = []
        for _ in target:
            if index < len(target):
                if target[index] in streakList:
                    found = False
                    for group in finalGroups:
                        if not found:
                            if target[index] in group:
                                raw_reg.append([target[index], len(group)])
                                index += len(group)
                                found = True
                else:
                    raw_reg.append(target[index])
                    index += 1

        return raw_reg

    @staticmethod
    def __analyze(text):
        alphas = [f'{x}:a:{i}' for i, x in enumerate(text) if x.isalpha()]
        digits = [f'{x}:d:{i}' for i, x in enumerate(text) if x.isdigit()]
        spaces = [f'{x}:n:{i}' for i, x in enumerate(text) if x.isspace()]
        symbols = [f'{x}:s:{i}' for i, x in enumerate(text) if not x.isalpha() and not x.isdigit() and not x.isspace()]
        charTypes = alphas + digits + spaces + symbols
        charTypes.sort(key=lambda x: int(x[4:]))

        return charTypes

    @staticmethod
    def __findStreak(target):
        streakList = []
        for x in range(len(target)):
            current = target[x][2:3]
            try:
                if current == target[x + 1][2:3]:
                    if target[x] not in streakList:
                        streakList.append(target[x])
                    streakList.append(target[x + 1])
            except IndexError:
                pass
        return streakList

    @staticmethod
    def __separateGroupsByOrder(lst):
        grouped = []
        result = []
        for i in range(len(lst)):
            result.append(lst[i])
            if i == len(lst) - 1:
                grouped.append(result)
            if (i != len(lst) - 1) and (lst[i][4:] != str(int(lst[i + 1][4:]) - 1)):
                grouped.append(result)
                result = []
        return grouped

    def __separateGroupsByConst(self, overviewGroups, constants):
        for i in range(len(overviewGroups)):
            for c in constants:
                if c in overviewGroups[i]:
                    index = overviewGroups[i].index(c)
                    overviewGroups[i].pop(index)
                    overviewGroups[i] = [overviewGroups[i][:index], overviewGroups[i][index:]]

        finalGroups = self.__listFlatter(overviewGroups)
        return finalGroups

    @staticmethod
    def __listFlatter(overviewGroups):
        finalGroups = []
        for group in overviewGroups:
            switch = False
            for part in group:
                if type(part) == list:
                    finalGroups.append(part)
                else:
                    switch = True
            if switch:
                finalGroups.append(group)

        return finalGroups

    @staticmethod
    def __groupByStreak(lst):
        grouped = []
        result = []
        for i in range(len(lst)):
            result.append(lst[i])
            if i == len(lst) - 1:
                grouped.append(result)
            if (i != len(lst) - 1) and (lst[i][2:3] != lst[i + 1][2:3]):
                grouped.append(result)
                result = []
        return grouped

    def __beforeTarget(self, lengthBeforeTarget):
        addChar = ''
        for x in range(lengthBeforeTarget + 1):
            if self.__countSubstrings(self.__doc, self.__doc[lengthBeforeTarget - x] + addChar) == 1:
                return self.__doc[lengthBeforeTarget - x] + addChar
            else:
                addChar = self.__doc[lengthBeforeTarget - x] + addChar

    def __afterTarget(self, lengthAfterTarget):
        addChar = ''
        charIndex = len(self.__doc) - lengthAfterTarget
        for x in range(lengthAfterTarget):
            if self.__countSubstrings(self.__doc, addChar + self.__doc[charIndex + x]) == 1:
                return addChar + self.__doc[charIndex + x]
            else:
                addChar += self.__doc[charIndex + x]

    @staticmethod
    def __checkPattern(target, whole_text):
        checkPattern = []
        target = [x[2:3] for x in target]
        whole_text = [x[2:3] for x in whole_text]
        for i in range(len(whole_text) - len(target) + 1):
            if whole_text[i:i + len(target)] == target:
                checkPattern.append(True)

        if len(checkPattern) == 1:
            return True
        else:
            return False

    @staticmethod
    def __countSubstrings(string, substring):
        stringSize = len(string)
        substringSize = len(substring)
        count = 0
        for i in range(0, stringSize - substringSize + 1):
            if string[i:i + substringSize] == substring:
                count += 1
        return count

    def help(self):
        print('Character indexes:')
        for char in self.__str:
            print(char, end='  ')
        print('')
        for _ in self.__str:
            print('|  ', end='')
        print('')
        for index in range(len(self.__str)):
            print(index, end='  ')
        print('')
