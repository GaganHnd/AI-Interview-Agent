import streamlit as st
from agents.question_generator import generate_questions
from agents.evaluator import evaluate_answer
from agents.summary import generate_summary
from utils.pdf_report import generate_pdf

st.set_page_config(
    page_title="AI Interview Agent",
    page_icon="🤖",
    layout="wide"
)

# -----------------------
# Session State
# -----------------------

defaults = {
    "questions": [],
    "answers": [],
    "evaluations": [],
    "current_question": 0,
    "interview_started": False,
    "candidate_name": "",
    "job_role": "",
    "total_score": 0,
    "submitted": False
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# -----------------------
# Header
# -----------------------

st.title("🤖 AI Interview Agent")

st.markdown("""
### 🚀 Features

- 🤖 AI-generated technical interview questions
- 🧠 LLM-based answer evaluation
- 📊 Question-wise scoring
- 💡 Personalized feedback
- 📄 PDF interview report
- 📁 JSON report export
- 🎯 Hiring recommendation
""")
st.caption("Rooman Technologies AI Challenge")

st.divider()

# -----------------------
# Candidate Form
# -----------------------

if not st.session_state.interview_started:

    name = st.text_input(
        "Candidate Name"
    )

    role = st.text_input(
        "Job Role",
        placeholder="Example: AI Research Associate"
    )

    if st.button("🚀 Start Interview"):

        if name == "" or role == "":

            st.warning("Fill all fields.")

        else:

            with st.spinner("Generating Questions..."):

                questions = generate_questions(role)

            st.session_state.questions = questions
            st.session_state.candidate_name = name
            st.session_state.job_role = role
            st.session_state.interview_started = True
            st.rerun()

# -----------------------
# Interview
# -----------------------

if st.session_state.interview_started:

    total = len(st.session_state.questions)
    current = st.session_state.current_question

    st.progress((current + 1) / total)

    st.write(
        f"### Question {current+1} of {total}"
    )

    question = st.session_state.questions[current]

    st.info(question)

    answer = st.text_area(
        "Your Answer",
        height=220,
        key=f"answer_{current}"
    )

    # -----------------------
    # Submit
    # -----------------------

    if not st.session_state.submitted:

        if st.button("Submit Answer"):

            if answer.strip() == "":

                st.warning("Please answer the question.")

            else:

                with st.spinner("AI Evaluating..."):

                    result = evaluate_answer(
                        st.session_state.job_role,
                        question,
                        answer
                    )

                st.session_state.answers.append(answer)
                st.session_state.evaluations.append(result)
                st.session_state.total_score += result["score"]
                st.session_state.submitted = True

                st.rerun()

    # -----------------------
    # Evaluation
    # -----------------------

    if st.session_state.submitted:

        result = st.session_state.evaluations[current]

        st.divider()

        st.subheader("🤖 AI Evaluation")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Score",
                f'{result["score"]}/10'
            )

        with col2:
            st.metric(
                "Overall Score",
                st.session_state.total_score
            )

        st.success("### Strengths")

        for item in result["strengths"]:
            st.write(f"✅ {item}")

        st.error("### Weaknesses")

        for item in result["weaknesses"]:
            st.write(f"❌ {item}")

        st.info(result["feedback"])

        with st.expander("Expected Answer"):

            st.write(result["expected_answer"])

        # -----------------------
        # Next Question
        # -----------------------

        if current < total - 1:

            if st.button("Next Question ➜"):

                st.session_state.current_question += 1
                st.session_state.submitted = False

                st.rerun()

        else:

            import json

            st.balloons()

            st.divider()

            st.header("📄 Interview Report")

            average = st.session_state.total_score / total

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Final Score",
                    f"{st.session_state.total_score}/50"
                )

            with col2:
                st.metric(
                    "Average",
                    f"{average:.1f}/10"
                )

            with col3:

                if average >= 8:
                    recommendation = "🟢 Strong Hire"

                elif average >= 6:
                    recommendation = "🟡 Hire"

                elif average >= 4:
                    recommendation = "🟠 Borderline"

                else:
                    recommendation = "🔴 Reject"

                st.metric(
                    "Recommendation",
                    recommendation
                )

            st.divider()

            st.subheader("Question-wise Evaluation")

            for i, item in enumerate(st.session_state.evaluations):

                with st.expander(f"Question {i+1} • {item['score']}/10"):

                    st.write("### ✅ Strengths")

                    for strength in item["strengths"]:
                        st.success(strength)

                    st.write("### ❌ Weaknesses")

                    for weakness in item["weaknesses"]:
                        st.error(weakness)

                    st.write("### 💬 Feedback")
                    st.info(item["feedback"])

                    st.write("### 📚 Expected Answer")
                    st.write(item["expected_answer"])

            st.download_button(
                "⬇ Download JSON Report",
                data=json.dumps(
                    st.session_state.evaluations,
                    indent=4
                ),
                file_name="Interview_Report.json",
                mime="application/json"
            )
            pdf_file = generate_pdf(
                st.session_state.candidate_name,
                st.session_state.job_role,
                st.session_state.total_score,
                average,
                recommendation,
                st.session_state.evaluations
            )

            with open(pdf_file, "rb") as pdf:

                st.download_button(
                    "📄 Download PDF Report",
                    pdf,
                    file_name="Interview_Report.pdf",
                    mime="application/pdf"
                )