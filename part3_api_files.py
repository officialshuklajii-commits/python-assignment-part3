# ============================================================
# Part 3: File I/O, APIs & Exception Handling
# Theme : Product Explorer & Error-Resilient Logger
# Author: Gaurav Anand Shukla | ID: BITSoM_BA_25111017
# File  : part3_api_files.py
# ============================================================
# pip install requests  (if not already installed)
# ============================================================

import requests
import datetime

# ============================================================
# TASK 1 — File Read & Write Basics (6 marks)
# ============================================================

print("\n" + "=" * 55)
print(" TASK 1 — File Read & Write Basics")
print("=" * 55)

notes_file = "python_notes.txt"

# --- Part A: Write ---
lines_to_write = [
    "Topic 1: Variables store data. Python is dynamically typed.",
    "Topic 2: Lists are ordered and mutable.",
    "Topic 3: Dictionaries store key-value pairs.",
    "Topic 4: Loops automate repetitive tasks.",
    "Topic 5: Exception handling prevents crashes.",
]

# Write mode — creates / overwrites the file
with open(notes_file, "w", encoding="utf-8") as f:
    for line in lines_to_write:
        f.write(line + "\n")
print(f"\nFile written successfully. ({len(lines_to_write)} lines written)")

# Append two more lines
extra_lines = [
    "Topic 6: Functions promote code reuse and modularity.",
    "Topic 7: Modules allow you to organise code across files.",
]
with open(notes_file, "a", encoding="utf-8") as f:
    for line in extra_lines:
        f.write(line + "\n")
print("Lines appended.")

# --- Part B: Read ---
with open(notes_file, "r", encoding="utf-8") as f:
    all_lines = [line.rstrip("\n") for line in f]

print(f"\nAll lines (numbered):")
for i, line in enumerate(all_lines, start=1):
    print(f"  {i}. {line}")

print(f"\nTotal number of lines: {len(all_lines)}")

# Keyword search (case-insensitive)
keyword = "python"
print(f"\nLines containing keyword '{keyword}':")
matched = [line for line in all_lines if keyword.lower() in line.lower()]
if matched:
    for line in matched:
        print(f"  → {line}")
else:
    print("  No matches found.")

# ============================================================
# TASK 2 — API Integration (8 marks)
# ============================================================

print("\n" + "=" * 55)
print(" TASK 2 — API Integration")
print("=" * 55)

BASE_URL = "https://dummyjson.com/products"


def log_error(context, error_msg):
    """Write a timestamped error entry to error_log.txt (append mode)."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] ERROR in {context}: {error_msg}\n"
    with open("error_log.txt", "a", encoding="utf-8") as ef:
        ef.write(entry)
    print(f"  [Logged] {entry.strip()}")


# Step 1 — Fetch and display 20 products
print("\nStep 1: Fetching 20 products from DummyJSON API...")
products = []
try:
    response = requests.get(f"{BASE_URL}?limit=20", timeout=5)
    response.raise_for_status()
    data = response.json()
    products = data.get("products", [])

    print(f"\n{'ID':<5} {'Title':<30} {'Category':<18} {'Price':>8} {'Rating':>7}")
    print("-" * 72)
    for p in products:
        print(f"  {p['id']:<4} {p['title']:<30} {p['category']:<18} "
              f"${p['price']:>8.2f} {p['rating']:>7.2f}")

except requests.exceptions.ConnectionError as e:
    log_error("fetch_products", f"ConnectionError — {e}")
except requests.exceptions.Timeout as e:
    log_error("fetch_products", f"Timeout — {e}")
except Exception as e:
    log_error("fetch_products", str(e))

# Step 2 — Filter & Sort (rating >= 4.5, descending price)
print("\nStep 2: Filtered products (rating ≥ 4.5), sorted by price descending:")
high_rated = [p for p in products if p.get("rating", 0) >= 4.5]
high_rated.sort(key=lambda p: p["price"], reverse=True)
for p in high_rated:
    print(f"  {p['title']:<30} ${p['price']:.2f}  ★{p['rating']}")

# Step 3 — Search by category: laptops
print("\nStep 3: Fetching all products in category 'laptops'...")
try:
    response = requests.get(f"{BASE_URL}/category/laptops", timeout=5)
    response.raise_for_status()
    laptops = response.json().get("products", [])
    for p in laptops:
        print(f"  {p['title']:<35} ${p['price']:.2f}")
except requests.exceptions.ConnectionError as e:
    log_error("fetch_laptops", f"ConnectionError — {e}")
except requests.exceptions.Timeout as e:
    log_error("fetch_laptops", f"Timeout — {e}")
except Exception as e:
    log_error("fetch_laptops", str(e))

# Step 4 — POST request (simulated)
print("\nStep 4: Sending POST request to add a new product (simulated)...")
new_product = {
    "title":       "My Custom Product",
    "price":       999,
    "category":    "electronics",
    "description": "A product I created via API"
}
try:
    response = requests.post(f"{BASE_URL}/add", json=new_product, timeout=5)
    response.raise_for_status()
    print("  Full response from server:")
    print(f"  {response.json()}")
except requests.exceptions.ConnectionError as e:
    log_error("add_product", f"ConnectionError — {e}")
except requests.exceptions.Timeout as e:
    log_error("add_product", f"Timeout — {e}")
except Exception as e:
    log_error("add_product", str(e))

# ============================================================
# TASK 3 — Exception Handling (7 marks)
# ============================================================

print("\n" + "=" * 55)
print(" TASK 3 — Exception Handling")
print("=" * 55)

# --- Part A: Guarded Calculator ---
def safe_divide(a, b):
    """Return a / b with guarded exception handling."""
    try:
        return a / b
    except ZeroDivisionError:
        return "Error: Cannot divide by zero"
    except TypeError:
        return "Error: Invalid input types"

print("\nPart A — safe_divide tests:")
for a, b in [(10, 2), (10, 0), ("ten", 2)]:
    result = safe_divide(a, b)
    print(f"  safe_divide({a!r}, {b!r}) → {result}")

# --- Part B: Guarded File Reader ---
def read_file_safe(filename):
    """Read a file safely, catching FileNotFoundError."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
        return content
    except FileNotFoundError:
        print(f"  Error: File '{filename}' not found.")
        return None
    finally:
        print("  File operation attempt complete.")

print("\nPart B — read_file_safe tests:")
print(f"\n  Reading 'python_notes.txt' (should succeed):")
content = read_file_safe("python_notes.txt")
if content:
    print(f"  [Read {len(content)} characters successfully]")

print(f"\n  Reading 'ghost_file.txt' (should fail gracefully):")
read_file_safe("ghost_file.txt")

# --- Part C: Robust API Calls — already wrapped above in Task 2 ---
print("\nPart C — All API calls in Task 2 are already wrapped in try-except blocks.")
print("  (ConnectionError, Timeout, and any unexpected Exception are handled.)")

# --- Part D: Input Validation Loop ---
print("\nPart D — Product lookup loop (enter 'quit' to exit):")
while True:
    user_input = input("  Enter a product ID to look up (1–100), or 'quit' to exit: ").strip()
    if user_input.lower() == "quit":
        print("  Exiting product lookup.")
        break

    # Validate: must be an integer in range 1–100
    try:
        product_id = int(user_input)
    except ValueError:
        print("  ⚠ Warning: Please enter a valid integer between 1 and 100.")
        continue

    if not (1 <= product_id <= 100):
        print("  ⚠ Warning: ID must be between 1 and 100.")
        continue

    # Make the API call
    try:
        resp = requests.get(f"{BASE_URL}/{product_id}", timeout=5)
        if resp.status_code == 404:
            print(f"  Product not found (ID {product_id}).")
            log_error("lookup_product", f"HTTPError — 404 Not Found for product ID {product_id}")
        elif resp.status_code == 200:
            prod = resp.json()
            print(f"  Title : {prod['title']}")
            print(f"  Price : ${prod['price']:.2f}")
        else:
            print(f"  Unexpected status code: {resp.status_code}")
    except requests.exceptions.ConnectionError as e:
        log_error("lookup_product", f"ConnectionError — {e}")
    except requests.exceptions.Timeout as e:
        log_error("lookup_product", f"Timeout — Request timed out. Try again later.")
    except Exception as e:
        log_error("lookup_product", str(e))

# ============================================================
# TASK 4 — Logging to File (4 marks)
# ============================================================

print("\n" + "=" * 55)
print(" TASK 4 — Logging to File")
print("=" * 55)

# The log_error() function defined in Task 2 already handles all logging.
# It writes to error_log.txt in append mode with timestamps.
# Here we intentionally trigger two logged entries to prove the logger works.

print("\nTriggering two intentional logged errors to prove the logger works...")

# Trigger 1: ConnectionError — unreachable URL
unreachable_url = "https://this-host-does-not-exist-xyz.com/api"
try:
    requests.get(unreachable_url, timeout=5)
except requests.exceptions.ConnectionError as e:
    log_error("fetch_products", f"ConnectionError — {e}")
except Exception as e:
    log_error("fetch_products", f"ConnectionError — No connection could be made")

# Trigger 2: 404 HTTP error for a product ID that doesn't exist
bad_id = 999
try:
    resp = requests.get(f"{BASE_URL}/{bad_id}", timeout=5)
    if resp.status_code != 200:
        log_error("lookup_product", f"HTTPError — {resp.status_code} Not Found for product ID {bad_id}")
except requests.exceptions.ConnectionError as e:
    log_error("lookup_product", f"ConnectionError — {e}")
except requests.exceptions.Timeout as e:
    log_error("lookup_product", f"Timeout — Request timed out.")
except Exception as e:
    log_error("lookup_product", str(e))

# Read and print the full contents of error_log.txt
print("\n--- Full contents of error_log.txt ---")
try:
    with open("error_log.txt", "r", encoding="utf-8") as ef:
        log_contents = ef.read()
    print(log_contents)
except FileNotFoundError:
    print("  (error_log.txt not found — no errors were logged yet)")
