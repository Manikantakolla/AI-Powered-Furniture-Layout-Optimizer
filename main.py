import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from PIL import Image, ImageDraw

# Predefined furniture items with default dimensions
FURNITURE_OPTIONS = {
    "Bed": (4, 6),
    "Table": (3, 3),
    "Chair": (2, 2),
    "Sofa": (5, 3),
    "Fridge": (2, 3),
    "TV Stand": (3, 2),
    "Wardrobe": (4, 3),
    "Desk": (3, 2),
    "Bookshelf": (3, 4)
}

# User input for room dimensions and furniture selection
def get_user_inputs():
    uploaded_file = st.file_uploader("Upload a PNG room layout (optional)", type=["png"])
    
    if uploaded_file:
        img = Image.open(uploaded_file)
        room_width, room_height = img.size  # Assume pixels as measurement units
    else:
        room_width = st.number_input("Enter room width:", min_value=5, max_value=50, value=15)
        room_height = st.number_input("Enter room height:", min_value=5, max_value=50, value=15)
    
    furniture_items = []
    
    # First furniture selection
    selected_item = st.selectbox("Select a furniture item:", list(FURNITURE_OPTIONS.keys()))
    default_w, default_h = FURNITURE_OPTIONS[selected_item]
    width = st.number_input(f"Enter width of {selected_item}:", min_value=1, max_value=room_width, value=default_w)
    height = st.number_input(f"Enter height of {selected_item}:", min_value=1, max_value=room_height, value=default_h)
    x = st.number_input(f"Enter X position for {selected_item}:", min_value=0, max_value=room_width - width, value=0)
    y = st.number_input(f"Enter Y position for {selected_item}:", min_value=0, max_value=room_height - height, value=0)
    furniture_items.append((selected_item, width, height, x, y))
    
    # Option to add more items with unique keys
    add_more = True
    count = 1
    while add_more:
        add_more = st.checkbox("Would you like to add another furniture item?", key=f"add_more_{count}")
        if add_more:
            selected_item = st.selectbox(f"Select another furniture item (#{count}):", list(FURNITURE_OPTIONS.keys()), key=f"select_{count}")
            default_w, default_h = FURNITURE_OPTIONS[selected_item]
            width = st.number_input(f"Enter width of {selected_item} (#{count}):", min_value=1, max_value=room_width, value=default_w, key=f"width_{count}")
            height = st.number_input(f"Enter height of {selected_item} (#{count}):", min_value=1, max_value=room_height, value=default_h, key=f"height_{count}")
            x = st.number_input(f"Enter X position for {selected_item} (#{count}):", min_value=0, max_value=room_width - width, value=0, key=f"x_{count}")
            y = st.number_input(f"Enter Y position for {selected_item} (#{count}):", min_value=0, max_value=room_height - height, value=0, key=f"y_{count}")
            furniture_items.append((selected_item, width, height, x, y))
            count += 1
    
    return (room_width, room_height), furniture_items, uploaded_file

# Visualization function with PNG overlay
def plot_layout(room_size, furniture_items, uploaded_file):
    if uploaded_file:
        img = Image.open(uploaded_file)
        draw = ImageDraw.Draw(img)
        for (name, w, h, x, y) in furniture_items:
            draw.rectangle([x, y, x + w, y + h], outline="red", width=3)
            draw.text((x + w / 2, y + h / 2), name, fill="red")
        st.image(img, use_container_width=True)
    else:
        fig, ax = plt.subplots()
        ax.set_xlim(0, room_size[0])
        ax.set_ylim(0, room_size[1])
        for (name, w, h, x, y) in furniture_items:
            rect = plt.Rectangle((x, y), w, h, fill=True, color=np.random.rand(3,))
            ax.add_patch(rect)
            ax.text(x + w / 2, y + h / 2, name, fontsize=8, ha='center', va='center', color='white', fontweight='bold')
        plt.grid(True)
        st.pyplot(fig)

# Streamlit App
def main():
    st.title("AI-Powered Furniture Layout Optimizer")
    room_size, furniture_items, uploaded_file = get_user_inputs()
    plot_layout(room_size, furniture_items, uploaded_file)

if __name__ == "__main__":
    main()