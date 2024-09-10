import math as m
import hashlib
import ast


def MD4(data):
    md4_hash = hashlib.new('md4')
    md4_hash.update(data)
    return (md4_hash)


class Dane:

    def __init__(self, x):
        if isinstance(x, bytes):
            self.dane = x
            self.hash = None
        else:
            raise TypeError("Argument nie jest ciągiem bajtów")

    @classmethod
    def from_string(cls, x):
        if isinstance(x, str):
            return (cls(bytes(x, 'utf-8')))
        else:
            raise TypeError("Argument nie jest stringiem")

    @classmethod
    def from_file(cls, x):
        try:
            plik = open(x, "r")
            return (cls.from_string(plik.read()))
        except:
            raise ValueError("Nie udało się przeczytać pliku")

    def get_hash(self):
        if self.hash == None:
            md4_hash = hashlib.new('md4')
            md4_hash.update(self.dane)
            self.hash = int(md4_hash.hexdigest(), 16)
        return (self.hash)

    def __str__(self):
        return (hex(self.get_hash())[2:])


def isprime(a):
    sqrt = m.floor(m.sqrt(a))
    if a == 1:
        return (False)
    for i in range(2, sqrt + 1):
        if a % i == 0:
            return (False)

    return (True)


def NWD(a, b):
    while b != 0:
        a, b = b, a % b
    return (a)


class Keys:

    def __init__(self, p, q, e=1):
        if isinstance(p, int) and isinstance(q, int) and isinstance(e, int):
            if p > 0 and q > 0 and e > 0:
                if isprime(p) and isprime(q):
                    if NWD(e, (p - 1) * (q - 1)) == 1:
                        self.p = p
                        self.q = q
                        self.e = e

                        self.public_key = (p * q, e)
                        self.private_key = None

                    else:
                        raise ValueError("NWD{e, p-1, q-1} nie równa się 1")
                else:
                    raise ValueError("Któraś z liczb p lub q nie jest liczbą pierwszą")
            else:
                raise ValueError("Któraś z liczb nie jest liczbą dodatnią")

        else:
            raise TypeError("Któraś z liczb nie jest liczbą całkowitą")

    def get_private_key(self):
        if self.private_key == None:

            reszta = None
            a = self.e
            b = (self.q - 1) * (self.p - 1)
            listadiv = []

            while True:

                div = a // b
                reszta = a % b
                if reszta == 0:
                    break
                listadiv.append(div)
                a, b = b, reszta

            listadiv.reverse()
            x, y = 1, (-1) * listadiv[0]
            for i in range(1, len(listadiv)):
                x, y = y, x - (listadiv[i]) * y
            self.private_key = (x, self.p, self.q)

        return (self.private_key)

    def encrypt(self, m):
        if isinstance(m, int):
            if m >= 0 and self.public_key[0] > m:
                return ((m ** (self.get_private_key()[0])) % (self.p * self.q))
            else:
                raise ValueError(f"Szyfrowana wiadomość jest za duża maks: {self.public_key[0] - 1}")
        else:
            raise TypeError("Szyfrowana wiadomość nie jest liczbą całkowitą")

    def decrypt(self, c):
        if isinstance(c, int):
            if c > 0:
                return ((c ** (self.public_key[1])) % self.public_key[0])
            else:
                raise ValueError("Odszyfrowywna wiadomość nie jest liczbą naturalną")

        else:
            raise TypeError("Odszyfrowana wiadomość nie jest liczbą całkowitą")

    def public_key_to_file(self, nazwa_pliku):
        with open(f"{nazwa_pliku}.txt", "w") as file:
            file.write(str(self.public_key))

    def private_key_to_file(self, nazwa_pliku):
        with open(f"{nazwa_pliku}.txt", "w") as file:
            file.write(str(self.get_private_key()))

    def signature(self, dane):
        if isinstance(dane, Dane):
            return (self.encrypt(int(str(dane.get_hash())[:3], 16)))

        else:
            raise TypeError("Argument nie jest typu Dane")


class Public_key:

    def __init__(self, N, e):
        self.public_key = [N, e]

    @classmethod
    def from_string(cls, string):
        if isinstance(string, str):
            return (cls(ast.literal_eval(string)[0], ast.literal_eval(string)[1]))
        else:
            raise TypeError("Argument nie jest stringiem")

    @classmethod
    def from_file(cls, file):
        try:
            plik = open(file, "r")
            return (cls.from_string(plik.read()))
        except:
            raise ValueError("Nie udało się przeczytać pliku")

    @classmethod
    def from_keys(cls, key):
        if isinstance(key, Keys):
            return (cls(key.public_key[0], key.public_key[1]))
        else:
            raise TypeError("Argument nie jest obiektem keys")

    def decrypt(self, c):
        if isinstance(c, int):
            if c > 0:
                return ((c ** (self.public_key[1])) % self.public_key[0])
            else:
                raise ValueError("Odszyfrowywna wiadomość nie jest liczbą naturalną")

        else:
            raise TypeError("Odszyfrowana wiadomość nie jest liczbą całkowitą")

    def check_signature(self, dane, podpis):
        if isinstance(dane, Dane):
            if (int(str(dane.get_hash())[:3], 16)) == self.decrypt(podpis):
                return (True)
            else:
                return (False)
        else:
            raise TypeError("Argument nie jest typu Dane")