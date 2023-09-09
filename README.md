# phone_pe_visualization_project

ABOUT PHONEPE:
PhonePe is an Indian digital payments and financial services company headquartered in Bengaluru, Karnataka, India. PhonePe was founded in December 2015, by Sameer Nigam, Rahul Chari, and Burzin Engineer. The PhonePe app, based on the Unified Payments Interface (UPI), went live in August 2016.PhonePe is accepted as a payment option by over 3.5 crore offline and online merchant outlets, constituting 99% of pin codes in the country.

#Problem Statement:
There is a substantial quantity of information on various metrics and statistics in the Phonepe Pulse Github repository.The objective is to extract this data, process it, and then provide a user-friendly visualization of the insights and information that result.The following stages must be included in the solution:
By using scripting, clone and extract data from the Phonepe pulse Github project.
Put the data into the proper format and carry out any required cleaning and pre-processing operations.
Fill a PostgreSQL database with the modified data for effective storage and retrieval.  To present the data in an engaging and aesthetically pleasing way, use Python with Streamlit and Plotly to create a live geo visualisation dashboard.
To display the data in the dashboard, retrieve it from the PostgreSQL database.  Allow users to choose from at least 10 distinct drop-down menus to display various statistics on the dashboard. The solution must be reliable, effective, and simple to use. The dashboard needs to be simple to use and offer insightful facts about the data stored in the Phonepe pulse Github repository.

# Approach:
# 1. Data extraction:
Clone the Github using scripting to fetch the data from the Phonepe pulse Github repository and store it in a suitable format such as CSV or JSON.

# 2. Data transformation:
To alter and preprocess the data, use tools like Pandas and scripting languages like Python. This could entail preparing the data for analysis and visualization, addressing missing numbers, and cleaning the data.

# Database insertion:
Connect to a PostgreSQL database in Python using the "postgreSQL-connector-python" module, then use SQL commands to enter the modified data.

# 4.  Dashboard creation:
Create a dynamic and eye-catching dashboard using Python's Streamlit and Plotly modules. The data may be displayed on a map using Plotly's built-in geo-map features, and Streamlit can be used to provide an intuitive user interface with a variety of drop-down menus for users to choose the facts and statistics to display.

# 5.Data retrieval:
Connect to the PostgreSQL database using the "PostgreSQL-connector-python" module, and then download the data into a Pandas dataframe. Use the information in the dataframe to dynamically refresh the dashboard.

# 6.Deployment:
Ensuring the solution is user-friendly, effective, and secure. Thoroughly test the solution, then make the dashboard available to the public.

# Technologies:
Github Cloning
Python
Pandas
PostgreSQL
PostgreSQL-connector-python
Streamlit
Plotly

# Conclusion:
In order to extract, convert, and analyse data from the Phonepe Pulse GitHub repository, our solution makes use of Python and its robust libraries.
We effectively save and get the altered data from a PostgreSQL database using the "Postgresql-connector-python" package.
We utilise Streamlit and Plotly to create an interactive dashboard that is visually appealing and lets users choose which data points to display.
Finally, we thoroughly test the solution and make the dashboard available to the general public to guarantee that it is reliable, effective, and user-friendly.
Overall, our solution offers insightful and aesthetically pleasing information on the data in the Phonepe Pulse GitHub repository.



   





