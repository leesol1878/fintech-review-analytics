from google_play_scraper import reviews

# Try alternative CBE package
packages = [
    "com.combanketh.mobilebanking",
    "com.cbe.mobile"
]

for pkg in packages:
    print(f"Testing: {pkg}")
    result, _ = reviews(pkg, lang='en', country='us', count=100)
    print(f"  Found: {len(result)} reviews")