import streamlit as st
import random
import time

# ------------------------------
# Initialize session state
# ------------------------------
if "bird_y" not in st.session_state:
    st.session_state.bird_y = 250
    st.session_state.pipe_x = 400
    st.session_state.pipe_gap_y = random.randint(100, 300)
    st.session_state.score = 0
    st.session_state.game_over = False

# ------------------------------
# Reset game
# ------------------------------
def reset_game():
    st.session_state.bird_y = 250
    st.session_state.pipe_x = 400
    st.session_state.pipe_gap_y = random.randint(100, 300)
    st.session_state.score = 0
    st.session_state.game_over = False

# ------------------------------
# Game mechanics
# ------------------------------
def flap():
    if not st.session_state.game_over:
        st.session_state.bird_y -= 40  # jump up

def update_game():
    if st.session_state.game_over:
        return

    # Gravity
    st.session_state.bird_y += 10

    # Move pipe
    st.session_state.pipe_x -= 20
    if st.session_state.pipe_x < -50:
        st.session_state.pipe_x = 400
        st.session_state.pipe_gap_y = random.randint(100, 300)
        st.session_state.score += 1

    # Collision detection
    if st.session_state.bird_y > 480 or st.session_state.bird_y < 0:
        st.session_state.game_over = True
    if (st.session_state.pipe_x < 60 and st.session_state.pipe_x > 20):
        if not (st.session_state.pipe_gap_y < st.session_state.bird_y < st.session_state.pipe_gap_y + 120):
            st.session_state.game_over = True

# ------------------------------
# UI
# ------------------------------
st.title("🐦 Flappy Bird in Streamlit")

col1, col2, col3 = st.columns([1,1,1])
with col2:
    if st.button("Flap"):
        flap()

update_game()

# Draw game area
game_area = f"""
<div style="position:relative;width:400px;height:500px;background:#87CEEB;border:2px solid #000;">
  <!-- Bird -->
  <div style="position:absolute;left:50px;top:{st.session_state.bird_y}px;width:30px;height:30px;background:yellow;border-radius:50%;"></div>
  
  <!-- Pipe Top -->
  <div style="position:absolute;left:{st.session_state.pipe_x}px;top:0;width:50px;height:{st.session_state.pipe_gap_y}px;background:green;"></div>
  
  <!-- Pipe Bottom -->
  <div style="position:absolute;left:{st.session_state.pipe_x}px;top:{st.session_state.pipe_gap_y+120}px;width:50px;height:{500-st.session_state.pipe_gap_y-120}px;background:green;"></div>
</div>
"""
st.markdown(game_area, unsafe_allow_html=True)

st.write(f"Score: {st.session_state.score}")

if st.session_state.game_over:
    st.error("Game Over!")
    if st.button("Restart"):
        reset_game()
