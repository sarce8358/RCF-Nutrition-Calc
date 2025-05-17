import streamlit as st
import pandas as pd

# Import local modules
from data.food_database import food_database

def app():
    st.title("🔍 Food Search")
    st.write("Search for foods in our database and see their nutritional information")

    # ---- Category filter buttons ----
    st.markdown("### Filter by Category")
    categories = ["All", "Proteins", "Fats", "Carbs"]
    selected_category = st.radio("Choose a category:", categories, horizontal=True)

    # ---- Search bar with autocomplete ----
    all_foods = list(food_database.keys())
    search_term = st.selectbox("Search for a food:", [""] + all_foods)

    # ---- Normalize category names ----
    category_map = {
        "Proteins": "protein",
        "Fats": "fats",
        "Carbs": "carbs"
    }

    # ---- Filtering logic ----
    filtered_foods = food_database

    # If a category other than "All" is selected, filter by category
    if selected_category != "All":
        category_key = category_map.get(selected_category, None)
        if category_key:
            filtered_foods = {food: data for food, data in filtered_foods.items()
                              if data.get("category", "").lower() == category_key}

    # If a search term is entered, filter by food name
    if search_term:
        filtered_foods = {food: data for food, data in filtered_foods.items()
                          if search_term.lower() in food.lower()}

    # ---- Display results ----
    if filtered_foods:
        st.success(f"Found {len(filtered_foods)} matching food(s)")
        display_data = []
        for food, data in filtered_foods.items():
            row = {
                "Food": food,
                "Serving Size": f"{data.get('serving_size', 1)} {data.get('unit', '')}",
                "Category": data.get("category", "")
                # "Points per Serving": data.get("serving_points", 0),
            }
            if "subcategory" in data:
                row["Subcategory"] = data["subcategory"]
            display_data.append(row)

        df = pd.DataFrame(display_data)

        # Reset index and drop it to remove index column from dataframe display
        df = df.reset_index(drop=True)

        # Display the table without the index column
        st.dataframe(df)

        # ---- Add to selection (commented out) ----
        # st.subheader("Add to your selection")
        # col1, col2 = st.columns(2)

        # with col1:
        #     selected_food = st.selectbox("Choose a food from results:", list(filtered_foods.keys()))
        # with col2:
        #     servings = st.number_input("Number of Servings:", min_value=1.0, value=1.0, step=0.5)

        # if st.button("Add to Selection"):
        #     if 'selected_foods' not in st.session_state:
        #         st.session_state.selected_foods = []

        #     data = food_database[selected_food]
        #     total_points = data.get("serving_points", 0) * servings

        #     food_entry = {
        #         "food": selected_food,
        #         "servings": servings,
        #         "unit": data.get("unit", ""),
        #         "serving_size": data.get("serving_size", 1),
        #         "points": total_points,
        #         "category": data.get("category", "")
        #     }

        #     if "subcategory" in data:
        #         food_entry["subcategory"] = data["subcategory"]

        #     st.session_state.selected_foods.append(food_entry)
        #     st.success(f"Added {servings} serving(s) of {selected_food} for {total_points} points")
    else:
        st.warning("No foods found matching your search or filter")

    # ---- Footer and navigation ----
    st.markdown("---")
    st.caption("Made by S. RC for RCF")

    if st.button("Return to Calculator"):
        st.switch_page("app.py")

# Allow standalone run
if __name__ == "__main__":
    app()
