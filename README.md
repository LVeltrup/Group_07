Movie Data Analysis App

Project Overview  
This project is a Streamlit-based data analysis app that processes movie and actor metadata from the CMU MovieSummaries dataset. The dataset is automatically downloaded, extracted, and processed for analysis. The application includes:

- Analysis of the most frequent movie genres.  
- A histogram showing the number of actors per movie.  
- Filtering and visualization of actors based on gender and height.  

Project Structure  

/Group_07/  
│── MovieSummaries/         Directory for dataset storage  
│── src/  
│   ├── movie_data.py       MovieData class for data handling  
│   ├── app.py              Streamlit application  
│   ├── test_movie_data.py  Pytest unit tests  
│── README.md               Project documentation  

Installation  
To run the app, you need Python 3.8+ and the required dependencies.

Install Required Libraries  
Run:  
pip install -r requirements.txt  

If you don’t have a requirements.txt file, install manually:  
pip install pandas matplotlib requests streamlit pydantic pytest  


Running the App  
Start the Streamlit application by running:  
streamlit run app.py  

This will open the web app in your default browser.  


Running Tests  
To validate functionality, run the following in the main project directory:  
pytest -v  

This will test:  
- movie_type(): Ensures correct genre extraction.  
- actor_count(): Checks correct calculation of actor counts.  
- actor_distributions(): Validates filtering logic and error handling.  


Features & Methods  

Movie Genre Analysis  

movie_data.movie_type(N)  

Input:  
- N (int): Number of top genres to display.  

Output:  
A Pandas DataFrame with:  
["Movie_Type", "Count"]  


Actor Count Distribution  

movie_data.actor_count()  

Output:  
A Pandas DataFrame with:  
["Number_of_Actors", "Movie_Count"]  


Actor Filtering by Gender & Height  

movie_data.actor_distributions(gender, max_height, min_height, plot)  

Input:  
- gender (str): "M", "F", or "All"  
- max_height (float): Max height in cm  
- min_height (float): Min height in cm  
- plot (bool): If True, generates a height histogram.  

Output:  
A Pandas DataFrame with:  
["Actor_Name", "Height_cm", "Gender"]  


Troubleshooting  

Dataset Not Found  
If files are missing, run:  
python movie_data.py  

This will re-download and extract the dataset.  

Streamlit App Not Displaying Charts  
Ensure you are using:  
st.pyplot(fig)  
instead of:  
plt.show()  


License  
This project is open-source and available under the MIT License.  


Contributors  
- Leon, Felix, Florian, Martin
- Your Emails  
