
# Overview

Mediscore calculation is a python based scoring system
which is designed to assess a patients vital signs and detect their potential health issues.
The following system follows a structured scoring model.
The following features are used to determine the mediscore.
**Respiration rate**, **Saturated oxygen level (SpO2)**, **consciousness**, **body temperature** and **oxygen usage**.
For a more comprehensive assesment additional factors like **Capillary Blood Glucose (CBL)** are also included.

This Medi-Score calculation system helps the health care profesionals quickly assess the 
patients deterioration and issue alerts for significant changes.
# Installation
To use the medi score calculator, you need to install python 3.6 or higher.
Following steps can be used:

1.Clone the repository- <pre>git clone https://github.com/yourusername/medi-score.git
cd medi-score</pre>

2.Install dependencies- <pre> pip install -r requirements.txt</pre>

3.Run the script-  <pre> python medi_score.py </pre>

# Usage
### Function- Calculate_Medi_score

```calculate_medi_score``(respiration_rate, oxygen_saturation, consciousness, temperature, air_or_oxygen, cbg=None, fasting=None, previous_score=None```

| Parameter          | Type   | Description                                      |
|--------------------|--------|--------------------------------------------------|
| respiration_rate    | int    | Breaths per minute (0-50).                       |
| oxygen_saturation   | int    | SpO₂ percentage (0-100).                         |
| consciousness       | int    | 0 for alert, non-zero for confused/unconscious.  |
| temperature         | float  | Body temperature in Celsius (30.0-42.0°C).       |
| air_or_oxygen       | int    | 0 for breathing air, 2 for supplemental oxygen.  |
| cbg (optional)      | float  | Capillary Blood Glucose (mmol/L).                |
| fasting (optional)  | bool   | True if fasting, False if not.                   |
| previous_score (optional) | int | Previous Medi Score (to check for trend alerts). |

# Scoring System

### Respiration_rate

| Range (breaths per min) | Score |
|-------------------------|-------|
| ≤8                      | 3     |
| 9 – 11                   | 2     |
| 12 – 20                  | 0 (Normal) |
| 21 – 24                  | 2     |
| ≥25                      | 3     |

### Oxygen_Saturation

| SpO₂ (%)   | Score (Air) | Score (Oxygen) |
|-------------|-------------|----------------|
| ≤83         | 3           | 3              |
| 84 – 85     | 2           | 2              |
| 86 – 87     | 1           | 1              |
| 88 – 92     | 0 (Normal)  | 1              |
| 93 – 94     | -           | 1              |
| 95 – 96     | -           | 2              |


### Consciousness

| Consciousness | Condition          | Score |
|---------------|--------------------|-------|
| Alert (0)     | -                  | 0     |
| Confused/Unconscious (1) | -          | 3     |



### Temperature 

| Temperature (°C) | Score           |
|------------------|-----------------|
| ≤35.0            | 3               |
| 35.1 – 36.0      | 2               |
| 36.1 – 38.0      | 0 (Normal)      |
| 38.1 – 39.0      | 1               |
| ≥39.1            | 2               |

### CBG when fasting

| CBG (mmol/L)   | Score (Fasting) |
|-----------------|-----------------|
| ≤3.4           | 3               |
| 3.5 – 3.9      | 2               |
| 4.0 – 5.4      | 1               |
| 5.5 – 5.9      | 0               |
| ≥6.0           | 1               |

### CBG 2 hours after eating

| CBG (mmol/L)   | Score (Post-meal) |
|-----------------|-------------------|
| ≤4.5           | 3                 |
| 4.5 – 5.8      | 2                 |
| 5.9 – 7.8      | 1                 |
| 7.9 – 8.9      | 0                 |
| ≥9.0           | 1                 |


# Medi Score Explanation

### Summary of Medi Scores
 1.Score 0 (Normal): The patient’s vital signs are within the healthy range, and there are no immediate concerns.

 2.Score 4 (Mild Concern): The patient is stable but requires closer monitoring, particularly if on supplemental oxygen or exhibiting mild symptoms.

 3.Score 8 (Moderate Concern): The patient’s condition warrants more immediate attention. Vital signs are outside the normal range, and the patient may require further medical intervention.


The Medi Score helps healthcare professionals quickly assess and respond to the patient’s health status. If the score changes significantly (by more than 2 points) within 24 hours, an alert will be triggered to signal possible deterioration in the patient’s condition.

## Example Usage
<pre>

from medi_score import calculate_medi_score

score, alert = calculate_medi_score(23, 88, 1, 38.5, 2, cbg=4.0, fasting=True, previous_score=5)
print(f"Medi Score: {score}")
if alert:
    print(alert)

</pre>
# Output
`Medi Score: 10
ALERT: Medi Score increased by more than 2 points in 24 hours!`

# Testing

The repository includes unit tests to validate the scoring system. Run tests using:
<pre>
python -m unittest test_medi_score.py
</pre>

## Example test cases from the code

<pre>import unittest
from medi_score import calculate_medi_score

class TestMediScore(unittest.TestCase):
    def test_normal_case(self):
        self.assertEqual(calculate_medi_score(15, 95, 0, 37.1, 0)[0], 0)

    def test_patient_on_oxygen(self):
        self.assertEqual(calculate_medi_score(17, 95, 0, 37.1, 2)[0], 4)

    def test_severe_case(self):
        self.assertEqual(calculate_medi_score(23, 88, 1, 38.5, 2)[0], 10)

if __name__ == "__main__":
    unittest.main()</pre>