from database import get_db
from models import Task, User, TaskStatus
from datetime import datetime, timedelta

def add_detailed_roadmap():
    db = next(get_db())
    try:
        # Get the user
        user = db.query(User).filter(User.email == "epiphanywanjira@gmail.com").first()
        if not user:
            print("User not found! Please create a user first.")
            return

        # All tasks organized by phase and week
        all_tasks = [
            # Phase 1: March - June 2025
            {
                "title": "AI for Finance - Data Collection & Exploration",
                "description": "Collect, clean, and explore historical wheat, coffee, soybean prices",
                "week_number": 1,
                "phase": "Phase 1",
                "status": TaskStatus.NOT_STARTED,
                "tools_resources": "Pandas, NumPy, Matplotlib, Seaborn, SQL, Yahoo Finance API, Quandl API",
                "notes": "Skills: Time-series analysis, Feature engineering, Data preprocessing\nDatasets: Yahoo Finance API, Quandl Commodity Prices, FAO Market Data"
            },
            {
                "title": "AI for Finance - Model Training & Deployment",
                "description": "Train and deploy a commodity price prediction model",
                "week_number": 2,
                "phase": "Phase 1",
                "status": TaskStatus.NOT_STARTED,
                "tools_resources": "TensorFlow, PyTorch, Scikit-learn, FastAPI, Streamlit",
                "notes": "Skills: LSTM, Transformer models, Hyperparameter tuning\nModels: LSTM, Transformer-based time-series forecasting"
            },
            {
                "title": "AI for Agriculture - Smart Irrigation Project",
                "description": "Build an AI-powered smart irrigation model",
                "week_number": 3,
                "phase": "Phase 1",
                "status": TaskStatus.NOT_STARTED,
                "tools_resources": "Google Earth Engine, OpenCV, Rasterio, NumPy, NASA API, OpenWeather API",
                "notes": "Skills: Remote sensing, Climate data processing, Computer vision\nDatasets: NASA POWER, FAO Climate Database, Sentinel-2 Satellite Imagery"
            },
            {
                "title": "AI for Agriculture - Model Training & Deployment",
                "description": "Train and deploy smart irrigation predictions",
                "week_number": 4,
                "phase": "Phase 1",
                "status": TaskStatus.NOT_STARTED,
                "tools_resources": "Flask API, Docker",
                "notes": "Skills: CNN-LSTM, Geospatial analytics, Model deployment\nModels: CNN-LSTM hybrid for water usage prediction"
            },
            {
                "title": "Generative AI for Finance - LLM-Based Advisor",
                "description": "Train an LLM-based financial advisor",
                "week_number": 5,
                "phase": "Phase 1",
                "status": TaskStatus.NOT_STARTED,
                "tools_resources": "OpenAI API, LangChain, Hugging Face Transformers, SEC Edgar API",
                "notes": "Skills: Large Language Models (LLMs), LangChain, Financial NLP\nDatasets: SEC Filings, Bloomberg Terminal, Edgar API"
            },
            {
                "title": "Finalizing AI Financial Advisor",
                "description": "Deploy the financial advisor chatbot",
                "week_number": 6,
                "phase": "Phase 1",
                "status": TaskStatus.NOT_STARTED,
                "tools_resources": "Pinecone, Streamlit, Hugging Face Spaces",
                "notes": "Skills: Vector search, Chatbot integration, Deployment\nIntegration: Pinecone for storing financial insights"
            },
            {
                "title": "Generative AI for Agribusiness - AI Investment Chatbot",
                "description": "Build an AI-powered agribusiness investment chatbot",
                "week_number": 7,
                "phase": "Phase 1",
                "status": TaskStatus.NOT_STARTED,
                "tools_resources": "ChatGPT API, OpenAI Function Calling, Gradio",
                "notes": "Skills: NLP for finance, Chatbot engineering\nDatasets: FAO Market Reports, USDA Data"
            },
            {
                "title": "Portfolio & Branding Development",
                "description": "Optimize GitHub, LinkedIn, personal website, and publish case studies",
                "week_number": 8,
                "phase": "Phase 1",
                "status": TaskStatus.NOT_STARTED,
                "tools_resources": "GitHub, LinkedIn, Personal Website Platform",
                "notes": "Tasks:\n- Optimize GitHub and LinkedIn\n- Publish 3 case studies\n- Post twice weekly on LinkedIn"
            },
            {
                "title": "Freelance Consulting Setup",
                "description": "Set up freelancing profiles and develop pitch materials",
                "week_number": 9,
                "phase": "Phase 1",
                "status": TaskStatus.NOT_STARTED,
                "tools_resources": "Upwork, Turing, Crossover",
                "notes": "Tasks:\n- Create freelancing profiles\n- Develop pitch deck\n- Identify target companies"
            },
            # Phase 2: June - September 2025
            {
                "title": "Begin Outreach & Networking",
                "description": "Start targeted outreach and networking activities",
                "week_number": 10,
                "phase": "Phase 2",
                "status": TaskStatus.NOT_STARTED,
                "tools_resources": "LinkedIn, Twitter, Email Marketing Tools",
                "notes": "Tasks:\n- Send 10 cold emails weekly\n- Offer free AI analysis reports\n- Join AI & Quant Finance forums"
            },
            {
                "title": "First Client Acquisition",
                "description": "Secure first paying clients and build credibility",
                "week_number": 11,
                "phase": "Phase 2",
                "status": TaskStatus.NOT_STARTED,
                "tools_resources": "Upwork, LinkedIn",
                "notes": "Tasks:\n- Offer free consultation\n- Secure $1,000+ paid gig\n- Write LinkedIn content"
            },
            {
                "title": "High-Paying Role Applications",
                "description": "Apply to top quantitative trading firms",
                "week_number": 12,
                "phase": "Phase 2",
                "status": TaskStatus.NOT_STARTED,
                "tools_resources": "LinkedIn, Company Career Pages",
                "notes": "Apply to: Jane Street, Citadel, Two Sigma, DE Shaw, Renaissance Tech"
            },
            # Phase 3: October - December 2025
            {
                "title": "Research & Publication",
                "description": "Publish research papers and content",
                "week_number": 19,
                "phase": "Phase 3",
                "status": TaskStatus.NOT_STARTED,
                "tools_resources": "Medium, LinkedIn, Research Platforms",
                "notes": "Tasks:\n- Submit research papers\n- Publish weekly insights"
            },
            {
                "title": "Scale Business Operations",
                "description": "Secure larger clients and increase revenue",
                "week_number": 21,
                "phase": "Phase 3",
                "status": TaskStatus.NOT_STARTED,
                "tools_resources": "CRM, Contract Management Tools",
                "notes": "Goals:\n- £10K+/month revenue\n- Long-term contracts (£100K+ annually)"
            },
            {
                "title": "Business Expansion",
                "description": "Invest in growth and team building",
                "week_number": 25,
                "phase": "Phase 3",
                "status": TaskStatus.NOT_STARTED,
                "tools_resources": "HR Tools, Project Management Software",
                "notes": "Tasks:\n- Hire team members\n- Develop 5-year roadmap\n- Invest in branding and PR"
            }
        ]

        # Add tasks to database
        for task_data in all_tasks:
            # Calculate dates based on phase and week number
            if task_data["phase"] == "Phase 1":
                base_date = datetime(2025, 3, 25)
            elif task_data["phase"] == "Phase 2":
                base_date = datetime(2025, 6, 1)
            else:  # Phase 3
                base_date = datetime(2025, 10, 1)

            # Adjust base date by week number
            base_date = base_date + timedelta(weeks=task_data["week_number"]-1)
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
        print("Detailed roadmap tasks added successfully!")

    except Exception as e:
        print(f"Error adding tasks: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_detailed_roadmap() 