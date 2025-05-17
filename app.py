import streamlit as st
import pandas as pd
from datetime import date
import matplotlib.pyplot as plt
import plotly.express as px

# Import local modules
from data.food_database import food_database
from utils.calculator import calculate_nutrients, calculate_points
from utils.visualization import create_nutrition_chart

# Set page config
st.set_page_config(page_title="NutriCalc - Nutrition Calculator",
                   page_icon="🥗",
                   layout="wide")

# Initialize session state variables if not present
if 'selected_foods' not in st.session_state:
    st.session_state.selected_foods = []

if 'daily_log' not in st.session_state:
    st.session_state.daily_log = {}

if 'current_date' not in st.session_state:
    st.session_state.current_date = str(date.today())

# Page title and introduction
st.title("🥗 NutriCalc")
st.subheader("Calculate and track your nutrition intake")

# Create two columns for better layout
col1, col2 = st.columns([2, 3])

with col1:
    st.subheader("Select Foods from List")

    # Category-based food selection
    category_options = [
        "All Foods", "Proteins", "Fats", "Carbs - Fruits", "Carbs - Starchy",
        "Carbs - Vegetables"
    ]
    selected_category = st.selectbox("Filter by category:", category_options)

    # Filter food options based on selected category
    if selected_category == "All Foods":
        food_options = list(food_database.keys())
    elif selected_category == "Proteins":
        food_options = [
            food for food, data in food_database.items()
            if data.get("category") == "protein"
        ]
    elif selected_category == "Fats":
        food_options = [
            food for food, data in food_database.items()
            if data.get("category") == "fats"
        ]
    elif selected_category == "Carbs - Fruits":
        food_options = [
            food for food, data in food_database.items()
            if data.get("category") == "carbs"
            and data.get("subcategory") == "fruit"
        ]
    elif selected_category == "Carbs - Starchy":
        food_options = [
            food for food, data in food_database.items()
            if data.get("category") == "carbs"
            and data.get("subcategory") == "starchy"
        ]
    elif selected_category == "Carbs - Vegetables":
        food_options = [
            food for food, data in food_database.items()
            if data.get("category") == "carbs"
            and data.get("subcategory") == "veggie"
        ]
    else:
        food_options = list(food_database.keys())

    # Sort foods alphabetically
    food_options.sort()

    # Food selection
    selected_food = st.selectbox("Choose a food item:", food_options)

    # Display nutritional information for selected food
    if selected_food:
        #st.write(f"**Nutritional Values per 100g of {selected_food}:**")

        # Show category information
        st.write(
            f"Category: **{food_database[selected_food]['category'].capitalize()}**")




        # Show subcategory if it exists
        if "subcategory" in food_database[selected_food]:
            st.write(
                f"Subcategory: **{food_database[selected_food]['subcategory'].capitalize()}**"
            )

    # Display serving size from database
    serving_size = food_database[selected_food].get("serving_size", "100g")
    unit = food_database[selected_food].get("unit")
    serving_points = food_database[selected_food].get("serving_points", 1)


    st.write(f"**Standard serving: {serving_size} {unit} = {serving_points} point**")


    # Multiplier input
    multiplier = st.number_input("Quantity (multiplier):",
                                 min_value=0.25,
                                 max_value=10.0,
                                 value=1.0,
                                 step=0.25)

    user_serving = round(serving_size * multiplier,2)

    st.write(f"Your Serving: {user_serving} {unit}")

    # Calculate points based on serving size and multiplier
    base_points = food_database[selected_food].get("serving_points", 1)
    food_points = base_points * multiplier

    # Create columns for displaying nutritional info
    n_col1, n_col2, n_col3, n_col4, n_col5 = st.columns(5)

    with n_col1:
        #st.write(f"Protein: **{food_database[selected_food]['protein']}g**"
        st.write(f"Points: **{food_points}**")

    #with n_col2:
    #     st.write(f"Carbs: **{food_database[selected_food]['carbs']}g**")

    #with n_col3:
    #   st.write(f"Fat: **{food_database[selected_food]['fat']}g**")

    #with n_col4:
    #   st.write(f"Calories: **{food_database[selected_food]['calories']}** kcal")

    #with n_col5:
        #st.write(f"Points: **{food_points}**")



    # Add food button
    if st.button("Add Food"):
        # Calculate values based on multiplier and standard serving
        #base_protein = food_database[selected_food]["protein"]
        #base_carbs = food_database[selected_food]["carbs"]
        #base_fat = food_database[selected_food]["fat"]
        #base_calories = food_database[selected_food]["calories"]

        scaled_values = {
            "food": selected_food,
            "serving_size": serving_size,
            "multiplier": multiplier,
           # "protein": base_protein * multiplier,
           # "carbs": base_carbs * multiplier,
           # "fat": base_fat * multiplier,
           # "calories": base_calories * multiplier,
            "category": food_database[selected_food]["category"]
        }

        # Set points based on serving points and multiplier
        points = serving_points * multiplier
        scaled_values["points"] = points

        # Add subcategory if it exists
        if "subcategory" in food_database[selected_food]:
            scaled_values["subcategory"] = food_database[selected_food][
                "subcategory"]

        st.session_state.selected_foods.append(scaled_values)
        st.success(
            f"Added {multiplier} serving(s) of {selected_food} ({points} points)"
        )

    # Link to advanced search
    st.write("[Go to Advanced Food Search Page](/food_search)")

with col2:
    st.subheader("Your Food Selection")

    # Display selected foods in a table
    if st.session_state.selected_foods:
        df = pd.DataFrame(st.session_state.selected_foods)

        # Format the table
        df_display = df.copy()
        #df_display["calories"] = df_display["calories"].round(1)
        #df_display["protein"] = df_display["protein"].round(1)
        #df_display["carbs"] = df_display["carbs"].round(1)
        #df_display["fat"] = df_display["fat"].round(1)

        # Display category information if present
        display_columns = [
            "food", "serving_size", "multiplier", "points"
        ]
        if "category" in df_display.columns:
            display_columns.append("category")

        if "subcategory" in df_display.columns and not df_display[
                "subcategory"].isnull().all():
            display_columns.append("subcategory")

        # Display the table with selected columns
        st.dataframe(df_display[display_columns])

        # Clear selection button
        if st.button("Clear Selection"):
            st.session_state.selected_foods = []
            st.rerun()

        # Calculate and display total nutrients
        totals = calculate_nutrients(st.session_state.selected_foods)

        # Calculate total points
        total_points = calculate_points(totals)

        #st.subheader("Nutritional Summary")

        # Create columns for the nutritional summary
        col_prot, col_carbs, col_fat, col_cal, col_points = st.columns(5)

        #with col_prot:
        #    st.metric("Total Protein", f"{totals['protein']:.1f} g")

        #with col_carbs:
        #    st.metric("Total Carbs", f"{totals['carbs']:.1f} g")

        #with col_fat:
        #    st.metric("Total Fat", f"{totals['fat']:.1f} g")

        #with col_cal:
        #    st.metric("Total Calories", f"{totals['calories']:.1f} kcal")

        #with col_points:
        #    st.metric("Total Points", f"{total_points:.1f}")

        # Add to daily log button
        if st.button("Add to Daily Log"):
            current_date = st.session_state.current_date

            # Initialize the date in daily log if not present
            if current_date not in st.session_state.daily_log:
                st.session_state.daily_log[current_date] = []

            # Add all selected foods to the daily log
            st.session_state.daily_log[current_date].extend(
                st.session_state.selected_foods)

            # Clear the selection
            st.session_state.selected_foods = []
            st.success(f"Added to daily log for {current_date}")
            st.rerun()

        # Empty section to maintain spacing
        st.write("")

    else:
        st.info("No foods selected. Choose foods from the menu on the left.")

# Menu Calculator
st.header("Menu Calculator")

# Initialize meal sections in session state if they don't exist
if 'breakfast' not in st.session_state:
    st.session_state.breakfast = []
if 'lunch' not in st.session_state:
    st.session_state.lunch = []
if 'dinner' not in st.session_state:
    st.session_state.dinner = []
if 'snack1' not in st.session_state:
    st.session_state.snack1 = []
if 'snack2' not in st.session_state:
    st.session_state.snack2 = []

# Create tabs for different meal sections
meal_tab1, meal_tab2, meal_tab3, meal_tab4, meal_tab5, meal_tab6 = st.tabs(
    ["Breakfast", "Lunch", "Dinner", "Snack 1", "Snack 2", "Summary"])

            # Breakfast Section
with meal_tab1:
                st.subheader("Breakfast")

                # Add food selection
                breakfast_col1, breakfast_col2 = st.columns(2)

                with breakfast_col1:
                    food_options = list(food_database.keys())
                    food_options.sort()
                    selected_breakfast_food = st.selectbox("Choose a food:",
                                                           food_options,
                                                           key="breakfast_food")

                    serving_size = food_database[selected_breakfast_food].get("serving_size", 1)
                    serving_unit = food_database[selected_breakfast_food].get("unit", "serving")
                    serving_points = food_database[selected_breakfast_food].get("serving_points", 1)

                    st.write(f"**Standard serving: {serving_size} {serving_unit} = {serving_points} point**")

                    breakfast_multiplier = st.number_input("Quantity (multiplier):",
                                                           min_value=0.5,
                                                           max_value=10.0,
                                                           value=1.0,
                                                           step=0.5,
                                                           key="breakfast_multiplier")
                    user_serving_breakfast = round(serving_size * breakfast_multiplier, 2)
                    user_points_breakfast = round(serving_points * breakfast_multiplier, 2)

                    st.write(f"**Your serving: {user_serving_breakfast} {serving_unit} = {user_points_breakfast} points**")

                    if st.button("Add to Breakfast"):
                        food_entry = {
                            "food": selected_breakfast_food,
                            "serving_size": f"{serving_size} {serving_unit}",
                            "multiplier": breakfast_multiplier,
                            "user_serving": f"{user_serving_breakfast} {serving_unit}",
                            "category": food_database[selected_breakfast_food]["category"],
                            "points": user_points_breakfast
                        }

                        if "subcategory" in food_database[selected_breakfast_food]:
                            food_entry["subcategory"] = food_database[selected_breakfast_food]["subcategory"]

                        st.session_state.breakfast.append(food_entry)
                        st.success(f"Added {breakfast_multiplier} serving(s) of {selected_breakfast_food} to breakfast")
                        st.rerun()

                with breakfast_col2:
                    if st.session_state.breakfast:
                        st.write("**Breakfast items:**")
                        breakfast_df = pd.DataFrame(st.session_state.breakfast)
                        st.dataframe(breakfast_df[["food", "serving_size", "multiplier", "user_serving", "points"]])

                        if st.button("Clear Breakfast"):
                            st.session_state.breakfast = []
                            st.rerun()
                    else:
                        st.info("No breakfast items added yet.")

            # Lunch Section
with meal_tab2:
                st.subheader("Lunch")

                lunch_col1, lunch_col2 = st.columns(2)

                with lunch_col1:
                    food_options = list(food_database.keys())
                    food_options.sort()
                    selected_lunch_food = st.selectbox("Choose a food:", food_options, key="lunch_food")

                    serving_size = food_database[selected_lunch_food].get("serving_size", 1)
                    serving_unit = food_database[selected_lunch_food].get("unit", "serving")
                    serving_points = food_database[selected_lunch_food].get("serving_points", 1)

                    st.write(f"**Standard serving: {serving_size} {serving_unit} = {serving_points} point**")

                    lunch_multiplier = st.number_input("Quantity (multiplier):",
                                                       min_value=0.5,
                                                       max_value=10.0,
                                                       value=1.0,
                                                       step=0.5,
                                                       key="lunch_multiplier")
                    user_serving_lunch = round(serving_size * lunch_multiplier, 2)
                    user_points_lunch = round(serving_points * lunch_multiplier, 2)

                    st.write(f"**Your serving: {user_serving_lunch} {serving_unit} = {user_points_lunch} points**")

                    if st.button("Add to Lunch"):
                        food_entry = {
                            "food": selected_lunch_food,
                            "serving_size": f"{serving_size} {serving_unit}",
                            "multiplier": lunch_multiplier,
                            "user_serving": f"{user_serving_lunch} {serving_unit}",
                            "category": food_database[selected_lunch_food]["category"],
                            "points": user_points_lunch
                        }

                        if "subcategory" in food_database[selected_lunch_food]:
                            food_entry["subcategory"] = food_database[selected_lunch_food]["subcategory"]

                        st.session_state.lunch.append(food_entry)
                        st.success(f"Added {lunch_multiplier} serving(s) of {selected_lunch_food} to lunch")
                        st.rerun()

                with lunch_col2:
                    if st.session_state.lunch:
                        st.write("**Lunch items:**")
                        lunch_df = pd.DataFrame(st.session_state.lunch)
                        st.dataframe(lunch_df[["food", "serving_size", "multiplier", "user_serving", "points"]])

                        if st.button("Clear Lunch"):
                            st.session_state.lunch = []
                            st.rerun()
                    else:
                        st.info("No lunch items added yet.")

            # Dinner Section
with meal_tab3:
                st.subheader("Dinner")

                dinner_col1, dinner_col2 = st.columns(2)

                with dinner_col1:
                    food_options = list(food_database.keys())
                    food_options.sort()
                    selected_dinner_food = st.selectbox("Choose a food:", food_options, key="dinner_food")

                    serving_size = food_database[selected_dinner_food].get("serving_size", 1)
                    serving_unit = food_database[selected_dinner_food].get("unit", "serving")
                    serving_points = food_database[selected_dinner_food].get("serving_points", 1)

                    st.write(f"**Standard serving: {serving_size} {serving_unit} = {serving_points} point**")

                    dinner_multiplier = st.number_input("Quantity (multiplier):",
                                                        min_value=0.5,
                                                        max_value=10.0,
                                                        value=1.0,
                                                        step=0.5,
                                                        key="dinner_multiplier")
                    user_serving_dinner = round(serving_size * dinner_multiplier, 2)
                    user_points_dinner = round(serving_points * dinner_multiplier, 2)

                    st.write(f"**Your serving: {user_serving_dinner} {serving_unit} = {user_points_dinner} points**")

                    if st.button("Add to Dinner"):
                        food_entry = {
                            "food": selected_dinner_food,
                            "serving_size": f"{serving_size} {serving_unit}",
                            "multiplier": dinner_multiplier,
                            "user_serving": f"{user_serving_dinner} {serving_unit}",
                            "category": food_database[selected_dinner_food]["category"],
                            "points": user_points_dinner
                        }

                        if "subcategory" in food_database[selected_dinner_food]:
                            food_entry["subcategory"] = food_database[selected_dinner_food]["subcategory"]

                        st.session_state.dinner.append(food_entry)
                        st.success(f"Added {dinner_multiplier} serving(s) of {selected_dinner_food} to dinner")
                        st.rerun()

                with dinner_col2:
                    if st.session_state.dinner:
                        st.write("**Dinner items:**")
                        dinner_df = pd.DataFrame(st.session_state.dinner)
                        st.dataframe(dinner_df[["food", "serving_size", "multiplier", "user_serving", "points"]])

                        if st.button("Clear Dinner"):
                            st.session_state.dinner = []
                            st.rerun()
                    else:
                        st.info("No dinner items added yet.")
            # Snack 1 Section
with meal_tab4:
                st.subheader("Snack 1")

                snack1_col1, snack1_col2 = st.columns(2)

                with snack1_col1:
                    food_options = list(food_database.keys())
                    food_options.sort()
                    selected_snack1_food = st.selectbox("Choose a food:", food_options, key="snack1_food")

                    serving_size = food_database[selected_snack1_food].get("serving_size", "1 serving")
                    serving_unit = food_database[selected_snack1_food].get("unit", "serving")
                    serving_points = food_database[selected_snack1_food].get("serving_points", 1)

                    st.write(f"**Standard serving: {serving_size} {serving_unit} = {serving_points} point**")

                    snack1_multiplier = st.number_input("Quantity (multiplier):",
                                                        min_value=0.5,
                                                        max_value=10.0,
                                                        value=1.0,
                                                        step=0.5,
                                                        key="snack1_multiplier")
                    user_serving_snack1 = round(serving_size * snack1_multiplier, 2)
                    user_points_snack1 = round(serving_points * snack1_multiplier, 2)

                    st.write(f"**Your serving: {user_serving_snack1} {serving_unit} = {user_points_snack1} points**")

                    if st.button("Add to Snack 1"):
                        food_entry = {
                            "food": selected_snack1_food,
                            "serving_size": f"{serving_size} {serving_unit}",
                            "multiplier": snack1_multiplier,
                            "user_serving": f"{user_serving_snack1} {serving_unit}",
                            "category": food_database[selected_snack1_food]["category"],
                            "points": user_points_snack1
                        }

                        if "subcategory" in food_database[selected_snack1_food]:
                            food_entry["subcategory"] = food_database[selected_snack1_food]["subcategory"]

                        st.session_state.snack1.append(food_entry)
                        st.success(f"Added {snack1_multiplier} serving(s) of {selected_snack1_food} to snack 1")
                        st.rerun()

                with snack1_col2:
                    if st.session_state.snack1:
                        st.write("**Snack 1 items:**")
                        snack1_df = pd.DataFrame(st.session_state.snack1)
                        st.dataframe(snack1_df[["food", "serving_size", "multiplier", "user_serving", "points"]])

                        if st.button("Clear Snack 1"):
                            st.session_state.snack1 = []
                            st.rerun()
                    else:
                        st.info("No snack 1 items added yet.")

            # Snack 2 Section
with meal_tab5:
                st.subheader("Snack 2")

                snack2_col1, snack2_col2 = st.columns(2)

                with snack2_col1:
                    food_options = list(food_database.keys())
                    food_options.sort()
                    selected_snack2_food = st.selectbox("Choose a food:", food_options, key="snack2_food")

                    serving_size = food_database[selected_snack2_food].get("serving_size", "1 serving")
                    serving_unit = food_database[selected_snack2_food].get("unit", "serving")
                    serving_points = food_database[selected_snack2_food].get("serving_points", 1)

                    st.write(f"**Standard serving: {serving_size} {serving_unit} = {serving_points} point**")

                    snack2_multiplier = st.number_input("Quantity (multiplier):",
                                                        min_value=0.5,
                                                        max_value=10.0,
                                                        value=1.0,
                                                        step=0.5,
                                                        key="snack2_multiplier")
                    user_serving_snack2 = round(serving_size * snack2_multiplier, 2)
                    user_points_snack2 = round(serving_points * snack2_multiplier, 2)

                    st.write(f"**Your serving: {user_serving_snack2} {serving_unit} = {user_points_snack2} points**")

                    if st.button("Add to Snack 2"):
                        food_entry = {
                            "food": selected_snack2_food,
                            "serving_size": f"{serving_size} {serving_unit}",
                            "multiplier": snack2_multiplier,
                            "user_serving": f"{user_serving_snack2} {serving_unit}",
                            "category": food_database[selected_snack2_food]["category"],
                            "points": user_points_snack2
                        }

                        if "subcategory" in food_database[selected_snack2_food]:
                            food_entry["subcategory"] = food_database[selected_snack2_food]["subcategory"]

                        st.session_state.snack2.append(food_entry)
                        st.success(f"Added {snack2_multiplier} serving(s) of {selected_snack2_food} to snack 2")
                        st.rerun()

                with snack2_col2:
                    if st.session_state.snack2:
                        st.write("**Snack 2 items:**")
                        snack2_df = pd.DataFrame(st.session_state.snack2)
                        st.dataframe(snack2_df[["food", "serving_size", "multiplier", "user_serving", "points"]])

                        if st.button("Clear Snack 2"):
                            st.session_state.snack2 = []
                            st.rerun()
                    else:
                        st.info("No snack 2 items added yet.")

            

            

# Daily Summary
with meal_tab6:
    st.subheader("Daily Summary")

    all_foods = (
        st.session_state.breakfast +
        st.session_state.lunch +
        st.session_state.dinner +
        st.session_state.snack1 +
        st.session_state.snack2
    )

    if all_foods:
        # Calculate points by category
        category_points = {}
        for item in all_foods:
            cat = item.get("category", "Uncategorized").capitalize()
            pts = item.get("points", 0)
            category_points[cat] = category_points.get(cat, 0) + pts

        total_points = sum(category_points.values())

        st.write("### Daily Points by Category")
        cols = st.columns(len(category_points))
        for i, (cat, pts) in enumerate(category_points.items()):
            cols[i].metric(f"{cat}", f"{pts:.1f} points")

        #st.write("### Total Points")
        #st.metric("All Categories", f"{total_points:.1f} points")

        if st.button("Clear All Meals"):
            st.session_state.breakfast = []
            st.session_state.lunch = []
            st.session_state.dinner = []
            st.session_state.snack1 = []
            st.session_state.snack2 = []
            st.success("Cleared all meal data")
            st.rerun()
    else:
        st.info("No meals added yet. Add foods to your meals to see daily totals.")

# Calculate points for foods not in the list
st.header("Calculate Points for Custom Foods")

# Create two tabs
custom_tab1, custom_tab2 = st.tabs(["Points Calculator", "Meal Suggestions"])

with custom_tab1:
    st.subheader("Calculate Points for a Food Not on the List")

    # Input fields for macronutrients
    custom_protein = st.number_input("Protein (g):",
                                     min_value=0.0,
                                     value=0.0,
                                     step=0.1,
                                     key="custom_protein")
    custom_carbs = st.number_input("Carbs (g):",
                                   min_value=0.0,
                                   value=0.0,
                                   step=0.1,
                                   key="custom_carbs")
    custom_fat = st.number_input("Fat (g):",
                                 min_value=0.0,
                                 value=0.0,
                                 step=0.1,
                                 key="custom_fat")

    # Calculate points for each macronutrient
    protein_points = custom_protein / 7  # 1 point = 7g protein
    carb_points = custom_carbs / 9  # 1 point = 9g carbs
    fat_points = custom_fat / 1.5  # 1 point = 1.5g fat

    total_points = protein_points + carb_points + fat_points

    # Display results
    if st.button("Calculate Points"):
        # Show breakdown of points
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Protein Points", f"{protein_points:.1f}")

        with col2:
            st.metric("Carb Points", f"{carb_points:.1f}")

        with col3:
            st.metric("Fat Points", f"{fat_points:.1f}")

with custom_tab2:
    st.subheader("Meal Planner by Points")

    # Ask for target points
    target_points = st.number_input(
        "How many points should this meal be worth?",
        min_value=1,
        value=4,
        step=1)

    # Define points distribution
    protein_points = target_points  # Equal points for protein
    fat_points = target_points  # Equal points for fat
    carb_points = target_points  # Equal points for carbs

    # Convert points to grams
    protein_grams = protein_points * 7  # 1 point = 7g protein
    fat_grams = fat_points * 1.5  # 1 point = 1.5g fat
    carb_grams = carb_points * 9  # 1 point = 9g carb

    # Display the meal plan
    st.write("### Your Balanced Meal Plan")
    st.write(f"To make a **{target_points} point meal**, you need:")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Protein", f"{protein_grams:.1f}g")
        st.write(f"({protein_points:.1f} points)")

    with col2:
        st.metric("Fat", f"{fat_grams:.1f}g")
        st.write(f"({fat_points:.1f} points)")

    with col3:
        st.metric("Carbs", f"{carb_grams:.1f}g")
        st.write(f"({carb_points:.1f} points)")

    # Initialize session state for random seeds if not present
    if 'protein_seed' not in st.session_state:
        st.session_state.protein_seed = 0
    if 'fat_seed' not in st.session_state:
        st.session_state.fat_seed = 0
    if 'carb_seed' not in st.session_state:
        st.session_state.carb_seed = 0

    # Suggestions section
    st.write("### Suggestions from the Database")

    # Randomize buttons
    randomize_col1, randomize_col2, randomize_col3 = st.columns(3)

    with randomize_col1:
        if st.button("Randomize Protein"):
            st.session_state.protein_seed += 1
            st.rerun()

    with randomize_col2:
        if st.button("Randomize Fat"):
            st.session_state.fat_seed += 1
            st.rerun()

    with randomize_col3:
        if st.button("Randomize Carbs"):
            st.session_state.carb_seed += 1
            st.rerun()

    import random

    # Protein suggestions
    protein_foods = [
        food for food, data in food_database.items()
        if data.get("category") == "protein"
    ]
    if protein_foods:
        st.write("**Protein options:**")

        # Use seed for consistent randomization
        random.seed(st.session_state.protein_seed)
        selected_proteins = random.sample(protein_foods,
                                          min(3, len(protein_foods)))

        for food in selected_proteins:
            st.write(f"- {food}")

    # Fat suggestions
    fat_foods = [
        food for food, data in food_database.items()
        if data.get("category") == "fats"
    ]
    if fat_foods:
        st.write("**Fat options:**")
        fat_suggestions = []

        # Use seed for consistent randomization
        random.seed(st.session_state.fat_seed)
        selected_fats = random.sample(fat_foods, min(3, len(fat_foods)))

        for food in selected_fats:
            fat_per_point = 1.5  # 1 point = 1.5g fat
            st.write(f"- {food}")

        for suggestion in fat_suggestions:
            st.write(suggestion)

    # Carb suggestions with one from each subcategory
    carb_starchy = [
        food for food, data in food_database.items()
        if data.get("category") == "carbs"
        and data.get("subcategory") == "starchy"
    ]
    carb_fruit = [
        food for food, data in food_database.items() if
        data.get("category") == "carbs" and data.get("subcategory") == "fruit"
    ]
    carb_veggie = [
        food for food, data in food_database.items() if
        data.get("category") == "carbs" and data.get("subcategory") == "veggie"
    ]

    st.write("**Carb options:**")
    carb_suggestions = []

    # Use seed for consistent randomization
    random.seed(st.session_state.carb_seed)

    # Select one from each subcategory if available
    if carb_starchy:
        starchy_food = random.choice(carb_starchy)
        carb_per_point = 9  # 1 point = 9g carb
        food_carb_per_100g = food_database[starchy_food]["carbs"]
        quantity_for_points = (carb_points *
                               carb_per_point) / food_carb_per_100g * 100
        st.write(
            f"- **Starchy:** {quantity_for_points:.0f}g of {starchy_food}")

    if carb_fruit:
        fruit_food = random.choice(carb_fruit)
        carb_per_point = 9  #1 point = 9g carb
        food_carb_per_100g = food_database[fruit_food]["carbs"]
        quantity_for_points = (carb_points *
                               carb_per_point) / food_carb_per_100g * 100
        st.write(f"- **Fruit:** {quantity_for_points:.0f}g of {fruit_food}")

    if carb_veggie:
        veggie_food = random.choice(carb_veggie)
        carb_per_point = 9  # 1 point = 9g carb
        food_carb_per_100g = food_database[veggie_food]["carbs"]
        quantity_for_points = (carb_points *
                               carb_per_point) / food_carb_per_100g * 100
        st.write(
            f"- **Vegetable:** {quantity_for_points:.0f}g of {veggie_food}")

# Footer
st.markdown("---")
st.caption(
    "NutriCalc - Your personal nutrition calculator | Made by S. RC for RCF")
