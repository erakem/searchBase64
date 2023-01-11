# **Introduction**

If you have a base64-encoded file and want to find a word into it, you could do this :

```
base64 -d <file> | grep <word>
```

But for a partially base64-encoded file, it is not possible anymore.
With this code, you could do

```
$ echo "HEADER$(echo -n "Hi Bob! How are you doing?" | base64)TRAILER" | python3 -m search_base64.find Bob
-: found Bob => Qm9i
```

# **Installation**

You can install it as a PyPI package:
```
pip install search-base64
```

# **Base64**

Quoting wikipedia, "Base64 is a group of binary-to-text encoding schemes that represent binary data (more specifically, a sequence of 8-bit bytes) in sequences of 24 bits that can be represented by four 6-bit Base64 digits."

One of the possible table is the one defined in RFC 4648 §4:

| Index | Binary | Char |  | Index | Binary | Char |  | Index | Binary | Char | | Index | Binary | Char |
| ----- | ------ | ---- | - | ----- | ------ | ---- | - | ----- | ------ | ---- | - | ----- | ------ | ---- |
|  0 | 000000 | A |  | 16 | 010000 | Q | |  32 | 100000 | g | |  48 | 110000 | w |
|  1 | 000001 | B |  | 17 | 010001 | R | |  33 | 100001 | h | |  49 | 110001 | x |
|  2 | 000010 | C |  | 18 | 010010 | S | |  34 | 100010 | i | |  50 | 110010 | y |
|  3 | 000011 | D |  | 19 | 010011 | T | |  35 | 100011 | j | |  51 | 110011 | z |
|  4 | 000100 | E |  | 20 | 010100 | U | |  36 | 100100 | k | |  52 | 110100 | 0 |
|  5 | 000101 | F |  | 21 | 010101 | V | |  37 | 100101 | l | |  53 | 110101 | 1 |
|  6 | 000110 | G |  | 22 | 010110 | W | |  38 | 100110 | m | |  54 | 110110 | 2 |
|  7 | 000111 | H |  | 23 | 010111 | X | |  39 | 100111 | n | |  55 | 110111 | 3 |
|  8 | 001000 | I |  | 24 | 011000 | Y | |  40 | 101000 | o | |  56 | 111000 | 4 |
|  9 | 001001 | J |  | 25 | 011001 | Z | |  41 | 101001 | p | |  57 | 111001 | 5 |
| 10 | 001010 | K |  | 26 | 011010 | a | |  42 | 101010 | q | |  58 | 111010 | 6 |
| 11 | 001011 | L |  | 27 | 011011 | b | |  43 | 101011 | r | |  59 | 111011 | 7 |
| 12 | 001100 | M |  | 28 | 011100 | c | |  44 | 101100 | s | |  60 | 111100 | 8 |
| 13 | 001101 | N |  | 29 | 011101 | d | |  45 | 101101 | t | |  61 | 111101 | 9 |
| 14 | 001110 | O |  | 30 | 011110 | e | |  46 | 101110 | u | |  62 | 111110 | + |
| 15 | 001111 | P |  | 31 | 011111 | f | |  47 | 101111 | v | |  63 | 111111 | / |

Padding is '='.

For now, let's assume that
1. a character is encoded as 1 byte. It will be easier to speak about strings instead of bytes.
2. there is only one way to encode a character

## **How to get binary representation of a character?**

Let's use this python command to determine it:
```
f"{ord(char):08b}"
```

## **Encode "B"**

For 'B', we get 01000010 so 8 bits.

**Notice the little gap every 6 bits as they will be used as index to the encoded character**

| b01 | b02 | b03 | b04 | b05 | b06 |  | b07 | b08 | b09 | b10 | b11 | b12 |  | b13 | b14 | b15 | b16 | b17 | b18 |  | b19 | b20 | b21 | b22 | b23 | b24 |
| --- | --- | --- | --- | --- | --- | - | --- | --- | --- | --- | --- | --- | - | --- | --- | --- | --- | --- | --- | - | --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 0 | 0 | 0 |   | 1 | 0 | 

But, by definition, we need 24 digits. So we need to pad the last 16 bits with zeroes.

| b01 | b02 | b03 | b04 | b05 | b06 |  | b07 | b08 | b09 | b10 | b11 | b12 |  | b13 | b14 | b15 | b16 | b17 | b18 |  | b19 | b20 | b21 | b22 | b23 | b24 |
| --- | --- | --- | --- | --- | --- | - | --- | --- | --- | --- | --- | --- | - | --- | --- | --- | --- | --- | --- | - | --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 0 | 0 | 0 |   | 1 | 0 | 0 | 0 | 0 | 0 |   | 0 | 0 | 0 | 0 | 0 | 0 |   | 0 | 0 | 0 | 0 | 0 | 0 |

Now we will use the previous table to encode these 24 bits into 4 characters.
| b1 | b2 | b3 | b4 | b5 | b6 |  | Char |
| --- | --- | --- | --- | --- | - | --- | ---- |
| 0 | 1 | 0 | 0 | 0 | 0 |  | Q
| 1 | 0 | 0 | 0 | 0 | 0 |  | g
| 0 | 0 | 0 | 0 | 0 | 0 |  | =
| 0 | 0 | 0 | 0 | 0 | 0 |  | =

Last 2 characters should be encoded as 'A' but as there is only one character to be encoded the last 2 ones are the padding characters.

Now, let's examine how to encode a string of 1, 2 and 3 characters.

## Encode "Bo"

For 'B', we still get 01000010 so 8 bits.

For 'o', we get 01101111 so 8 more bits.

| b01 | b02 | b03 | b04 | b05 | b06 |  | b07 | b08 | b09 | b10 | b11 | b12 |  | b13 | b14 | b15 | b16 | b17 | b18 |  | b19 | b20 | b21 | b22 | b23 | b24 |
| --- | --- | --- | --- | --- | --- | - | --- | --- | --- | --- | --- | --- | - | --- | --- | --- | --- | --- | --- | - | --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 0 | 0 | 0 |   | 1 | 0 | 0 | 1 | 1 | 0 |  | 1 | 1 | 1 | 1 |

But, by definition, we need 24 digits. So we need to pad the last 8 bits with zeroes.

| b01 | b02 | b03 | b04 | b05 | b06 |  | b07 | b08 | b09 | b10 | b11 | b12 |  | b13 | b14 | b15 | b16 | b17 | b18 |  | b19 | b20 | b21 | b22 | b23 | b24 |
| --- | --- | --- | --- | --- | --- | - | --- | --- | --- | --- | --- | --- | - | --- | --- | --- | --- | --- | --- | - | --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 0 | 0 | 0 |   | 1 | 0 | 0 | 1 | 1 | 0 |  | 1 | 1 | 1 | 1 | 0 | 0 |  | 0 | 0 | 0 | 0 | 0 | 0 |

Now we will use the previous table to encode these 24 bits into 4 characters.
| b1 | b2 | b3 | b4 | b5 | b6 |  | Char |
| --- | --- | --- | --- | --- | - | --- | ---- |
| 0 | 1 | 0 | 0 | 0 | 0 | | Q
| 1 | 0 | 0 | 1 | 1 | 0 | | m
| 1 | 1 | 1 | 1 | 0 | 0 | | 8
| 0 | 0 | 0 | 0 | 0 | 0 | | =

Last character should be encoded as 'A' but, as there are two characters to be encoded, the last one is the padding character.

## **Encode "Bob"**

For 'B', we still get 01000010 so 8 bits.

For 'o', we still get 01101111 so 8 more bits.

For 'b', we get 01100010 so 8 more bits.

| b01 | b02 | b03 | b04 | b05 | b06 |  | b07 | b08 | b09 | b10 | b11 | b12 |  | b13 | b14 | b15 | b16 | b17 | b18 |  | b19 | b20 | b21 | b22 | b23 | b24 |
| --- | --- | --- | --- | --- | --- | - | --- | --- | --- | --- | --- | --- | - | --- | --- | --- | --- | --- | --- | - | --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 0 | 0 | 0 |   | 1 | 0 | 0 | 1 | 1 | 0 |  | 1 | 1 | 1 | 1 | 0 | 1 | | 1 | 0 | 0 | 0 | 1 | 0 |

This time we don't need any padding.

Now we will use the previous table to encode these 24 bits into 4 characters.
| b1 | b2 | b3 | b4 | b5 | b6 |  | Char |
| --- | --- | --- | --- | --- | - | --- | ---- |
| 0 | 1 | 0 | 0 | 0 | 0 | | Q
| 1 | 0 | 0 | 1 | 1 | 0 | | m
| 1 | 1 | 1 | 1 | 0 | 1 | | 9
| 1 | 0 | 0 | 0 | 1 | 0 | | i

This time there is no need to replace anything as there was no padding involved.

## **Generalisation**

We can see that a string can be split into 3-characters chunks (so 3*8=24 bits) which will be independently encoded as 4 characters (so 4*6=24 bits).


As we've seen :
- "B" will be encoded as "Qg=="
- "Bo" will be encoded as "Qm8="
- "Bob" will be encoded as "Qm9i"

So :
- "BobB" will be encoded as "Qm9iQg=="
- "BobBo" will be encoded as "Qm9iQm8="
- "BobBob" will be encoded as "Qm9iQm9i"

## **We need to do it the other way around**

But we can't just search for "Qm9i" in the base64-encoded text.

As we've just shown, 3 consecutive letters are encoded as base64. The text "Dear Bob!" will be encoded as 3-characters chunks :
- "Dea" encoded as "RGVh"
- "r B" encoded as "ciBC"
- "ob!" encoded as "b2Ih"

As you can notice, "Qm9i" is nowhere to be found even if "Bob" is part of the (clear) text.

Indeed, "Bob" can appear in 2 separated 3-characters chunks :
- x"Bo", "b"yz
- xy"B", "ob"z

with x, y, z being whatever character (remember: we assume, for now, that any given character is 1 byte).

## **Let's analyse that first case x"Bo", "b"yz **

### **First part x"Bo"**

For x, we get abcdefgh so 8 bits. Each letter a to h is either 0 or 1.

For 'B', we still get 01000010 so 8 more bits.

For 'o', we still get 01101111 so 8 more bits.

| b01 | b02 | b03 | b04 | b05 | b06 |  | b07 | b08 | b09 | b10 | b11 | b12 |  | b13 | b14 | b15 | b16 | b17 | b18 |  | b19 | b20 | b21 | b22 | b23 | b24 |
| --- | --- | --- | --- | --- | --- | - | --- | --- | --- | --- | --- | --- | - | --- | --- | --- | --- | --- | --- | - | --- | --- | --- | --- | --- | --- |
| a | b | c | d | e | f |   | g | h | 0 | 1 | 0 | 0 |  | 0 | 0 | 1 | 0 | 0 | 1 | | 1 | 0 | 1 | 1 | 1 | 1 |

Yet again, as we already have 24 bits, no padding is required.

Now we will use the previous table to encode these 24 bits into 4 characters.
| b1 | b2 | b3 | b4 | b5 | b6 |  | Char |
| --- | --- | --- | --- | --- | - | --- | ---- |
| a | b | c | d | e | f | |  See below 1.
| g | h | 0 | 1 | 0 | 0 | |  See below 2.
| 0 | 0 | 1 | 0 | 0 | 1 | |  J
| 1 | 0 | 1 | 1 | 1 | 1 | |  v

So now we have :
1. one character we don't care about as it does not contain any information about "Bob"
2. one character than can be one of the 4
    1. 00 0100, so 'E'
    2. 01 0100, so 'U'
    3. 10 0100, so 'k'
    4. 11 0100, so '0'

So looking for "Bo"('b' is coming thereafter) into the clear text is "equivalent" (so far) to look for "[EUk0]Jv" into the base64-encoded text.

### **Second part "b"yz**

For 'b', we still get 01100010 so 8 bits.

For y, we get abcdefgh so 8 more bits. Each letter a to h is either 0 or 1.

For z, we get ijklmnop so 8 more bits. Each letter i to p is either 0 or 1.

| b01 | b02 | b03 | b04 | b05 | b06 |  | b07 | b08 | b09 | b10 | b11 | b12 |  | b13 | b14 | b15 | b16 | b17 | b18 |  | b19 | b20 | b21 | b22 | b23 | b24 |
| --- | --- | --- | --- | --- | --- | - | --- | --- | --- | --- | --- | --- | - | --- | --- | --- | --- | --- | --- | - | --- | --- | --- | --- | --- | --- |
 0 | 1 | 1 | 0 | 0 | 0 |  | 1 | 0 | a | b | c | d |  | e | f | g | h | i | j | | k | l | m | n | o | p |

Now we will use the previous table to encode these 24 bits into 4 characters.
| b1 | b2 | b3 | b4 | b5 | b6 |  | Char |
| --- | --- | --- | --- | --- | - | --- | ---- |
| 0 | 1 | 1 | 0 | 0 | 0 | |  Y
| 1 | 0 | a | b | c | d | |  See below 2.
| e | f | g | h | i | j | |  See below 1.
| k | l | m | n | o | p | |  See below 1.

So now we have :
1. two trailing characters we don't care about as they do not contain any information about "Bob"
2. one character than can be one of the 16
    1. 10 0000, so 'g'
    1. 10 0001, so 'h'
    1. 10 0010, so 'i'
    1. 10 0011, so 'j'
    1. 10 0100, so 'k'
    1. 10 0101, so 'l'
    1. 10 0110, so 'm'
    1. 10 0111, so 'n'
    1. 10 1000, so 'o'
    1. 10 1001, so 'p'
    1. 10 1010, so 'q'
    1. 10 1011, so 'r'
    1. 10 1100, so 's'
    1. 10 1101, so 't'
    1. 10 1110, so 'u'
    1. 10 1111, so 'v'

So looking for ("Bo")"b" into the clear text is "equivalent" (so far) to look for "Y[g-v]" into the base64-encoded text.

## **Intermediate result for the "Bob" case**

So now we have more information to look for "Bob" directly inside the base64-encoded:
1. "Qm9i" if "Bob" is in the same 3-characters chunk
2. "[EUk0]JvY[g-v]" if "Bo" and "b" are in 2 distinct chunks.

## **Let's analyse that second case xy"B", "ob"z**

### **First part xy"B"**

For x, we get abcdefgh so 8 bits. Each letter a to h is either 0 or 1.

For y, we get ijklmnop so 8 more bits. Each letter i to p is either 0 or 1.

For 'B', we still get 01000010 so 8 more bits.

| b01 | b02 | b03 | b04 | b05 | b06 |  | b07 | b08 | b09 | b10 | b11 | b12 |  | b13 | b14 | b15 | b16 | b17 | b18 |  | b19 | b20 | b21 | b22 | b23 | b24 |
| --- | --- | --- | --- | --- | --- | - | --- | --- | --- | --- | --- | --- | - | --- | --- | --- | --- | --- | --- | - | --- | --- | --- | --- | --- | --- |
| a | b | c | d | e | f |   | g | h | i | j | k | l |  | m | n | o | p | 0 | 1 | | 0 | 0 | 0 | 0 | 1 | 0 |

Yet again, as we already have 24 bits, no padding is required.
Now we will use the previous table to encode these 24 bits into 4 characters.
| b1 | b2 | b3 | b4 | b5 | b6 |  | Char |
| --- | --- | --- | --- | --- | - | --- | ---- |
| a | b | c | d | e | f | | See below 1.
| g | h | i | j | k | l | | See below 1.
| m | n | o | p | 0 | 1 | | See below 2.
| 0 | 0 | 0 | 0 | 1 | 0 | | C

So now we have :
1. two leading characters we don't care about as they do not contain any information about "Bob"
2. one character than can be one of the 16
    1. 0000 01, so 'B'
    1. 0001 01, so 'F'
    1. 0010 01, so 'J'
    1. 0011 01, so 'N'
    1. 0100 01, so 'R'
    1. 0101 01, so 'V'
    1. 0110 01, so 'Z'
    1. 0111 01, so 'd'
    1. 1000 01, so 'h'
    1. 1001 01, so 'l'
    1. 1010 01, so 'p'
    1. 1011 01, so 't'
    1. 1100 01, so 'x'
    1. 1101 01, so '1'
    1. 1110 01, so '5'
    1. 1111 01, so '9'

So looking for 'B'("ob" is coming thereafter) into the clear text is "equivalent" (so far) to look for "[BFJNRVZdhlptx159]C" into the base64-encoded text.

### **Second part "ob"z**

For 'o', we still get 01101111 so 8 more bits.

For 'b', we still get 01100010 so 8 bits.

For z, we get abcdefgh so 8 more bits. Each letter a to h is either 0 or 1.

| b01 | b02 | b03 | b04 | b05 | b06 |  | b07 | b08 | b09 | b10 | b11 | b12 |  | b13 | b14 | b15 | b16 | b17 | b18 |  | b19 | b20 | b21 | b22 | b23 | b24 |
| --- | --- | --- | --- | --- | --- | - | --- | --- | --- | --- | --- | --- | - | --- | --- | --- | --- | --- | --- | - | --- | --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 0 | 1 | 1 |   | 1 | 1 | 0 | 1 | 1 | 0 |  | 0 | 0 | 1 | 0 | a | b | | c | d | e | f | g | h |

Yet again, as we already have 24 bits, no padding is required.
Now we will use the previous table to encode these 24 bits into 4 characters.
| b1 | b2 | b3 | b4 | b5 | b6 |  | Char |
| --- | --- | --- | --- | --- | - | --- | ---- |
| 0 | 1 | 1 | 0 | 1 | 1 | | b |
| 1 | 1 | 0 | 1 | 1 | 0 | | 2 |
| 0 | 0 | 1 | 0 | a | b | | See below 1.
| c | d | e | f | g | h | | See below 2.

So now we have :
1. one trailing character we don't care about as it does not contain any information about "Bob"
2. one character than can be one of the 4:
    1. 0010 00, so 'I'
    2. 0010 01, so 'J'
    3. 0010 10, so 'K'
    4. 0010 11, so 'L'

So looking for ('B')"ob" into the clear text is "equivalent" (so far) to look for "b2[IJKL]" into the base64-encoded text.

## **Final result for the "Bob" case**

So now we have all information to look for "Bob" directly inside the base64-encoded:
1. "Qm9i" if "Bob" is in the same 3-characters chunk
2. "[EUk0]JvY[g-v]" if "Bo" and "b" are in 2 consecutive chunks.
3. "[BFJNRVZdhlptx159]Cb2[IJKL]" if "B" and "ob" are in 2 consecutive chunks.

## **Let's use this tool**

```
$ echo -n "Dear Bob!" | base64 | python3 -m search_base64.find Bob
-: found Bob => BCb2I # See case 3 above
$ echo -n "Dear  Bob!" | base64 | python3 -m search_base64.find Bob
-: found Bob => Qm9i # See case 1 above
$ echo -n "Dear   Bob!" | base64 | python3 -m search_base64.find Bob
-: found Bob => EJvYi # See case 2 above
```

# Let's talk about encoding

So far we assumed that one character was encoded as one byte. But Japanese people will disagree with us.

Look at how different is the result to base64-encoded 3 characters :
```
$ echo -n "abc" | base64
YWJj            #  4 b64 characters => 24 bits => 3*8 bits => 3 bytes
$ echo -n "日本語" | base64
5pel5pys6Kqe    # 12 b64 characters => 72 bits => 9*8 bits => 9 bytes
```

Thus we need to be careful to count the bytes of the characters, not the characters directly.

# **TODO**

- Finish this README
- Specify encoding of content
- Specify an encoding table
- More tests
- Optimize
- Regex?
- Non-printable character?

