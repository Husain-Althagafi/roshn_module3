"""
Generate additional training samples for daily logs
Uses templates and variation to create realistic construction daily logs
"""

import random
from datetime import datetime, timedelta
import os

# Project names
PROJECTS = [
    "SEDRA Residential",
    "ALAROUS Coastal Development",
    "ALFULWA Eastern Province",
    "MARAFY Canal District"
]

# Locations within projects
LOCATIONS = [
    "Tower A", "Tower B", "Tower C", "Block A", "Block B",
    "Building 1", "Building 2", "Zone North", "Zone South",
    "Level 2", "Level 3", "Level 4", "Basement B1"
]

# Site manager names
MANAGERS = [
    "Ahmed Al-Rashid", "Khalid Rahman", "Faisal Al-Mutairi",
    "Omar Abdulaziz", "Yousef Al-Qahtani", "Hassan Al-Shammari",
    "Mohammed Al-Harbi", "Abdullah Al-Saud", "Salem Al-Otaibi"
]

# Completed tasks templates
TASK_TEMPLATES = [
    "Concrete pour for {location} slab completed - {amount} cubic meters",
    "Installed formwork for {location} columns by {crew} team",
    "Blockwork on {location} finished - {amount} sqm completed",
    "Rebar installation for foundation pads {ref1} through {ref2} completed",
    "Waterproofing membrane applied to {location} wall - {amount} sqm",
    "Steel column erection on {location} - {amount} columns installed",
    "Drywall installation completed in {location} - {amount} sqm",
    "MEP rough-in for {system} finished on {location}",
    "Ceramic tile installation in {location} - {amount} sqm covered",
    "Electrical conduit installation completed for {location}",
    "Paving completed from {ref1} to {ref2} - {amount} linear meters",
    "Plumbing underground pipes laid - {amount} meters",
    "Facade panels installed on {location} - {amount} panels",
    "Landscaping team planted {amount} trees along {location}",
    "Painting completed in {location} apartments - {amount} units",
]

# Blocker templates
BLOCKER_TEMPLATES = [
    "Material delay: {material} scheduled for {day} but delayed until {future_day} due to {cause}",
    "Equipment failure: {equipment} down since {time}. {repair_status}",
    "Waiting on approval from {authority} for {item}. Scheduled {day} but not received yet",
    "Shortage of {material}. Only {percent}% of required quantity available. Affects {work_type} scheduled for next week",
    "{crew} crew delayed - {cause}. Lost {hours} hours of productivity",
    "Weather delay: {weather_condition}. All {work_type} work halted from {time_start} to {time_end}",
    "Coordination issue: {trade1} and {trade2} both need {location}. Scheduling conflict causing delays",
]

# Incident templates
INCIDENT_TEMPLATES = [
    "Safety incident at {time}: {description}. Worker {name} sustained {injury}. {action_taken}",
    "Minor injury reported: Worker {name} - {injury_type} while {activity}. First aid administered, returned to work",
    "Near miss event: {description}. {action_taken}",
    "Quality issue identified: {defect} in {location}. Rework required for approximately {amount} sqm",
    "Environmental incident: {description}. {action_taken}",
]

# Data for randomization
MATERIALS = ["rebar", "concrete", "electrical conduits", "facade panels", "tiles", "steel beams", "drywall sheets", "waterproofing membrane"]
EQUIPMENT = ["Tower crane TC-01", "concrete pump", "excavator EX-300", "scaffold lift", "mixer truck", "piling rig"]
SYSTEMS = ["HVAC ducts", "fire alarm system", "power distribution", "plumbing risers", "data cabling"]
CREWS = ["Al-Bawani", "Almabani", "Saudi Oger", "Bin Laden Group", "Nesma", "Tamimi"]
CAUSES = ["supplier issue", "traffic delays", "customs clearance", "production delays", "coordination issue"]
WEATHER = ["heavy rain (35mm)", "sandstorm with poor visibility", "high winds (45 kph)", "extreme heat (44°C)"]
AUTHORITIES = ["municipality", "civil defense", "building authority", "client engineer"]

def generate_task():
    """Generate a random completed task"""
    template = random.choice(TASK_TEMPLATES)
    return template.format(
        location=random.choice(LOCATIONS),
        amount=random.randint(50, 500),
        crew=random.choice(CREWS),
        ref1=f"P-{random.randint(10,50)}",
        ref2=f"P-{random.randint(51,99)}",
        system=random.choice(SYSTEMS)
    )

def generate_blocker():
    """Generate a random blocker"""
    template = random.choice(BLOCKER_TEMPLATES)
    days = ["Monday", "Tuesday", "Wednesday", "Thursday"]
    return template.format(
        material=random.choice(MATERIALS),
        day=random.choice(days),
        future_day=random.choice(["Friday", "next week", "in 3 days"]),
        cause=random.choice(CAUSES),
        equipment=random.choice(EQUIPMENT),
        time=f"{random.randint(9,15)}:{random.choice(['00','30'])}",
        repair_status=random.choice(["Parts ordered", "Technician on site", "Under repair"]),
        authority=random.choice(AUTHORITIES),
        item=random.choice(["structural inspection", "fire safety approval", "MEP review"]),
        percent=random.randint(30, 60),
        work_type=random.choice(["concrete", "steel", "MEP", "finishing"]),
        crew=random.choice(CREWS),
        hours=random.randint(2, 6),
        weather_condition=random.choice(WEATHER),
        time_start=f"{random.randint(6,10)}am",
        time_end=f"{random.randint(12,16)}pm",
        trade1=random.choice(["electricians", "plumbers", "carpenters"]),
        trade2=random.choice(["painters", "tillers", "HVAC crew"]),
        location=random.choice(LOCATIONS)
    )

def generate_incident():
    """Generate a random incident"""
    template = random.choice(INCIDENT_TEMPLATES)
    injuries = ["minor cut", "bruised arm", "strained back", "minor burn"]
    activities = ["handling materials", "using power tools", "climbing ladder", "moving equipment"]
    names = ["Ahmed Hassan", "Khalid Mahmoud", "Saleh Ali", "Mohammed Rashid"]

    return template.format(
        time=f"{random.randint(9,16)}:{random.choice(['00','15','30','45'])}",
        description=random.choice([
            "worker slipped on wet surface",
            "falling object from upper level",
            "improper lifting technique",
            "equipment malfunction"
        ]),
        name=random.choice(names),
        injury=random.choice(injuries),
        injury_type=random.choice(injuries),
        activity=random.choice(activities),
        action_taken=random.choice([
            "First aid provided, safety briefing conducted",
            "Worker sent to clinic, investigation initiated",
            "Safety protocols reviewed with all crews",
            "Equipment inspected and tagged out"
        ]),
        defect=random.choice([
            "misaligned blockwork",
            "concrete surface finish below standard",
            "improper joint sealing",
            "incorrect installation"
        ]),
        location=random.choice(LOCATIONS),
        amount=random.randint(10, 50)
    )

def generate_daily_log(log_number):
    """Generate one complete daily log"""

    # Random date in October 2025
    base_date = datetime(2025, 10, 22)
    log_date = base_date + timedelta(days=log_number)

    # Determine log complexity (how many items)
    num_tasks = random.randint(2, 5)
    has_blocker = random.random() < 0.4  # 40% chance
    has_incident = random.random() < 0.2  # 20% chance

    log_content = f"""Daily Site Log - {random.choice(PROJECTS)}
Date: {log_date.strftime('%d/%m/%Y')}
Site Manager: {random.choice(MANAGERS)}
Location: {random.choice(LOCATIONS)}

"""

    # Add tasks
    log_content += "Progress Today:\n\n"
    for _ in range(num_tasks):
        log_content += f"- {generate_task()}\n"

    log_content += f"\nWorkers on site: {random.randint(45, 180)}\n"

    # Add blocker if applicable
    if has_blocker:
        log_content += f"\nISSUE REPORTED:\n{generate_blocker()}\n"

    # Add incident if applicable
    if has_incident:
        log_content += f"\nINCIDENT:\n{generate_incident()}\n"

    # Random ending note
    endings = [
        "\nOverall productive day. Weather clear.",
        "\nNo other issues to report. All equipment operational.",
        "\nGood progress maintained. Safety briefing conducted.",
        "\nCrew morale good. Deliveries on schedule.",
        ""
    ]
    log_content += random.choice(endings)

    return log_content

def main():
    """Generate 20 additional daily logs"""

    output_dir = "data/sample_logs"
    os.makedirs(output_dir, exist_ok=True)

    print("Generating 20 additional daily logs...")
    print("=" * 60)

    # Start from log_008 (we already have 001-007)
    for i in range(8, 28):
        log_content = generate_daily_log(i - 8)
        filename = f"{output_dir}/log_{i:03d}.txt"

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(log_content)

        print(f"Created: {filename}")

    print("=" * 60)
    print(f"Successfully generated 20 logs (log_008.txt to log_027.txt)")
    print(f"Total sample logs: 27")
    print(f"\nAll logs saved in: {output_dir}/")

if __name__ == "__main__":
    main()
