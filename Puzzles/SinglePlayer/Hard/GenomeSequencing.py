import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

n = int(input())
seqs = [input() for _ in range(n)]


def best_combine(seq1, seq2):
    l1 = len(seq1)
    l2 = len(seq2)
    best_shortening = 0
    shortest_combined = seq1 + seq2
    for i in range(-l2 + 1, l1):
        start1 = max(0, i)
        end1 = min(l1, l2 + i)
        start2 = max(0, -i)
        end2 = min(l2, l1 - i)
        # print("i=", i, "start1=", start1, "end1=", end1, "start2=", start2, "end2=", end2, file=sys.stderr)
        # print("subseq1=", seq1[start1:end1], "subseq2=", seq2[start2:end2], file=sys.stderr)
        if seq1[start1:end1] == seq2[start2:end2]:
            if i < 0:
                if l2 + i <= l1:
                    print("Case1", file=sys.stderr)
                    # seq2 overlaps left side of seq1 only
                    length = l1 - i
                    combined = seq2[:-i] + seq1
                else:
                    # seq2 longer than seq1 and seq1 is subsequence
                    print("Case2", file=sys.stderr)
                    length = l2
                    combined = seq2
            elif i + l2 <= l1:
                # seq2 completely in seq1
                print("Case3", file=sys.stderr)
                length = l1
                combined = seq1
            else:
                # seq2 overlaps right side of seq1 only
                print("Case4", file=sys.stderr)
                length = l2 + i
                combined = seq1[:i] + seq2
            print("i=", i, "seq1=", seq1, "seq2=", seq2, "equal part=", seq1[start1:end1], "Length", length, "combined",
                  combined, file=sys.stderr)
            shortening = l1 + l2 - length
            if shortening > best_shortening:
                best_shortening = shortening
                shortest_combined = combined
    return shortest_combined


def explore(s):
    if len(s) == 1:
        return s[0]
    if len(s) == 2:
        return best_combine(*s)
    best_length = float('inf')
    best_combined = None
    for i in range(len(s)):
        curr = s[i]
        other = s[:]
        del other[i]
        other_combined = explore(other)
        combined = best_combine(curr, other_combined)
        length = len(combined)
        if length < best_length:
            best_length = length
            best_combined = combined
    return best_combined


print(len(explore(seqs)))

