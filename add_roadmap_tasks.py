from database import Session
from models import Task, User, TaskStatus
from datetime import datetime, timedelta

def add_roadmap_tasks():
    db = Session()
    try:
        # Get the user
        user = db.query(User).filter(User.email == "epiphanywanjira@gmail.com").first()
        if not user:
            print("User not found! Please create a user first.")
            return

        # Phase 1 Tasks (March-June 2025)
        phase1_tasks = [
            {
                "title": "Set up AI consulting infrastructure",
                "description": "Establish core infrastructure for AI consulting business including website, documentation templates, and project management tools.",
                "week_number": 1,
                "phase": "Phase 1",
                "status": TaskStatus.NOT_STARTED,
                "tools_resources": "Website builder, project management software, documentation templates",
                "notes": "Focus on professional branding and clear service offerings"
            },
            {
                "title": "Develop Quantitative Finance frameworks",
                "description": "Create frameworks and methodologies for quantitative finance consulting services.",
                "week_number": 2,
                "phase": "Phase 1",
                "status": TaskStatus.NOT_STARTED,
                "tools_resources": "Financial modeling software, research papers, market data sources",
                "notes": "Include risk management and portfolio optimization strategies"
            },
            {
                "title": "Research agricultural AI applications",
                "description": "Conduct comprehensive research on AI applications in agriculture and identify key opportunities.",
                "week_number": 3,
                "phase": "Phase 1",
                "status": TaskStatus.NOT_STARTED,
                "tools_resources": "Academic databases, industry reports, agricultural tech platforms",
                "notes": "Focus on practical applications for local farming communities"
            },
            {
                "title": "Build initial client pipeline",
                "description": "Develop relationships with potential clients and create a sales pipeline.",
                "week_number": 4,
                "phase": "Phase 1",
                "status": TaskStatus.NOT_STARTED,
                "tools_resources": "CRM system, LinkedIn Premium, networking events",
                "notes": "Target mix of industries: finance, agriculture, and technology"
            }
        ]

        # Add tasks to database
        for task_data in phase1_tasks:
            # Set deadline and reminder times
            base_date = datetime(2025, 3, 25) + timedelta(weeks=task_data["week_number"]-1)
            deadline = base_date + timedelta(days=6)  # End of the week
            reminder = deadline - timedelta(days=1)  # One day before deadline

            task = Task(
                title=task_data["title"],
                description=task_data["description"],
                deadline=deadline,
                reminder_time=reminder,
                status=task_data["status"],
                week_number=task_data["week_number"],
                phase=task_data["phase"],
                tools_resources=task_data["tools_resources"],
                notes=task_data["notes"],
                owner_id=user.id
            )
            db.add(task)

        db.commit()
        print("Roadmap tasks added successfully!")

    except Exception as e:
        print(f"Error adding tasks: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_roadmap_tasks() 