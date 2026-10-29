"""
NEURONEXUS BACKEND - FastAPI REST API Server for Vercel
Team: Infinite Loopers (Sathyabama Institute of Science and Technology)
Theme: Open Innovation | Team ID: DEX26031

Provides production-grade REST endpoints with automatic OpenAPI (/docs),
CORS handling, NeuroLearn Loop assessment, explainable AI recommendations,
and BioAmp EXG telemetry processing.
"""

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime

# Initialize FastAPI application
# root_path="" ensures docs work correctly behind Vercel's routing
app = FastAPI(
    title="NEURONEXUS Platform API",
    description="Educational intelligence platform connecting verified academic performance, topic mastery, explainable AI recommendations, and contextual EEG analytics.",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    redirect_slashes=False,
)

# Enable CORS for SPA frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------------------------------------------------
# PYDANTIC SCHEMAS
# -----------------------------------------------------------------------------

class SubtopicAccuracy(BaseModel):
    correct: int
    total: int
    accuracy: float

class LearningGap(BaseModel):
    subtopic: str
    accuracy: float
    correct: int
    total: int
    severity: str
    reason: str

class RevisionStep(BaseModel):
    id: str
    step_number: int
    title: str
    description: str
    target_action: str
    subtopic: Optional[str] = None
    topic_id: str
    reason: str

class QuizSubmission(BaseModel):
    user_id: str = "usr_student_01"
    course_id: str = "crs_dsa_101"
    topic_id: str = "top_trees"
    is_follow_up: bool = False
    answers: Dict[str, int]
    time_taken_seconds: int = 120

class QuizAttemptResult(BaseModel):
    id: str
    user_id: str
    course_id: str
    topic_id: str
    is_follow_up: bool
    timestamp: datetime
    time_taken_seconds: int
    score: int
    total: int
    percentage: float
    subtopic_breakdown: Dict[str, SubtopicAccuracy]
    identified_gaps: List[LearningGap]
    recommendations: List[RevisionStep]

# -----------------------------------------------------------------------------
# SEED & MOCK DATA
# -----------------------------------------------------------------------------

COURSES_DATA = [
    {
        "id": "crs_dsa_101",
        "code": "CSE-301",
        "title": "Data Structures & Algorithms",
        "category": "Core Computer Science",
        "badge": "Foundation",
        "instructor": "Dr. K. Ramanathan",
        "duration": "12 Weeks",
        "topics": [
            {"id": "top_trees", "title": "Trees & Binary Search Trees", "subtopics": ["BST Operations", "Tree Traversal", "Tree Balancing"]},
            {"id": "top_graphs", "title": "Graph Traversal & Shortest Paths", "subtopics": ["BFS & DFS", "Shortest Path Algorithms", "Cycle Detection"]},
            {"id": "top_dp", "title": "Dynamic Programming Paradigms", "subtopics": ["Optimal Substructure", "Knapsack Variants"]},
            {"id": "top_hashing", "title": "Hash Tables & Collision Resolution", "subtopics": ["Chaining vs Probing", "Bloom Filters"]}
        ]
    },
    {
        "id": "crs_dbms_102",
        "code": "CSE-304",
        "title": "Database Management Systems",
        "category": "Core Computer Science",
        "badge": "Systems",
        "instructor": "Dr. K. Ramanathan",
        "duration": "10 Weeks",
        "topics": [
            {"id": "top_normalization", "title": "Normalization & BCNF", "subtopics": ["Functional Dependencies", "3NF vs BCNF"]},
            {"id": "top_transactions", "title": "Transactions & ACID", "subtopics": ["Conflict Serializability", "2PL"]}
        ]
    }
]

NEURO_SESSIONS_DATA = [
    {
        "id": "ses_01",
        "topic_title": "Trees & Binary Search Trees",
        "duration_minutes": 30,
        "valid_data_coverage_percent": 93.4,
        "signal_quality_status": "ACCEPTABLE",
        "inferred_focus_indicator": 74.0,
        "note": "Acceptable impedance maintained throughout session."
    },
    {
        "id": "ses_02",
        "topic_title": "Database Normalization",
        "duration_minutes": 20,
        "valid_data_coverage_percent": 41.2,
        "signal_quality_status": "INSUFFICIENT",
        "inferred_focus_indicator": None,
        "note": "Coverage 41.2% < 70% threshold. Focus estimate transparently withheld."
    }
]

COMMUNITY_QA_DATA = [
    {
        "id": "q_01",
        "title": "How does the grading curve work for CSE-301?",
        "category": "Academics",
        "course_id": "crs_dsa_101",
        "author_name": "Aarav Sharma",
        "author_role": "Student",
        "author_avatar": "AS",
        "timestamp": "2026-10-28T14:30:00Z",
        "votes": 18,
        "views": 142,
        "tags": ["dsa", "grading"],
        "content": "Are midterm exams normalized against class median or absolute percentages?",
        "answers": [
            {
                "id": "ans_01",
                "author_name": "Dr. K. Ramanathan",
                "author_role": "Faculty",
                "author_avatar": "KR",
                "verified": True,
                "timestamp": "2026-10-28T16:00:00Z",
                "votes": 12,
                "content": "Curving ensures fair letter grade distributions. Practice quizzes and active participation are heavily rewarded."
            }
        ]
    }
]

# -----------------------------------------------------------------------------
# HELPER: health response
# -----------------------------------------------------------------------------

def _health_response():
    return {
        "status": "online",
        "service": "NEURONEXUS FastAPI Backend",
        "team": "Infinite Loopers",
        "institution": "Sathyabama Institute of Science and Technology",
        "framework": "FastAPI",
        "eeg_bridge": "BioAmp EXG Pill (v1.0b) + ESP32 Bridge",
        "timestamp": datetime.utcnow().isoformat()
    }

# -----------------------------------------------------------------------------
# REST ENDPOINTS — registered with BOTH /api/... and bare /... paths
# so the handler works whether Vercel passes the full path or strips the prefix
# -----------------------------------------------------------------------------

@app.get("/", tags=["System"])
@app.get("/api", tags=["System"])
@app.get("/api/", tags=["System"])
@app.get("/health", tags=["System"])
@app.get("/api/health", tags=["System"])
def health_check():
    """Health check endpoint confirming FastAPI backend server availability."""
    return _health_response()


@app.get("/courses", tags=["Courses"])
@app.get("/api/courses", tags=["Courses"])
def get_courses():
    """Returns the list of structured academic courses and topics."""
    return COURSES_DATA


@app.get("/courses/{course_id}", tags=["Courses"])
@app.get("/api/courses/{course_id}", tags=["Courses"])
def get_course_detail(course_id: str):
    """Returns specific course metadata and syllabus topics."""
    for c in COURSES_DATA:
        if c["id"] == course_id or c["code"].lower() == course_id.lower():
            return c
    raise HTTPException(status_code=404, detail="Course not found")


@app.post("/neurolearn/assess", response_model=QuizAttemptResult, tags=["NeuroLearn Loop"])
@app.post("/api/neurolearn/assess", response_model=QuizAttemptResult, tags=["NeuroLearn Loop"])
def assess_and_discover(submission: QuizSubmission):
    """
    Signature NeuroLearn Loop:
    1. Assess: Evaluates answer accuracy per question.
    2. Discover: Discovers granular subtopic knowledge gaps (<70% accuracy threshold).
    3. Personalize: Generates an explainable revision plan with mathematical justifications.
    """
    total_q = max(len(submission.answers), 1)
    correct_count = 0
    subtopic_counts: Dict[str, Dict[str, int]] = {}

    question_subtopics = {
        "q_tree_01": "BST Operations", "q_tree_02": "Tree Traversal",
        "q_tree_03": "Tree Balancing", "q_tree_04": "BST Operations",
        "q_tree_05": "Tree Traversal", "q_tree_06": "Tree Balancing",
        "q_tree_07": "Tree Traversal", "q_tree_08": "BST Operations",
        "q_tree_09": "Tree Balancing", "q_tree_10": "Tree Traversal"
    }

    correct_key = {
        "q_tree_01": 0, "q_tree_02": 2, "q_tree_03": 2, "q_tree_04": 2,
        "q_tree_05": 0, "q_tree_06": 1, "q_tree_07": 0, "q_tree_08": 1,
        "q_tree_09": 1, "q_tree_10": 1
    }

    for qid, chosen in submission.answers.items():
        sub = question_subtopics.get(qid, "General")
        if sub not in subtopic_counts:
            subtopic_counts[sub] = {"correct": 0, "total": 0}
        subtopic_counts[sub]["total"] += 1
        if chosen == correct_key.get(qid, -1):
            correct_count += 1
            subtopic_counts[sub]["correct"] += 1

    breakdown_models: Dict[str, SubtopicAccuracy] = {}
    gaps: List[LearningGap] = []

    for sub, stats in subtopic_counts.items():
        acc = round((stats["correct"] / max(stats["total"], 1)) * 100, 1)
        breakdown_models[sub] = SubtopicAccuracy(
            correct=stats["correct"],
            total=stats["total"],
            accuracy=acc
        )
        if acc < 70.0:
            severity = "HIGH" if acc < 40.0 else "MEDIUM"
            reason = f"Critical knowledge gap: accuracy was {acc}% across {stats['total']} question(s)." if acc < 40.0 else f"Moderate gap: accuracy was {acc}% across {stats['total']} question(s)."
            gaps.append(LearningGap(
                subtopic=sub,
                accuracy=acc,
                correct=stats["correct"],
                total=stats["total"],
                severity=severity,
                reason=reason
            ))

    gaps.sort(key=lambda g: g.accuracy)
    percentage = round((correct_count / total_q) * 100, 1)

    recommendations: List[RevisionStep] = []
    step_num = 1
    if not gaps:
        recommendations.append(RevisionStep(
            id=f"rec_{step_num}",
            step_number=step_num,
            title="Mastery Confirmed: Review Advanced Applications",
            description="All evaluated subtopics met or exceeded the 70% threshold.",
            target_action="OPEN_LESSON",
            topic_id=submission.topic_id,
            reason="Recommended because student achieved comprehensive mastery across all subtopics."
        ))
    else:
        worst = gaps[0]
        recommendations.append(RevisionStep(
            id=f"rec_{step_num}",
            step_number=step_num,
            title=f"Targeted Concept Review: {worst.subtopic}",
            description=f"Review fundamental invariants and illustrative proofs for {worst.subtopic}.",
            target_action="OPEN_LESSON",
            subtopic=worst.subtopic,
            topic_id=submission.topic_id,
            reason=f"Recommended because accuracy in {worst.subtopic} was {worst.accuracy}%, the lowest assessed."
        ))
        step_num += 1
        recommendations.append(RevisionStep(
            id=f"rec_{step_num}",
            step_number=step_num,
            title=f"AI Socratic Practice on {worst.subtopic}",
            description=f"Solve step-by-step diagnostic problems with real-time feedback.",
            target_action="AI_PRACTICE",
            subtopic=worst.subtopic,
            topic_id=submission.topic_id,
            reason=f"Interactive problem solving helps overcome specific error patterns detected in {worst.subtopic}."
        ))
        step_num += 1
        recommendations.append(RevisionStep(
            id=f"rec_{step_num}",
            step_number=step_num,
            title="Follow-Up Improvement Assessment",
            description="Retake the topic evaluation to measure your learning progress delta.",
            target_action="START_RETAKE",
            topic_id=submission.topic_id,
            reason="Required to measure percentage point change against your baseline attempt."
        ))

    return QuizAttemptResult(
        id=f"att_srv_{int(datetime.utcnow().timestamp())}",
        user_id=submission.user_id,
        course_id=submission.course_id,
        topic_id=submission.topic_id,
        is_follow_up=submission.is_follow_up,
        timestamp=datetime.utcnow(),
        time_taken_seconds=submission.time_taken_seconds,
        score=correct_count,
        total=total_q,
        percentage=percentage,
        subtopic_breakdown=breakdown_models,
        identified_gaps=gaps,
        recommendations=recommendations
    )


@app.get("/neuro/sessions", tags=["Neuro Analysis"])
@app.get("/api/neuro/sessions", tags=["Neuro Analysis"])
def get_neuro_sessions(user_id: str = "usr_student_01"):
    """Returns voluntary contextual EEG sessions with signal coverage quality indicators."""
    return NEURO_SESSIONS_DATA


@app.get("/faculty/courses/{course_id}/analytics", tags=["Faculty"])
@app.get("/api/faculty/courses/{course_id}/analytics", tags=["Faculty"])
def get_faculty_analytics(course_id: str):
    """
    Returns aggregated class-level analytics.
    Privacy enforcement: Biometric / EEG signals are excluded from faculty visibility.
    """
    return {
        "course_id": course_id,
        "total_enrolled": 128,
        "class_average_score": 68.5,
        "hardest_subtopics": [
            {"subtopic": "Morris Traversal", "average_accuracy": 34.2, "difficulty": "High"},
            {"subtopic": "AVL RL/LR Double Rotations", "average_accuracy": 48.0, "difficulty": "High"},
            {"subtopic": "BCNF Decomposition", "average_accuracy": 54.1, "difficulty": "Moderate"}
        ],
        "recommended_intervention": "Conduct live interactive recitation on Morris thread pointer mechanics."
    }


@app.get("/community/questions", tags=["Community Q&A"])
@app.get("/api/community/questions", tags=["Community Q&A"])
def get_community_questions():
    """Returns community discussion questions and peer/faculty verified answers."""
    return COMMUNITY_QA_DATA
