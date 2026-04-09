PARAMETERS = {
    "hemoglobin": {"min": 12, "max": 16},
    "wbc": {"min": 4000, "max": 11000},
    "platelets": {"min": 150000, "max": 450000},
    "rbc": {"min": 4.0, "max": 6.0},
    "glucose": {"min": 70, "max": 140}
}

def analyze_report(data):
    result = {}

    for param, value in data.items():
        if param in PARAMETERS:
            min_val = PARAMETERS[param]["min"]
            max_val = PARAMETERS[param]["max"]

            if value < min_val:
                status = "low"
            elif value > max_val:
                status = "high"
            else:
                status = "normal"

            result[param] = {
                "value": value,
                "status": status
            }

    return result