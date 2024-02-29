# Delivery Management - ClientxWELYNE -

This project is dedicated to optimizing goods delivery using routing algorithms. It provides a solution to optimize delivery routes for multiple missions and tasks.
# 
This project has been custom made for the client. 
Feel free to use it and change it to your needs.
   
## File Description

- `Final_algorithm.py` contains the main function that generates optimized delivery routes.
- `Main_functions.py` contains secondary functions used for optimization calculations and others.
- `TSP_modified.py` contains primary functions used for optimization calculations.
- `API_Call.py` is an essential file for the application's API.

## Running Locally

If you want to run this application locally for testing or development, follow these steps:

1. Make sure you have Python installed on your system. If not, download it from [Python.org](https://www.python.org/downloads/) and install it.

2. Clone this repository to your machine using the following command:

   ```bash
   git clone https://github.com/client-app/welyne-api
   ```

3. Navigate to your project directory:

   ```bash
   cd welyne-api/BaseFunctions
   ```

4. Install required dependencies from the `requirements.txt` file:

   ```bash
   pip install -r requirements.txt
   ```

5. Now, you can run the application using the following command:

   ```bash
   python API_Call.py
   ```

6. If there is a problem in the execution (then retry step 5):

   ```bash
   pip install --upgrade Flask
   ```

   The application should be accessible at [http://localhost:5000](http://localhost:5000). You can access the API using this URL.

Don't forget that you'll also need to obtain API keys if you're using third-party services, like Google Maps, for specific features of the application.

## Testing with Postman
- http://127.0.0.1:5000/api/v1/runsheet-proposal
If you want to test the API locally, you can use tools like Postman to send POST requests to the appropriate endpoints. Examples of mission data are provided in the `missions.js` file.

## Output

The proposed runsheets documentation is in the document 'welyne-api\11-16-2023\openapi_welyne.yaml'

## About the Project

This project aims to provide an efficient solution for goods delivery management by optimizing routes. It uses advanced algorithms to ensure missions are accomplished as efficiently as possible.

**Author**: Youssef Ghaoui
