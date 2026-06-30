from graphviz import Digraph

# Create workflow graph
workflow = Digraph(
    "FinRelief_AI_Workflow",
    filename="finrelief_ai_workflow",
    format="png"
)

workflow.attr(rankdir="LR", splines="ortho", nodesep="0.4", ranksep="0.8")
workflow.attr(label="FinRelief AI Project Workflow", fontsize="22", fontname="Helvetica", labelloc="t")

# -------------------------
# Epic 1
# -------------------------
workflow.node(
    "E1",
    """Epic 1
FinRelief AI Application Development
& System Setup""",
    shape="box",
    style="filled",
    fillcolor="lightblue"
)

workflow.node("E1S1", "Story 1\nPython Backend\nEnvironment Setup")
workflow.node("E1S2", "Story 2\nBackend Dependency\nInstallation\n(requirements.txt)")
workflow.node("E1S3", "Story 3\nFrontend Setup\n(React + Vite)")
workflow.node("E1S4", "Story 4\nProject Structure\n& Directory Organization")

workflow.edges([
    ("E1","E1S1"),
    ("E1S1","E1S2"),
    ("E1S2","E1S3"),
    ("E1S3","E1S4")
])

# -------------------------
# Epic 2
# -------------------------
workflow.node(
    "E2",
    """Epic 2
AI Integration &
Financial Processing Setup""",
    shape="box",
    style="filled",
    fillcolor="lightgreen"
)

workflow.node("E2S1","Story 1\nFastAPI Backend\nAPI Endpoints")
workflow.node("E2S2","Story 2\nFinancial Engine\nModule")
workflow.node("E2S3","Story 3\nSettlement Prediction\nSystem")
workflow.node("E2S4","Story 4\nAI Negotiation\nStrategy Engine")
workflow.node("E2S5","Story 5\nFallback Logic\nImplementation")

workflow.edges([
    ("E2","E2S1"),
    ("E2S1","E2S2"),
    ("E2S2","E2S3"),
    ("E2S3","E2S4"),
    ("E2S4","E2S5")
])

# -------------------------
# Epic 3
# -------------------------
workflow.node(
    "E3",
    """Epic 3
Database Management &
Financial Data Storage""",
    shape="box",
    style="filled",
    fillcolor="khaki"
)

workflow.node("E3S1","Story 1\nAPI Development\nFunctionality")
workflow.node("E3S2","Story 2\nLoan & Settlement\nProcessing")
workflow.node("E3S3","Story 3\nData Handling")

workflow.edges([
    ("E3","E3S1"),
    ("E3S1","E3S2"),
    ("E3S2","E3S3")
])

# -------------------------
# Epic 4
# -------------------------
workflow.node(
    "E4",
    """Epic 4
Frontend Integration &
UI Development""",
    shape="box",
    style="filled",
    fillcolor="plum"
)

workflow.node("E4S1","Story 1\nUser Interface\nDevelopment")
workflow.node("E4S2","Story 2\nFrontend\nCommunication\nwith FastAPI")
workflow.node("E4S3","Story 3\nFinancial Metrics\nVisualization")
workflow.node("E4S4","Story 4\nUI Enhancements")

workflow.edges([
    ("E4","E4S1"),
    ("E4S1","E4S2"),
    ("E4S2","E4S3"),
    ("E4S3","E4S4")
])

# -------------------------
# Epic 5
# -------------------------
workflow.node(
    "E5",
    """Epic 5
Testing, Debugging &
Performance Optimization""",
    shape="box",
    style="filled",
    fillcolor="lightsalmon"
)

workflow.node("E5S1","Story 1\nSystem Testing")
workflow.node("E5S2","Story 2\nBackend Error Handling\n& AI Fallback")
workflow.node("E5S3","Story 3\nPerformance Optimization\n& Secure Sessions")

workflow.edges([
    ("E5","E5S1"),
    ("E5S1","E5S2"),
    ("E5S2","E5S3")
])

# -------------------------
# Epic 6
# -------------------------
workflow.node(
    "E6",
    """Epic 6
Version Control &
Deployment Readiness""",
    shape="box",
    style="filled",
    fillcolor="lightcyan"
)

workflow.node("E6S1","Story 1\nGitHub Repository\n& Version Control")
workflow.node("E6S2","Story 2\nProject Cleanup\n& Folder Structure")
workflow.node("E6S3","Story 3\nDeployment\nConfiguration")

workflow.edges([
    ("E6","E6S1"),
    ("E6S1","E6S2"),
    ("E6S2","E6S3")
])

# -------------------------
# Workflow Connections
# -------------------------
workflow.edge("E1S4","E2", color="blue")
workflow.edge("E2S5","E3", color="blue")
workflow.edge("E3S3","E4", color="blue")
workflow.edge("E4S4","E5", color="blue")
workflow.edge("E5S3","E6", color="blue")

# Render Diagram
workflow.render(cleanup=True)

print("FinRelief AI Project Workflow Diagram generated successfully!")