"""
NEURONEXUS Vercel Serverless Function (Zero Third-Party Dependencies)
Compatible with all Python versions (including 3.12, 3.13, 3.14) on Vercel.
Handles health checks, courses, assessments, neuro analytics, and faculty insights.
"""

from http.server import BaseHTTPRequestHandler
import json
import urllib.parse
from datetime import datetime

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


class handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Disable default stderr logging in serverless environment
        pass

    def send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    def send_json(self, data, status_code=200):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_cors_headers()
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_cors_headers()
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.rstrip("/")

        if path in ("/api", "/api/health"):
            return self.send_json({
                "status": "online",
                "service": "NEURONEXUS Platform API",
                "team": "Infinite Loopers",
                "institution": "Sathyabama Institute of Science and Technology",
                "runtime": "Vercel Serverless (Zero-Dependency)",
                "timestamp": datetime.utcnow().isoformat()
            })

        if path == "/api/courses":
            return self.send_json(COURSES_DATA)

        if path == "/api/neuro/sessions":
            return self.send_json(NEURO_SESSIONS_DATA)

        if path.startswith("/api/faculty/courses/") and path.endswith("/analytics"):
            course_id = path.split("/")[4]
            return self.send_json({
                "course_id": course_id,
                "total_enrolled": 128,
                "class_average_score": 68.5,
                "hardest_subtopics": [
                    {"subtopic": "Morris Traversal", "average_accuracy": 34.2, "difficulty": "High"},
                    {"subtopic": "AVL RL/LR Double Rotations", "average_accuracy": 48.0, "difficulty": "High"},
                    {"subtopic": "BCNF Decomposition", "average_accuracy": 54.1, "difficulty": "Moderate"}
                ],
                "recommended_intervention": "Conduct live interactive recitation on Morris thread pointer mechanics."
            })

        # Fallback for unrecognized GET endpoints
        return self.send_json({"error": "Endpoint not found", "path": path}, status_code=404)

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.rstrip("/")

        content_length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
        try:
            payload = json.loads(raw_body)
        except Exception:
            payload = {}

        if path == "/api/neurolearn/assess":
            answers = payload.get("answers", {})
            total_q = max(len(answers), 1)
            correct_key = {
                "q_tree_01": 0, "q_tree_02": 2, "q_tree_03": 2, "q_tree_04": 2,
                "q_tree_05": 0, "q_tree_06": 1, "q_tree_07": 0, "q_tree_08": 1,
                "q_tree_09": 1, "q_tree_10": 1
            }
            question_subtopics = {
                "q_tree_01": "BST Operations", "q_tree_02": "Tree Traversal",
                "q_tree_03": "Tree Balancing", "q_tree_04": "BST Operations",
                "q_tree_05": "Tree Traversal", "q_tree_06": "Tree Balancing",
                "q_tree_07": "Tree Traversal", "q_tree_08": "BST Operations",
                "q_tree_09": "Tree Balancing", "q_tree_10": "Tree Traversal"
            }
            correct_count = 0
            subtopic_counts = {}
            for qid, chosen in answers.items():
                sub = question_subtopics.get(qid, "General")
                if sub not in subtopic_counts:
                    subtopic_counts[sub] = {"correct": 0, "total": 0}
                subtopic_counts[sub]["total"] += 1
                if chosen == correct_key.get(qid, -1):
                    correct_count += 1
                    subtopic_counts[sub]["correct"] += 1

            subtopic_breakdown = {}
            gaps = []
            for sub, stats in subtopic_counts.items():
                acc = round((stats["correct"] / max(stats["total"], 1)) * 100, 1)
                subtopic_breakdown[sub] = {
                    "correct": stats["correct"],
                    "total": stats["total"],
                    "accuracy": acc
                }
                if acc < 70.0:
                    gaps.append({
                        "subtopic": sub,
                        "accuracy": acc,
                        "correct": stats["correct"],
                        "total": stats["total"],
                        "severity": "HIGH" if acc < 40.0 else "MEDIUM",
                        "reason": f"Accuracy was {acc}% across {stats['total']} assessed question(s)."
                    })

            percentage = round((correct_count / total_q) * 100, 1)
            recs = [
                {
                    "id": "rec_1",
                    "step_number": 1,
                    "title": "Targeted Concept Review",
                    "description": "Review foundational notes and key diagrams for identified gaps.",
                    "target_action": "OPEN_LESSON",
                    "reason": "Recommended to address lowest accuracy topics."
                },
                {
                    "id": "rec_2",
                    "step_number": 2,
                    "title": "Interactive Practice Drill",
                    "description": "Solve diagnostic problems with immediate feedback.",
                    "target_action": "AI_PRACTICE",
                    "reason": "Strengthen conceptual retention through active recall."
                }
            ]

            return self.send_json({
                "id": f"att_{int(datetime.utcnow().timestamp())}",
                "user_id": payload.get("user_id", "usr_student_01"),
                "course_id": payload.get("course_id", "crs_dsa_101"),
                "topic_id": payload.get("topic_id", "top_trees"),
                "score": correct_count,
                "total": total_q,
                "percentage": percentage,
                "subtopic_breakdown": subtopic_breakdown,
                "identified_gaps": gaps,
                "recommendations": recs
            })

        return self.send_json({"error": "Endpoint not found", "path": path}, status_code=404)
