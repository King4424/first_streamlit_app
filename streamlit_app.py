import streamlit as st
import pandas as pd
from PIL import Image
import snowflake.connector
from urllib.error import URLError

# Function to list available folders from the external stage location
def get_folder_list():
    # Replace with your Snowflake connection details (ensure secure storage)
    try:
        my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
        with my_cnx.cursor() as my_cur:
            my_cur.execute(
                """
                SELECT DISTINCT SUBSTRING(file_path, 1, INSTR(file_path, '/')) AS folder_name
                FROM @MANGO_LEAF_ML_DB.ML_APP_SCHEMA.MANGO_LEAF_ML_DATASET_STAGE
                """
            )
            folders = [row[0] for row in my_cur.fetchall()]
        return folders
    except Exception as e:
        st.error(f"Error fetching folders: {e}")
        return []

# Function to list image files within a selected folder
def get_image_list(folder_name):
    # Replace with your Snowflake connection details (ensure secure storage)
    try:
        my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
        with my_cnx.cursor() as my_cur:
            my_cur.execute(
                """
                SELECT SUBSTRING(file_path, INSTR(file_path, '/') + 1) AS image_name
                FROM @MANGO_LEAF_ML_DB.ML_APP_SCHEMA.MANGO_LEAF_ML_DATASET_STAGE
                WHERE SUBSTRING(file_path, 1, INSTR(file_path, '/')) = ?
                """,
                (folder_name,),
            )
            images = [row[0] for row in my_cur.fetchall()]
        return images
    except Exception as e:
        st.error(f"Error fetching images: {e}")
        return []

st.title('Image Selection App')

# Get available folders from the external stage location
folder_list = get_folder_list()

if folder_list:
    selected_folder = st.selectbox('Select Folder', folder_list)

    # Get image list for the selected folder (if any)
    image_list = get_image_list(selected_folder) if selected_folder else []

    if image_list:
        selected_image = st.selectbox('Select Image', image_list)

        # Download the selected image (assuming public access for demonstration)
        image_url = f"https://s3.amazonaws.com/your-bucket-name/{selected_folder}/{selected_image}"  # Replace with your actual URL structure
        try:
            response = requests.get(image_url, stream=True)
            if response.status_code == 200:
                image = Image.open(response.raw)
                st.image(image, caption=selected_image, use_column_width=True)
            else:
                st.error(f"Failed to download image: {response.status_code}")
        except URLError as e:
            st.error(f"Error downloading image: {e}")
        except Exception as e:
            st.error(f"Unexpected error: {e}")
    else:
        st.info("No images found in this folder.")
else:
    st.error("Error fetching folders from Snowflake.")
