from fpdf import FPDF
import os

def create_pdf(text, filename, folder):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)
    
    # Clean text to fallback to latin-1
    clean_text = text.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 6, clean_text)
    
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    pdf.output(filepath)
    print(f"Created {filepath}")

base_dir = "data/hr_policies"

# 1. Employee Handbook
handbook_text = """EMPLOYEE HANDBOOK - COMPANY X

I. Welcome and Company Overview
Welcome to Company X! We are thrilled to have you join our innovative team. This handbook is your guide to understanding our culture, policies, and the resources available to help you thrive here.
Our Mission: To revolutionize the industry with cutting-edge solutions.
Our Values: Innovation, Integrity, Teamwork, and Customer Focus.

II. Employment Essentials
Employment with Company X is at-will. We are an equal opportunity employer and do not discriminate based on race, color, religion, sex, or any other protected status.
Confidentiality: Employees are entrusted with proprietary information and must sign an NDA.
Intellectual Property: All works created during employment belong to the company.

III. Workplace Guidelines
Code of Conduct: We expect integrity and professionalism. Harassment and discrimination are strictly prohibited.
Technology Usage: Company devices and internet are for business use. Data security is paramount; use strong passwords and report incidents immediately.
Work Hours: Standard hours are 9:00 AM to 6:00 PM, Monday to Friday.

IV. Compensation and Benefits
We offer competitive salaries and a comprehensive benefits package including health insurance and 401k. Paychecks are issued bi-weekly.
Paid Time Off (PTO): Detailed in the Leave Policy.
Holidays: We observe 10 national holidays.

V. Employee Development
Performance Reviews: Conducted annually to provide feedback and set goals.
Training: We support continuous learning through workshops and online courses.

VI. Safety
We are committed to a safe workplace. Report any hazards immediately. In emergencies, follow the posted evacuation routes.
"""
create_pdf(handbook_text, "sample_handbook_companyX.pdf", os.path.join(base_dir, "handbook"))

# 2. Leave Policy
leave_text = """LEAVE POLICY 2024

1. General Principles
Applies to all confirmed employees. Leave year is Jan-Dec.
All leaves must be applied for on the HR portal.

2. Types of Leave
2.1 Casual Leave (CL)
- Entitlement: 12 days per annum.
- Purpose: Personal urgent work or short downtime.
- Pro-rata for new joinees.
- Max duration: 3 days at a time.
- Lapses at year-end (no carry forward).

2.2 Sick Leave (SL)
- Entitlement: 10 days per annum.
- Purpose: Medical recovery.
- Medical Certificate required for absence > 2 days.
- Lapses at year-end.

2.3 Earned Leave (EL) / Privilege Leave
- Entitlement: 15 days per annum (approx 1.25 per month).
- Eligibility: After probation period.
- Purpose: Planned vacations. Apply 2 weeks in advance.
- Carry Forward: Up to 45 days.
- Encashment: Allowed only at time of exit.

3. Holidays
Total 10 paid public holidays per year as per the published calendar.

4. Unpaid Leave (LOP)
Leaves taken beyond entitlement will be treated as Loss of Pay.
"""
create_pdf(leave_text, "leave_policy_template.pdf", os.path.join(base_dir, "leave"))

# 3. Reimbursement Policy
reimbursement_text = """TRAVEL AND EXPENSE REIMBURSEMENT POLICY

1. Objective
To provide guidelines for business travel and expense claims.

2. Scope
Applies to all employees traveling for official business.

3. Travel Rules
- Approvals: Pre-approval required from Manager for all travel.
- Flight: Economy class for domestic/short-haul. Books via admin team.
- Train: AC 2-Tier or 3-Tier allowed.
- Taxi: Uber/Ola/Prepaid cab reimbursed for airport transfers and client visits.

4. Accommodation
- Tier 1 Cities: Up to INR 5000 / $150 per night.
- Tier 2 Cities: Up to INR 3000 / $100 per night.
- Stay in partner hotels preferred.

5. Daily Allowance (Per Diem)
- Fixed flat allowance of INR 800 / $50 per day for meals/incidentals when traveling.
- No bills required for flat per diem. OR Actuals up to limit with bills.

6. Expense Submission
- Submit claim via Expense Portal within 15 days of return.
- Original physical bills required for any single expense > INR 1000.
- Approval workflow: Reporting Manager -> Finance.
- Payout: Within 7 working days of approval.

7. Non-Reimbursable
Alcohol, personal entertainment, traffic fines, laundry (unless trip > 7 days).
"""
create_pdf(reimbursement_text, "travel_reimbursement_policy.pdf", os.path.join(base_dir, "reimbursement"))

# 4. Onboarding Policy
onboarding_text = """EMPLOYEE ONBOARDING PROCESS CHECKLIST

Phase 1: Pre-boarding (Before Day 1)
- HR: Send offer letter and welcome email.
- HR: Initiate background verification.
- IT: Provision laptop and email account (Google Workspace/Outlook).
- Admin: Create ID card and access badge.
- Manager: Assign a "Buddy".

Phase 2: Day 1
- 10:00 AM: Report to HR for documentation collection.
- 11:00 AM: IT Asset handover (Laptop configuration).
- 12:00 PM: Welcome lunch with the team.
- 02:00 PM: Office tour.
- 03:00 PM: Orientation session (Mission, Vision, Values).

Phase 3: First Week
- Meeting with Reporting Manager (Role expectations, Goal setting).
- Intro to key stakeholders.
- Compliance training (POSH, Data Security, Code of Conduct).
- Access to tools (Jira, Slack, GitHub, HRMS).

Phase 4: First Month
- Regular check-ins with Manager (Weekly).
- Completion of department-specific training.
- 30-day feedback conversation.
"""
create_pdf(onboarding_text, "onboarding_policy_v1.pdf", os.path.join(base_dir, "onboarding"))

# 5. Offboarding Policy
offboarding_text = """EMPLOYEE EXIT AND OFFBOARDING POLICY

1. Resignation
- Must be submitted in writing (email) to Manager and HR.
- Notice period starts from date of resignation email.

2. Notice Period
- Probationers: 15 days.
- Confirmed Employees: 60 days (2 months).
- Shortfall in notice period must be bought out (subject to management approval).
- Leaves during notice period are generally not permitted.

3. Exit Clearance Checklist
- IT: Return Laptop, Charger, Mouse, Data card.
- Admin: Return ID Card, Access keys.
- Finance: Clear travel impress or loans.
- KT: Complete Knowledge Transfer to assigned person and sign-off from Manager.

4. Exit Interview
HR will conduct a confidential exit interview to gather feedback.

5. Full and Final Settlement (FNF)
- Processed within 45 days of last working day.
- Includes unpaid salary, leave encashment (EL only), and bonus (if applicable).
- Relieving Letter and Experience Certificate issued post FNF settlement.
"""
create_pdf(offboarding_text, "exit_policy.pdf", os.path.join(base_dir, "offboarding"))

# 6. Performance Policy
performance_text = """PERFORMANCE APPRAISAL POLICY

1. Purpose
To evaluate contribution, provide feedback, and align goals.

2. Cycle
- Financial Year: April to March.
- Goal Setting: April.
- Mid-Year Review: October.
- Annual Appraisal: March.

3. Process
- Self-Appraisal: Employee submits self-review in PMS.
- Manager Review: Manager provides rating and comments.
- Normalization: Bell curve discussion at department level.
- Discussion: 1:1 meeting to convey rating and increment.

4. Rating Scale
- 5: Outstanding (Far exceeds expectations)
- 4: Exceeds Expectations
- 3: Meets Expectations
- 2: Needs Improvement (PIP potential)
- 1: Unsatisfactory (PIP mandatory)

5. Promotion Guidelines
- Minimum 18 months tenure in current level.
- Rating of 4 or 5 in last appraisal.
- Demonstrated readiness for next level competencies.

6. PIP (Performance Improvement Plan)
- Duration: 3 months.
- Goal: Specific, measurable targets to restore performance.
- Outcome: Improvement or termination.
"""
create_pdf(performance_text, "performance_appraisal_policy.pdf", os.path.join(base_dir, "performance"))

# 7. Code of Conduct
code_text = """CODE OF CONDUCT AND ETHICS POLICY

1. Core Values
Integrity, Respect, Accountability, Compliance.

2. Standards of Conduct
- Ethical Business: No bribery, kickbacks, or fraud.
- Conflict of Interest: Disclose any outside business interests or family in the company. Hiring relatives in direct reporting line is prohibited.
- Side Husltes: Freelancing allowed only affecting work and not for competitors.
- Confidentiality: Do not disclose sensitive company data (trade secrets, client lists).

3. Workplace Behavior
- Respectful Workplace: Zero tolerance for bullying or discrimination.
- Professionalism: Maintain decorum in communication and dressing.
- Social Media: Do not represent personal views as company views.

4. Gifts Policy
- Nominal gifts (diaries, chocolates) < $50 allowed.
- Cash gifts strictly prohibited.
- Report all gifts to HR.

5. Reporting Violations
- Whistleblower policy protects reporters.
- Contact ethics@company.com.
"""
create_pdf(code_text, "code_of_conduct_template.pdf", os.path.join(base_dir, "code_of_conduct"))

# 8. Grievance & POSH
grievance_text = """PREVENTION OF SEXUAL HARASSMENT (POSH) & GRIEVANCE POLICY

1. POSH Policy (Sexual Harassment)
- Scope: Protects all women employees at the workplace.
- Definition: Unwelcome physical contact, sexual overtones, pornography, unwelcome remarks.
- Internal Complaints Committee (ICC): Presiding Officer + 2 Internal Members + 1 NGO Member.
- Complaint Procedure: Submit written complaint to ICC (icc@company.com) within 3 months.
- Inquiry: Completed within 90 days. Confidentiality maintained.
- Redressal: Disciplinary action ranges from warning to termination.

2. General Grievance Redressal
- Level 1: Discuss with immediate Manager.
- Level 2: Escalate to Dept Head if unresolved in 7 days.
- Level 3: Contact HR Head.
- Topics: Salary issues, inter-personal conflict, infrastructure, etc.

3. Safety
- Emergency Response Team (ERT) available on each floor.
- Fire Drills conducted bi-annually.
- Late Night Transport: Cabs provided for female employees leaving after 8 PM effective security guard escort.
"""
create_pdf(grievance_text, "posh_policy.pdf", os.path.join(base_dir, "grievance"))

# ================= NEW CONTENT =================

# 9. Salary & CTC Policy
salary_text = """SALARY STRUCTURE AND COMPENSATION POLICY (CTC)

1. Components of Salary
The Cost to Company (CTC) is divided into Fixed and Variable components.

A. Fixed Pay
- Basic Salary: 40% of Fixed Pay. Fully taxable.
- House Rent Allowance (HRA): 50% of Basic (Metros) / 40% (Non-Metros). Tax exempt subject to rent receipts.
- Special Allowance: Balancing figure. Fully taxable.
- Leave Travel Allowance (LTA): Tax exempt twice in block of 4 years.

B. Statutory Deductions
- Provident Fund (PF): 12% of Basic (Employer + Employee contribution).
- Professional Tax (PT): State-specific (approx INR 200/month).
- Income Tax (TDS): Deducted monthly based on projected annual liability.

c. Retirals
- Gratuity: payable after 5 years of continuous service. Formula: (15/26) * Last Drawn Basic * Years of Service.

2. Payroll Cycle
- Attendance Cut-off: 25th of every month.
- Salary Credit: Last working day of the month.
- Payslips: Available on HRMS on 1st of next month.

3. Reimbursements (Flexible Benefit Plan)
Employees can opt for Food coupons, Fuel, and Driver allowance components to optimize tax.
"""
create_pdf(salary_text, "salary_policy.pdf", os.path.join(base_dir, "salary"))

# 10. Governance & Compliance
compliance_text = """CORPORATE GOVERNANCE AND STATUTORY COMPLIANCE FRAMEWORK

1. Labor Law Compliance
The company strictly adheres to:
- Shops and Establishments Act: Regulating hours of work, leave, and holidays.
- Minimum Wages Act: Adherence to state-notified minimum wages.
- Payment of Bonus Act: Statutory bonus for eligible employees.
- Maternity Benefit Act: 26 weeks paid leave for female employees.

2. Data Privacy (DPDP Act)
- Data Principals (Employees/Clients) have the right to access and correct their personal data.
- Data Fiduciary (Company) ensures secure storage and limited processing of data.
- Consent Manager: Explicit consent obtained before collecting sensitive data (health, biometric).

3. Whistleblower Policy
- Mechanism to report financial irregularities, corruption, or gross misconduct.
- Protected Disclosure: Identity of whistleblower is kept confidential.
- Reports go directly to the Audit Committee Chairman.
"""
create_pdf(compliance_text, "governance_framework.pdf", os.path.join(base_dir, "compliance"))

# 11. Employee Welfare
welfare_text = """EMPLOYEE WELLNESS AND WELFARE BENEFITS

1. Group Health Insurance (GHI)
- Coverage: Employee + Spouse + 2 Children + 2 Parents.
- Sum Insured: INR 5,00,000 Family Floater.
- Room Rent Cap: 1% of Sum Insured.
- Maternity Cover: INR 50,000 for normal / INR 75,000 for C-Section.

2. Group Personal Accident (GPA)
- Coverage: 3x Annual CTC in case of accidental death or permanent disability.
- Term Life Insurance: 2x Annual CTC (Death due to any cause).

3. Office Perks
- Free Meals: Breakfast and Lunch provided in cafeteria.
- Gym: Corporate tie-up with Gold's Gym (50% reimbursement).
- Creche: Facility available for children (6 months to 6 years) at office premises.

4. EAP (Employee Assistance Program)
- 24/7 Counseling Hotline for mental health support.
- Free psychological counseling sessions (up to 6 per year).
"""
create_pdf(welfare_text, "welfare_benefits.pdf", os.path.join(base_dir, "welfare"))

# 12. Women's Welfare & Rights (Consolidated)
women_rights_text = """WOMEN'S WELFARE, RIGHTS, AND MANDATES POLICY

1. Statutory Rights (Government Mandated)
- Maternity Benefit Act, 1961:
  * 26 weeks of paid maternity leave for up to 2 children.
  * 12 weeks for more than 2 children or adopting a child < 3 months.
  * Work From Home: Available after maternity leave period if job nature permits (mutual agreement).
  * Nursing Breaks: 2 breaks/day until child is 15 months old.

- Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013 (POSH):
  * Strictly enforced Zero Tolerance.
  * Internal Complaints Committee (ICC) details: icc@company.com.
  * Anonymity and protection from retaliation guaranteed.

- Equal Remuneration Act, 1976:
  * No discrimination in pay based on gender for same work.

- Factories Act, 1948:
  * Transport: Mandatory cab with security escort for women working between 8 PM and 6 AM.
  * Creche: Mandatory facility near workplace.

2. Company Specific Benefits
- Menstrual Leave: 1 day paid leave/month (Optional/Trust-based).
- Sabbatical: Unpaid career break option for 1 year for childcare/eldercare.
- Mentorship: 'Women in Tech' leadership program.
"""
create_pdf(women_rights_text, "women_welfare_rights.pdf", os.path.join(base_dir, "welfare"))

print("All authentic detailed PDF templates (Handbook, Salary, Compliance, Welfare, Women's Rights etc.) created.")
