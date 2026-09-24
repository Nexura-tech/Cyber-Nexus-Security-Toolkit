import string

from core.reporter import save_json, save_text


def analyze_password(password):
    result = {
        "length": len(password),
        "uppercase": any(char.isupper() for char in password),
        "lowercase": any(char.islower() for char in password),
        "digits": any(char.isdigit() for char in password),
        "special": any(char in string.punctuation for char in password),
    }

    score = sum([
        result["length"] >= 8,
        result["length"] >= 12,
        result["uppercase"],
        result["lowercase"],
        result["digits"],
        result["special"],
    ])

    if score <= 2:
        strength = "Weak"
    elif score <= 4:
        strength = "Medium"
    else:
        strength = "Strong"

    result["score"] = score
    result["strength"] = strength

    return result


def run():
    print("\nPassword Analyzer")
    print("-" * 30)

    password = input("Enter test password: ")

    result = analyze_password(password)

    print("\nAnalysis Result")
    print("-" * 30)
    print(f"Length: {result['length']}")
    print(f"Uppercase: {'YES' if result['uppercase'] else 'NO'}")
    print(f"Lowercase: {'YES' if result['lowercase'] else 'NO'}")
    print(f"Numbers: {'YES' if result['digits'] else 'NO'}")
    print(f"Special Characters: {'YES' if result['special'] else 'NO'}")
    print(f"Score: {result['score']}/6")
    print(f"\nStrength: {result['strength']}")

    report_data = {
        "module": "Password Analyzer",
        "result": result,
    }

    json_file = save_json(report_data)

    text_data = {
        "Module": "Password Analyzer",
        "Length": result["length"],
        "Uppercase": result["uppercase"],
        "Lowercase": result["lowercase"],
        "Digits": result["digits"],
        "Special Characters": result["special"],
        "Score": f"{result['score']}/6",
        "Strength": result["strength"],
    }

    text_file = save_text("Cyber Nexus Password Analysis Report", text_data)

    print("\nReports Generated")
    print("-" * 30)
    print(f"JSON: {json_file}")
    print(f"TXT:  {text_file}")


if __name__ == "__main__":
    run()
