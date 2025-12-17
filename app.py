
import streamlit as st
from youtubetranscripter import get_transcript, generate_social_media_content
from youtubetranscripter import extract_video_id

st.set_page_config(
    page_title="Social Media Content Generator",
    layout="centered"
)

st.title(" Social Media Content Generator")
st.caption("Generate platform-specific posts from any YouTube video")

# Inputs
video_id = st.text_input(
    "YouTube Video URL or Video ID",
    placeholder="https://www.youtube.com/watch?v=Zxs7Rf2rWxc"
)

query = st.text_area(
    "What do you want to generate?",
    placeholder="Example: Create a professional LinkedIn post highlighting key takeaways",
    height=120
)

platforms = st.multiselect(
    "Platforms",
    [
        "LinkedIn",
        "Instagram",
        "Twitter/X",
        "Facebook",
        "YouTube Community Post",
        "Reddit",
        "Blog"
    ],
    default=["LinkedIn"]
)

# Caching
@st.cache_data(show_spinner=False)
def cached_transcript(video_id: str):
    return get_transcript(video_id)


# Generate
if st.button(" Generate Content"):
    if not video_id or not query or not platforms:
        st.error("Please fill all fields.")
        st.stop()

        # remove nested spinner (cosmetic)
    with st.spinner("Fetching transcript..."):
        video_id_clean = extract_video_id(video_id)
        if not video_id_clean:
            st.error("❌ Invalid YouTube URL or Video ID.")
            st.stop()

        transcript = cached_transcript(video_id_clean)



    if not transcript:
        st.error("❌ Transcript not available for this video.")
        st.stop()

    st.success("Transcript loaded successfully!")
    st.divider()

    for platform in platforms:
        with st.spinner(f"Generating {platform} content..."):
            result = generate_social_media_content(
                transcript=transcript,
                platform=platform,
                user_query=query
            )

        st.subheader(platform)
        st.write(result)
        st.divider()
