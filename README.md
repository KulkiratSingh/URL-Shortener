
# **URL Shortener Application**

This project is a URL Shortening service developed using **Vue.js** for the frontend and **Python (Flask)** for the backend. The app provides a simple interface for users to shorten URLs, manage user accounts, and track link visits. It is secured using **LDAP Active Directory** for authentication.

![image](https://github.com/user-attachments/assets/a29cf3c5-4ff0-425c-b298-f61b35c16ddb)

## **Technology Stack**
- **Frontend**: Vue.js, Bootstrap
- **Backend**: Python (Flask)
- **Database**: MySQL
- **Authentication**: LDAP Active Directory
- **API Documentation**: OpenAPI with Swagger
- **Version Control**: Git


## **Features**

### **1. User Authentication (LDAP)**
Users must log in using their credentials, which are authenticated through **LDAP**. Once logged in, users can manage their links and view their statistics.

![image](https://github.com/user-attachments/assets/e1d7f5ab-2460-4f3c-9ebd-407b8a46c93b)

### **2. URL Shortening**
- Users can submit a long URL, which is then shortened using a randomly generated alias. This shortened link is displayed and can be shared.
- Each user has their own list of shortened links that they can manage.

![image](https://github.com/user-attachments/assets/714fdcd1-c2fa-404f-bc21-64a66f0060a3)

### **3. Link Management**
- Users can **edit** the alias of their shortened links.
- Users can **delete** links they no longer need.
- A **confirmation dialog** ensures that users don’t accidentally delete their links.

![image](https://github.com/user-attachments/assets/aacbb5d9-6bfb-49fe-88fc-7562b7103d83)

### **4. Visit Tracking**
Each time someone clicks on a shortened URL, the app tracks the number of times that URL has been visited.

### **5. User Management**
- Users can delete their account along with all associated data. A confirmation dialog ensures the user does not delete their account by mistake.

## **API Documentation**
This project uses **Swagger** to document the API endpoints.

![image](https://github.com/user-attachments/assets/d4268b50-b92e-4e99-8630-5ab522447b22)


### **Authentication Endpoints**
- **POST /login**: Login and authenticate a user using LDAP credentials.
- **DELETE /delete_user/{userID}**: Delete a user from the system.

### **URL Shortening Endpoints**
- **POST /users/{userID}/link**: Create a new short URL for a user.
- **GET /users/{userID}/links**: Retrieve all URLs for a specific user.
- **PUT /users/{userID}/link/{linkID}**: Update the short URL alias for a user.
- **DELETE /users/{userID}/links/{linkID}**: Delete a specific URL.

### **Visit Tracking**
- **GET /visit/{alias}**: Redirects to the original URL and increments the visit count.

## **Database**
The database stores user information, original URLs, and shortened URLs. **Stored procedures** were written in SQL for efficient data management.

### **Stored Procedures**:
- `checkUserInDb()`: Check to see if the user is already in the database.
- `deleteURL()`: Remove a URL from the table.
- `deleteUser()`: Remove a user from the table.
- `getURLFromAlias()`: Fetches the url with a matching alias from the database.
- `getUserURL()`: Gets the url associated with the user_id and url_id.
- `getUserURLs()`: Gets all the urls associated with the user_id.
- `incrementCounter()`: Increments the counter of the associated url.
- `InsertURLIntoDB()`: Inserts a url into the database.
- `InsertUserIntoDB()`: Inserts a user into the database.
- `readURLID()`: Gets the url_id of the url associated with the alias.
- `readUser()`: Fetch a user’s data from the table.
- `updateShort()`: Updates the alias of the associated url.


