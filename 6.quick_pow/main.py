import time

from tools import fast_pow, naive_pow

a, b, m = 2, 512, 10**9 + 7

start = time.perf_counter()
res1 = naive_pow(a, b, m)
end = time.perf_counter()
print(f"🐢 naive_pow time: {end - start:.6f} sec")
print(f"naive_pow result: {res1}")
print(f"naive_pow steps: {b}\n")

start = time.perf_counter()
res, steps = fast_pow(a, b, m, verbose=False)
end = time.perf_counter()
print(f"⏱ fast_pow time: {end - start:.6f} sec")
print(f"fast_pow result: {res}")
print(f"fast_pow steps: {steps}\n")

assert res1 == res, "Results do not match"

# res, steps = fast_pow(a, b, m, verbose=True)
# print(f"fast_pow result: {res}, steps: {steps}")