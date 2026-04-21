# Epistemic Alignment Trap — Investment Experiment

Complete web experiment for the Epistemic Alignment Trap study.
Built with Python Flask. Ready to deploy on Render.com for free.

## What This App Does

- Pre-survey: 4 questions (hold duration, goal, risk tolerance, sector)
- Randomly assigns participants to Condition A (persistent memory) or Condition B (forgetting)
- 15 investment rounds — Technology sector stocks
- Confidence slider + allocation slider ($1,000 split) in every round
- Feedback summaries after Round 5 and Round 10
- Full portfolio results after Round 15
- Post-survey: demographics + manipulation check + open text
- Saves all data to responses.csv automatically

## Deploy to Render.com — Step by Step

### Step 1 — Create GitHub Repository

1. Go to github.com — sign in or create free account
2. Click "New repository"
3. Name it: epistemic-alignment-experiment
4. Click "Create repository"
5. Upload all files from this folder to the repository

### Step 2 — Deploy on Render

1. Go to render.com — sign in or create free account
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Set these settings:
   - Name: epistemic-alignment-experiment
   - Environment: Python 3
   - Build Command: pip install -r requirements.txt
   - Start Command: gunicorn app:app --workers 2 --bind 0.0.0.0:$PORT
5. Add Environment Variables:
   - SECRET_KEY = any_random_string_here_2024
   - DATA_PASSWORD = your_chosen_password
6. Click "Create Web Service"
7. Wait 2-3 minutes for deployment
8. Your app URL will be: https://epistemic-alignment-experiment.onrender.com

### Step 3 — Add Your Charts

1. Create folder: static/charts/
2. Upload your PNG chart files:
   R1_A_TechCore_Inc.png
   R1_B_DataStream_Ltd.png
   R2_A_CloudVault_Corp.png
   ... etc for all 30 charts
3. If charts are not uploaded — the app shows auto-generated placeholder charts

### Step 4 — Connect to Prolific

1. Your study URL: https://your-app.onrender.com/?PROLIFIC_PID={{%PROLIFIC_PID%}}
2. Set completion URL in Prolific: https://app.prolific.com/submissions/complete?cc=YOUR_CODE
3. Update the completion code in thankyou.html

### Step 5 — Download Your Data

1. Go to: https://your-app.onrender.com/data?pw=your_chosen_password
2. This downloads responses.csv with all participant data
3. Import into SPSS or R for analysis

## File Structure

```
experiment/
├── app.py                 -- Main Flask application
├── requirements.txt       -- Python dependencies
├── Procfile               -- Render deployment command
├── README.md              -- This file
├── templates/
│   ├── base.html          -- Base template with styling
│   ├── prestudy.html      -- Pre-survey (4 questions)
│   ├── round.html         -- Investment round page
│   ├── trajectory.html    -- Stock movement charts
│   ├── feedback.html      -- Feedback after rounds 5 and 10
│   ├── final_results.html -- Portfolio results after round 15
│   ├── post_survey.html   -- Demographics and manipulation check
│   └── thankyou.html      -- Completion page
└── static/
    └── charts/            -- Upload your PNG chart images here
```

## Data Variables Saved

For each participant:
- participant_id, condition (A or B), prolific_id
- hold_duration, investment_goal, risk_tolerance, sector_choice
- R1_alloc through R15_alloc — allocation slider value 0-100
- R1_conf through R15_conf — confidence slider value 0-100
- R1_aci through R15_aci — calculated ACI per round
- R1_return through R15_return — dollar return per round
- total_return, benchmark_return, portfolio_score
- mean_confidence, mean_accuracy, oci, mean_aci
- Demographics and manipulation check

## Key Calculations

OCI = Mean Confidence - Mean Accuracy
ACI = |allocation - 50| * 2 / 100
Accuracy = 1 if actual_return >= benchmark_return, else 0
Benchmark = $500 in each stock equal split

## Contact

Raj — PhD Student, MIS Department
University of Houston, Bauer College of Business
Supervised by Professor Xiao
