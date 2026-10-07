from flask import Flask, render_template, request

app = Flask(__name__)


def caesar(text, shift):
    result = ""

    for char in text:
        if char.isalpha() and char.isascii():
            base = ord("A") if char.isupper() else ord("a")

            result += chr(
                (ord(char) - base + shift) % 26 + base
            )
        else:
            result += char

    return result


def vigenere(text, key, decrypt=False):
    key = key.upper()

    if not key.isalpha():
        raise ValueError("مفتاح Vigenère لازم يكون حروف إنجليزية فقط")

    result = ""
    key_index = 0

    for char in text:

        if char.isalpha() and char.isascii():

            shift = ord(key[key_index % len(key)]) - ord("A")

            if decrypt:
                shift = -shift

            base = ord("A") if char.isupper() else ord("a")

            result += chr(
                (ord(char) - base + shift) % 26 + base
            )

            key_index += 1

        else:
            result += char

    return result


def xor_cipher(text, key):
    if not key:
        raise ValueError("اكتب مفتاح XOR")

    result = ""

    for i, char in enumerate(text):
        result += chr(
            ord(char) ^ ord(key[i % len(key)])
        )

    return result


@app.route("/", methods=["GET", "POST"])
def home():

    result = ""
    error = ""

    if request.method == "POST":

        message = request.form.get("message", "")
        key = request.form.get("key", "")
        algorithm = request.form.get("algorithm", "caesar")
        action = request.form.get("action", "encrypt")

        try:

            if not message:
                raise ValueError("اكتب رسالة أولًا")

            if not key:
                raise ValueError("اكتب المفتاح")

            decrypt = action == "decrypt"

            if algorithm == "caesar":

                shift = int(key)

                if decrypt:
                    shift = -shift

                result = caesar(message, shift)

            elif algorithm == "vigenere":

                result = vigenere(
                    message,
                    key,
                    decrypt
                )

            elif algorithm == "xor":

                result = xor_cipher(
                    message,
                    key
                )

            else:
                raise ValueError("الخوارزمية غير صحيحة")

        except ValueError as e:
            error = str(e)

    return render_template(
        "index.html",
        result=result,
        error=error
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
