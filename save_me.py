from argparse import *
from os import system

OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'

parser = ArgumentParser()
parser.add_argument("file")
parser.add_argument("-o", "--out", help="file to print the result into", required=True)
parser.add_argument("-f", "--force", help="allows output file to match the input one", action='store_true')
parser.add_argument("-e", "--enum", help="use enum style of declaration instead of define one", action='store_true')
parser.add_argument("-i", "--interactive", help="asks you how to name unique numbers", action='store_true')
parser.add_argument("-w", "--with-comments", help="provides you with an opportunity to comment the constants, forces --interactive", action='store_true')

args = parser.parse_args()

fin = open(args.file, 'r')
content = fin.read()
fin.close()

if args.with_comments:
    args.interactive = True

if args.file == args.out and not args.force:
    print("Output file can't be equal to the input one")
    exit(0)

if args.enum:
    print(WARNING + "[WARN]  " + ENDC + ": USE OF --enum WILL GENERATE A NEW ENUM ON EACH SUBSEQUENT CALL UNLIKE USING DEFINES. YOU MIGHT HAVE TO CLEAR THEM UP MANUALLY")
elif args.with_comments:
    print(WARNING + "[WARN]  " + ENDC + ": USE OF --with-comment WITH define-style CAN LEAVE SOME COMMENTS ON SUBSEQUENT CALLS. YOU MIGHT HAVE TO CLEAR THEM UP MANUALLY")

def convert(x : str) -> str:
    return x.replace('1', 'one')\
        .replace('2', 'two')\
            .replace('3', 'three')\
                .replace('4', 'four')\
                    .replace('5', 'five')\
                        .replace('6', 'six')\
                            .replace('7', 'seven')\
                                .replace('8', 'eight')\
                                    .replace('9', 'nine')\
                                        .replace('0', 'zero')\
                                            .replace('.', 'dot').upper()

def ask(x : str) -> str:
    return input(OKGREEN + "[INPUT] " + ENDC + ": How do I name " + x + "? (Press Enter to skip the change)\n").upper()

def ask_for_comment(x : str) -> str:
    return input(OKGREEN + "[INPUT] " + ENDC + ": Provide a comment for the number " + x + ": (Press Enter to leave it blank)\n")

getname = convert
if args.interactive:
    getname = ask

i = 0
in_quotes = 0
in_squotes = 0
arr = []
used_names = set()
skipped_numbers = set()
while i < len(content):
    if content[i:i + 2] == '\"' or content[i:i + 2] == '\'':
        i += 2
        continue
    if content[i] == '"':
        in_quotes ^= 1
    if content[i] == "'":
        in_squotes ^= 1
    if in_quotes or in_squotes:
        i += 1
        continue
    if not content[i].isdigit():
        i += 1
        continue
    if not content[i - 1].isspace() and not content[i - 1] in "-=.,/'\"}{[]()!@#":
        i += 1
        continue
    j = i + 1
    while j < len(content) and content[j] in 'abcdef0123456789.uldbx':
        j += 1



    if content[i:j] in skipped_numbers:
        i = j
        continue

    new_name = "ALLO"
    comment = None

    known_number = False

    for x in arr:
        if x[0] == content[i:j]:
            known_number = True
            new_name = x[1]
            comment = x[2]
            break


    if not known_number:
        new_name = getname(content[i:j])
        while True:
            ok = True
            for x in arr:
                if x[0] != content[i:j] and x[1] == new_name:
                    print(FAIL + "[FAIL]  " + ENDC + ": THIS NAME IS ALREADY TAKEN BY NUMBER " + x[0])
                    ok = False
                    break
            bad = False
            for x in new_name:
                if x.lower() not in 'abcdefghijklmnopqrtstuvwxyz0123456789_':
                    bad = True
                    print(FAIL + "[FAIL]  " + ENDC + ":  UNSUPPORTED SYMBOL : '" + x + "'")
                    break
            if bad:
                ok = False
            if ok:
                break
            new_name = getname(content[i:j])

    if new_name == '':
        print(OKCYAN + "[INFO]  " + ENDC + ": SKIPPING NUMBER " + content[i:j])
        skipped_numbers.add(content[i:j])
        i = j
        continue
    if args.with_comments and comment is None:
        comment = ask_for_comment(content[i:j])
        if comment == '':
            print(OKCYAN + "[INFO]  " + ENDC + ": NO COMMENT PROVIDED FOR NUMBER " + content[i:j])

    if new_name != '':
        arr.append((content[i:j], new_name, comment))
        content = content[:i] + new_name + content[j:]
    i = j


st = set(arr)
st = sorted(list(st), key=lambda x : (-len(x[0]), x[0]))

print(OKBLUE + "[TRACE] " + ENDC + ": RECOGNISED " + str(len(st)) + " NUMBERS : " + str(st))

the_enum = []
for x in st:
    newx = x[1]
    thecomment = x[2]
    repl = '#define ' + newx + ' ' + newx + '\n'
    if repl in content:
        content = content.replace(repl, '', 1)
    if args.enum:
        if thecomment != '' and thecomment is not None:
            the_enum.append(newx + " = " + x[0] + " /* " + thecomment + " */")
        else:
            the_enum.append(newx + " = " + x[0])
    else:
        if thecomment != '' and thecomment is not None:
            content = "#define " + newx + ' ' + x[0] + ' /* ' + thecomment + ' */\n' + content
        else:
            content = "#define " + newx + ' ' + x[0] + '\n' + content

if args.enum:
    content = "enum { " + ", ".join(the_enum) + " };\n\n" + content

print(OKCYAN + "[INFO]  " + ENDC + ": REPLACED ALL RECOGNISED NUMBERS")

fout = open(args.out, "w")
fout.write(content)
fout.close()

print(OKBLUE + "[TRACE] " + ENDC + ": CALLING clang-format -i ON THE GENERATED FILE AT '" + args.out + "'")

ret = system("clang-format -i " + args.out)

if ret != 0:
    print(FAIL + "[FAIL]  " + ENDC + ": CALL TO clang-format -i FAILED")
else:
    print(OKCYAN + "[INFO]  " + ENDC + ": CALL TO clang-format -i SUCCEEDED")

fin = open(args.out, 'r')
content = fin.read()
fin.close()

for i, line in enumerate(content.split('\n')):
    if 'printf' in line and '\\n' not in line:
        print(WARNING + "[WARN]  " + ENDC + ": POSSIBLE CALL TO prtinf WITHOUT NEWLINE SYMBOL AT LINE " + str(i + 1) + " : '" + line.strip() + "'")
