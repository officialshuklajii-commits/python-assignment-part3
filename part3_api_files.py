# ============================================================
# Part 3: File I/O, APIs & Exception Handling
# Theme : Product Explorer & Error-Resilient Logger
# Author: Gaurav Anand Shukla  |  ID: BITSoM_BA_25111017
# File  : part3_api_files.py
# ============================================================
# This script fetches real product data from a public API,
# processes it, saves results to files, and handles all
# failure scenarios gracefully — like a production app.
# ============================================================

import requests
import datetime

# ============================================================
# GLOBAL ERROR LOGGER — used throughout the entire script
# ============================================================

def log_error(function_name, error_message):
    """
    Append a timestamped error entry to error_log.txt in append mode.
    Format: [YYYY-MM-DD HH:MM:SS] ERROR in <function>: <message>
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] ERROR in {function_name}: {error_message}\n"
    with open("error_log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(entry)


# Clear the log at the start of a fresh run (entries accumulate below)
with open("error_log.txt", "w", encoding="utf-8") as _f:
    pass


# ============================================================
# TASK 1 — File Read & Write Basics  (6 marks)
# ============================================================

print("\n" + "=" * 65)
print("  TASK 1 — File Read & Write Basics")
print("=" * 65)

# ─── Part A: Write ──────────────────────────────────────────

# Five required lines written using write mode ('w')
notes_to_write = [
    "Topic 1: Variables store data. Python is dynamically typed.",
    "Topic 2: Lists are ordered and mutable.",
    "Topic 3: Dictionaries store key-value pairs.",
    "Topic 4: Loops automate repetitive tasks.",
    "Topic 5: Exception handling prevents crashes.",
]

with open("python_notes.txt", "w", encoding="utf-8") as f:
    for line in notes_to_write:
        f.write(line + "\n")
print("File written successfully.")

# Two additional lines appended using append mode ('a')
extra_notes = [
    "Topic 6: Functions promote code reuse and readability.",
    "Topic 7: Modules and packages extend Python's built-in capabilities.",
]
with open("python_notes.txt", "a", encoding="utf-8") as f:
    for line in extra_notes:
        f.write(line + "\n")
print("Lines appended.")

# ─── Part B: Read ───────────────────────────────────────────

print("\n--- Reading python_notes.txt ---")

with open("python_notes.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

# 1. Print each line numbered, stripping the trailing newline (\n)
for i, line in enumerate(lines, start=1):
    print(f"  {i}. {line.rstrip()}")

# 2. Total line count
print(f"\nTotal lines in file: {len(lines)}")

# 3. Keyword search (case-insensitive)
keyword = input("\nEnter a keyword to search in the notes: ").strip()
matched = [line.rstrip() for line in lines if keyword.lower() in line.lower()]

if matched:
    print(f"\nLines containing '{keyword}':")
    for line in matched:
        print(f"  → {line}")
else:
    print(f"\nNo lines found containing '{keyword}'. Try a different keyword.")


# ============================================================
# TASK 2 — API Integration  (8 marks)
# ============================================================

print("\n" + "=" * 65)
print("  TASK 2 — API Integration")
print("=" * 65)

BASE_URL = "https://dummyjson.com/products"

# ─── Step 1: Fetch 20 products and display a formatted table ──
print("\n--- Step 1: Fetching 20 products from DummyJSON ---")
try:
    response = requests.get(f"{BASE_URL}?limit=20", timeout=5)
    if response.status_code == 200:
        products_20 = response.json()["products"]
        print(f"\n  {'ID':<5} {'Title':<32} {'Category':<18} {'Price':>9} {'Rating':>8}")
        print("  " + "-" * 76)
        for p in products_20:
            print(f"  {p['id']:<5} {p['title'][:31]:<32} {p['category'][:17]:<18}"
                  f" ${p['price']:>8.2f} {p['rating']:>8.2f}")
    else:
        print(f"  HTTP Error {response.status_code} while fetching products.")
        log_error("fetch_products", f"HTTPError — {response.status_code}")

except requests.exceptions.ConnectionError as e:
    print("  Connection failed. Please check your internet.")
    log_error("fetch_products", f"ConnectionError — {e}")
except requests.exceptions.Timeout:
    print("  Request timed out. Try again later.")
    log_error("fetch_products", "Timeout — request exceeded 5 s")
except Exception as e:
    print(f"  Unexpected error: {e}")
    log_error("fetch_products", str(e))

# ─── Step 2: Filter rating ≥ 4.5, sort by price descending ──
print("\n--- Step 2: Products with rating ≥ 4.5 (sorted by price, descending) ---")
try:
    response = requests.get(f"{BASE_URL}?limit=20", timeout=5)
    if response.status_code == 200:
        products_20 = response.json()["products"]
        filtered = [p for p in products_20 if p["rating"] >= 4.5]
        filtered.sort(key=lambda x: x["price"], reverse=True)
        if filtered:
            print(f"  {'Title':<38} {'Price':>10} {'Rating':>8}")
            print("  " + "-" * 58)
            for p in filtered:
                print(f"  {p['title'][:37]:<38} ${p['price']:>9.2f} {p['rating']:>8.2f}")
        else:
            print("  No products with rating ≥ 4.5 found.")
    else:
        print(f"  HTTP Error {response.status_code}.")
        log_error("filter_products", f"HTTPError — {response.status_code}")

except requests.exceptions.ConnectionError as e:
    print("  Connection failed. Please check your internet.")
    log_error("filter_products", f"ConnectionError — {e}")
except requests.exceptions.Timeout:
    print("  Request timed out. Try again later.")
    log_error("filter_products", "Timeout")
except Exception as e:
    print(f"  Unexpected error: {e}")
    log_error("filter_products", str(e))

# ─── Step 3: Search by category — laptops ────────────────────
print("\n--- Step 3: All products in the 'laptops' category ---")
try:
    response = requests.get(f"{BASE_URL}/category/laptops", timeout=5)
    if response.status_code == 200:
        laptops = response.json()["products"]
        print(f"  Found {len(laptops)} laptop(s):\n")
        for p in laptops:
            print(f"  • {p['title']:<44} ${p['price']:.2f}")
    else:
        print(f"  HTTP Error {response.status_code}.")
        log_error("fetch_laptops", f"HTTPError — {response.status_code}")

except requests.exceptions.ConnectionError as e:
    print("  Connection failed. Please check your internet.")
    log_error("fetch_laptops", f"ConnectionError — {e}")
except requests.exceptions.Timeout:
    print("  Request timed out. Try again later.")
    log_error("fetch_laptops", "Timeout")
except Exception as e:
    print(f"  Unexpected error: {e}")
    log_error("fetch_laptops", str(e))

# ─── Step 4: Simulated POST request ──────────────────────────
print("\n--- Step 4: POST Request — Simulated Add Product ---")
new_product_payload = {
    "title":       "My Custom Product",
    "price":       999,
    "category":    "electronics",
    "description": "A product I created via API",
}
try:
    response = requests.post(f"{BASE_URL}/add", json=new_product_payload, timeout=5)
    print(f"  Status Code : {response.status_code}")
    print(f"  Response    : {response.json()}")
    print("  Note: DummyJSON is a mock API — no data is actually stored server-side.")

except requests.exceptions.ConnectionError as e:
    print("  Connection failed. Please check your internet.")
    log_error("post_product", f"ConnectionError — {e}")
except requests.exceptions.Timeout:
    print("  Request timed out. Try again later.")
    log_error("post_product", "Timeout")
except Exception as e:
    print(f"  Unexpected error: {e}")
    log_error("post_product", str(e))


# ============================================================
# TASK 3 — Exception Handling  (7 marks)
# ============================================================

print("\n" + "=" * 65)
print("  TASK 3 — Exception Handling")
print("=" * 65)

# ─── Part A: Guarded Calculator ──────────────────────────────

def safe_divide(a, b):
    """
    Divide a by b safely.
    Returns:
      - float result of a / b on success
      - 'Error: Cannot divide by zero'  on ZeroDivisionError
      - 'Error: Invalid input types'    on TypeError
    """
    try:
        return a / b
    except ZeroDivisionError:
        return "Error: Cannot divide by zero"
    except TypeError:
        return "Error: Invalid input types"


print("\n--- Part A: safe_divide ---")
print(f"  safe_divide(10, 2)     = {safe_divide(10, 2)}")
print(f"  safe_divide(10, 0)     = {safe_divide(10, 0)}")
print(f"  safe_divide('ten', 2)  = {safe_divide('ten', 2)}")


# ─── Part B: Guarded File Reader ─────────────────────────────

def read_file_safe(filename):
    """
    Try to open and read the given file.
    - Returns full content as a string on success.
    - Catches FileNotFoundError with a helpful message.
    - The finally block ALWAYS runs whether the file exists or not.
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
        return content
    except FileNotFoundError:
        print(f"  Error: File '{filename}' not found.")
        return None
    finally:
        print("  File operation attempt complete.")


print("\n--- Part B: read_file_safe ---")

print("  Testing 'python_notes.txt'  (should succeed):")
content = read_file_safe("python_notes.txt")
if content:
    preview = "\n".join(content.splitlines()[:2])
    print(f"  Preview:\n    {preview}\n    ...")

print("\n  Testing 'ghost_file.txt'  (should fail gracefully):")
read_file_safe("ghost_file.txt")


# ─── Part C: Robust API Calls ────────────────────────────────
# Every requests.get() and requests.post() call in Task 2 is
# already wrapped in try-except blocks that handle:
#   • ConnectionError  → "Connection failed. Please check your internet."
#   • Timeout          → "Request timed out. Try again later."
#   • Exception        → prints the error message
# This fully satisfies Part C.
print("\n--- Part C: Robust API Calls ---")
print("  ✓ All API calls in Task 2 are wrapped in try-except blocks.")
print("  ✓ Handles: ConnectionError, Timeout, and any unexpected Exception.")
print("  ✓ timeout=5 is passed to every requests call.")


# ─── Part D: Input Validation Loop ───────────────────────────
print("\n--- Part D: Input Validation Loop ---")
print("  Validates product ID (1–100) before making an API call.\n")

while True:
    user_input = input("Enter a product ID to look up (1–100), or 'quit' to exit: ").strip()

    # Exit condition
    if user_input.lower() == "quit":
        print("  Exiting product lookup.")
        break

    # Guard 1: must be a valid integer
    try:
        product_id = int(user_input)
    except ValueError:
        print("  ⚠ Warning: Please enter a valid integer between 1 and 100.")
        continue

    # Guard 2: must be within range 1–100
    if not (1 <= product_id <= 100):
        print("  ⚠ Warning: ID must be between 1 and 100. Please try again.")
        continue

    # Valid ID — make the API call
    try:
        response = requests.get(f"{BASE_URL}/{product_id}", timeout=5)
        if response.status_code == 200:
            p = response.json()
            print(f"  ✓ Found: {p['title']}  |  Price: ${p['price']}")
        elif response.status_code == 404:
            print(f"  ✗ Product not found for ID: {product_id}.")
            log_error("lookup_product",
                      f"HTTPError — 404 Not Found for product ID {product_id}")
        else:
            print(f"  ✗ HTTP Error: {response.status_code}")
            log_error("lookup_product",
                      f"HTTPError — {response.status_code} for product ID {product_id}")

    except requests.exceptions.ConnectionError as e:
        print("  Connection failed. Please check your internet.")
        log_error("lookup_product", f"ConnectionError — {e}")
    except requests.exceptions.Timeout:
        print("  Request timed out. Try again later.")
        log_error("lookup_product", f"Timeout for product ID {product_id}")
    except Exception as e:
        print(f"  Unexpected error: {e}")
        log_error("lookup_product", str(e))


# ============================================================
# TASK 4 — Logging to File  (4 marks)
# ============================================================

print("\n" + "=" * 65)
print("  TASK 4 — Logging to File")
print("=" * 65)

print("\n  error_log.txt opens in APPEND mode — entries accumulate across runs.")
print("  Format: [TIMESTAMP] ERROR in <function>: <message>\n")

# --- Trigger 1: ConnectionError — hit a genuinely unreachable URL ---
print("--- Trigger 1: ConnectionError (unreachable URL) ---")
try:
    requests.get("https://this-host-does-not-exist-xyz.com/api", timeout=5)
except requests.exceptions.ConnectionError as e:
    print("  Connection failed as expected. Logging to error_log.txt ...")
    log_error("fetch_products", f"ConnectionError — {e}")
except Exception as e:
    log_error("fetch_products", str(e))

# --- Trigger 2: HTTP 404 — product ID 999 does not exist ---
# Important: A 404 is NOT a Python exception — detect via response.status_code
print("\n--- Trigger 2: HTTP 404 (product ID 999 does not exist) ---")
try:
    response = requests.get(f"{BASE_URL}/999", timeout=5)
    if response.status_code != 200:
        print(f"  HTTP {response.status_code} received. Logging to error_log.txt ...")
        log_error("lookup_product",
                  f"HTTPError — {response.status_code} Not Found for product ID 999")
except requests.exceptions.ConnectionError as e:
    log_error("lookup_product", f"ConnectionError — {e}")
except Exception as e:
    log_error("lookup_product", str(e))

# --- Read and print the full contents of error_log.txt ---
print("\n--- Full contents of error_log.txt ---")
try:
    with open("error_log.txt", "r", encoding="utf-8") as f:
        log_content = f.read()
    if log_content.strip():
        print(log_content)
    else:
        print("  (No errors were logged this run.)")
except FileNotFoundError:
    print("  error_log.txt not found — no errors were logged.")
