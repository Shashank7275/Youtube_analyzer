
import streamlit as st

from youtube_analyzer import youtube_agent 

# --------------------------------------------------------------------------
# Page config
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="YouTube Video Analyzer",
    page_icon="🎬",
    layout="wide",
)

st.title("🎬 YouTube Video Analyzer")
st.caption("Powered by Agno + Gemini — paste a YouTube link and get a full breakdown.")

# --------------------------------------------------------------------------
# Session state
# --------------------------------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []  # list of (url, response_text)

# --------------------------------------------------------------------------
# Sidebar
# --------------------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Settings")
    st.write("This UI streams the response from `youtube_agent`.")
    if st.button("🗑️ Clear history"):
        st.session_state.history = []
        st.rerun()

    st.divider()
    st.subheader("📜 History")
    if st.session_state.history:
        for i, (url, _) in enumerate(reversed(st.session_state.history), 1):
            st.write(f"{i}. {url}")
    else:
        st.write("No videos analyzed yet.")

# --------------------------------------------------------------------------
# Main input
# --------------------------------------------------------------------------
with st.form(key="analyze_form"):
    video_url = st.text_input(
        "YouTube Video URL",
        placeholder="https://youtu.be/JkaxUblCGz0?si=KP4WAOjeKfzDG7PN",
    )
    submitted = st.form_submit_button("🔍 Analyze Video", use_container_width=True)

# --------------------------------------------------------------------------
# Run analysis
# --------------------------------------------------------------------------
if submitted:
    if not video_url.strip():
        st.warning("Please paste a valid YouTube URL first.")
    else:
        st.subheader("📊 Analysis Result")
        response_placeholder = st.empty()
        full_response = ""

        try:
            with st.spinner("Analyzing video... this may take a moment ⏳"):
                # Stream the agent's response into the UI
                run_stream = youtube_agent.run(
                    f"Analyze this YouTube video: {video_url.strip()}",
                    stream=True,
                )

                for chunk in run_stream:
                    # Agno RunResponse chunks expose `.content` with the delta text
                    content = getattr(chunk, "content", None)
                    if content:
                        full_response += content
                        response_placeholder.markdown(full_response)

            if not full_response:
                st.error("No response received from the agent.")
            else:
                st.session_state.history.append((video_url.strip(), full_response))
                st.success("Analysis complete ✅")

        except Exception as e:
            st.error(f"Something went wrong while analyzing the video: {e}")

# --------------------------------------------------------------------------
# Show previous results (most recent first)
# --------------------------------------------------------------------------
if st.session_state.history and not submitted:
    st.subheader("🕘 Previous Analyses")
    for url, text in reversed(st.session_state.history):
        with st.expander(f"🔗 {url}"):
            st.markdown(text)