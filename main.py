import db

# list of tokens for detection
tokens = []
# list of token's names
names = []
# list of all unique methods from all token standards
words = []


# add token ans its requirements to lists
def add_token(name, parents, words):
    names.append(name)
    tokens.append(list(set(sum(parents, []) + words)))


add_token(
    "erc20",
    [],
    [
        "balanceOf",
        "transfer",
        "totalSupply",
        "transfer",
        "transferFrom",
        "approve",
        "allowance",
        "Transfer",
        "Approval",
    ],
)
erc20 = tokens[0]
add_token("erc20Permit", [erc20], ["permit", "nonces", "DOMAIN_SEPARATOR"])

add_token("erc20Burnable", [erc20], ["burn", "burnFrom"])


words = list(set(sum(tokens, [])))
codes = []

# kind of vectorization. Every erc20 version is a vector of 0 and 1. Length of vector is length of words.
# Words is list of all methods and equls to [1,1,..,1]
for t in tokens:
    tmpCode = [1 if w in t else 0 for w in words]
    codes.append(tmpCode)


# def detect_contract_from_file(name):
#     code = [1 for _ in words]
#     with open(name, 'r', encoding='utf-8') as file:
#         data = file.read()
#         for i in range(len(words)):
#             if words[i] in data:
#                 code[i] = 0
#     for j in range(len(codes)-1, -1, -1):
#         if not any([codes[j][i] & code[i] == 1 for i in range(len(codes[j]))]):
#             return names[j]

# detects version of text and  returns first possible version from the end
def detect_contract(text):
    codes = []
    for t in tokens:
        tmpCode = [1 if w in t else 0 for w in words]
        codes.append(tmpCode)
    code = [1 for _ in words]
    for i in range(len(words)):
        if words[i] in text:
            code[i] = 0

    for j in range(len(codes) - 1, -1, -1):
        if not any([codes[j][i] & code[i] == 1 for i in range(len(codes[j]))]):
            return names[j]


# return binary data of file
def convert_from_file_to_binary(filename):
    with open(filename, "rb") as file:
        return file.read()


# returns text of binary data
def convert_from_binary_to_text(memo):
    return bytes(memo).decode("utf-8")


# function to generate lot of data and insert it into db. addressgeneration.nb generates ids.txt file.
def gen_data(cnt):
    tokens = [
        "bnb.sol",
        "token.sol",
        "token2.sol",
        "token3.sol",
        "token4.sol",
        "token6.sol",
    ]
    i = 0
    with open("ids.txt", "r") as file:
        for line in file:
            db.insert_contract(
                cnt, [line[:-2], convert_from_file_to_binary("tokens/" + tokens[i])]
            )
            i += 1
            if i == len(tokens):
                i = 0


# gets records that "waits processing", changes its status to "processing" then detects version and updates record
def detect(cnt, size=100):
    records = db.get_wait_processing_contracts(cnt, size)
    db.update_status_to_processing(cnt, [r[0] for r in records])
    udpateData = []

    for r in records:
        tmp = convert_from_binary_to_text(r[1])
        res = detect_contract(tmp)
        udpateData.append((r[0], res is not None, res))
    db.update_records(cnt, udpateData)


# detects all contracts from db. size — batch size.
def detectAll(cnt, size=100):
    records = db.get_wait_processing_contracts(cnt, size)
    while len(records) > 0:
        db.update_status_to_processing(cnt, [r[0] for r in records])
        udpateData = []

        for r in records:
            tmp = convert_from_binary_to_text(r[1])
            res = detect_contract(tmp)
            udpateData.append((r[0], res is not None, res))
        db.update_records(cnt, udpateData)
        records = db.get_wait_processing_contracts(cnt, size)


if __name__ == "__main__":

    cnt = db.connect()

    # data generation
    gen_data(cnt)

    # contract detection
    detectAll(cnt, 200)

    cnt.close()
