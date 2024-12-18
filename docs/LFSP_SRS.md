# **Software Requirements Specification (SRS)**  
### **Project Title**: **Local File Sharing Platform (LFSP)**  
---

## **1. Introduction**

### **1.1 Purpose**  
The purpose of this document is to provide a comprehensive **Software Requirements Specification (SRS)** for the development of the **Local File Sharing Platform (LFSP)**. The platform will facilitate file management and sharing in a local network environment. It enables users to create profiles, manage files/folders, and share content publicly or privately. The document serves as a reference for developers, testers, and stakeholders involved in the project.

---

### **1.2 Intended Audience**  
- **Developers**: For understanding system functionalities and technical implementation.  
- **Testers**: To design test cases and validate requirements.  
- **Project Managers**: For planning timelines, milestones, and resource allocation.  
- **Stakeholders**: For an overview of system features and capabilities.

---

### **1.3 Scope**  
LFSP is a **Spring Boot-based web application** that allows users in a **local network** to:  
1. Upload, download, rename, move, and delete files/folders within their profile directory.  
2. Mark files/folders as **public** or **private**.  
3. Stream/download public files shared by others.  
4. Search for other users to access their public content.  
5. Provide role-based access:  
   - **Guest Users**: Read-only access to public files.  
   - **Registered Users**: Full CRUD (Create, Read, Update, Delete) operations on their files.  

The system is designed to handle large files efficiently and provide a user-friendly interface for managing file operations.

---

### **1.4 Definitions, Acronyms, and Abbreviations**  
| **Term**           | **Description**                          |  
|---------------------|------------------------------------------|  
| **CRUD**           | Create, Read, Update, Delete operations. |  
| **LAN**            | Local Area Network.                      |  
| **Public File**     | A file accessible to all users.         |  
| **Private File**    | A file accessible only to its owner.    |  
| **JWT**            | JSON Web Token for authentication.       |  

---

## **2. Overall Description**

### **2.1 Product Perspective**  
LFSP is a standalone application that runs on a local server. It uses:  
- **Spring Boot** as the backend for RESTful APIs.  
- **Database (e.g., SQLite)** for user profiles and file metadata.  
- **File System** to store user files and folders.  
- **React/HTML/CSS/JS** for the frontend UI.  

The system can be accessed through a web browser on the local network.

---

### **2.2 Product Functions**  

#### **Guest Users (ROLE_GUEST)**  
1. **Browse Public Files**:  
   - Search for users and view their public files/folders.  
2. **Stream/Download Public Files**:  
   - Stream supported media files (audio/video).  
   - Download public files.  

#### **Registered Users (ROLE_USER)**  
1. **User Authentication**:  
   - Register and log in securely using credentials.  

2. **File Management in Own Profile**:  
   - **Upload Files**: Upload files to any folder in the user’s directory.  
   - **Create Folders**: Organize files by creating folders.  
   - **Rename Files/Folders**: Modify the name of existing files or folders.  
   - **Move Files/Folders**: Move files or folders within the user's directory.  
   - **Delete Files/Folders**: Delete files or folders.  
   - **Toggle Privacy**: Mark files or folders as **public** or **private**.  

3. **Access Public Files**:  
   - Browse, stream, and download public files of other users.  

4. **Search Other Users**:  
   - Search for users to view their public content.  

---

### **2.3 User Classes and Characteristics**  
| **User Class**     | **Description**                         | **Privileges**                      |  
|--------------------|-----------------------------------------|-------------------------------------|  
| **Guest User**     | Unregistered users (anonymous access).  | Browse, stream, and download public files. |  
| **Registered User**| Authenticated users.                    | Full file management within their profile. |  

---

### **2.4 Operating Environment**  
- **Server**: Localhost or LAN-based server.  
- **Operating System**: Cross-platform (Windows/Linux/Mac).  
- **Browser Compatibility**: Chrome, Firefox, Edge, Safari.  
- **Java Version**: JDK 17+.  
- **Spring Boot Version**: 3.4.0.  
- **Database**: SQLite.  
- **Frontend**: React/HTML/CSS/JS.  

---

### **2.5 Design and Implementation Constraints**  
1. **Local Deployment**: Application operates within a LAN; no external internet access is required.  
2. **Large File Support**: File uploads and downloads must support large files efficiently.  
3. **Storage Directory**: Files are stored on the server file system, organized by user profiles.  
4. **Security**: Use JWT-based authentication for registered users.  
5. **Performance**: Handle multiple simultaneous file uploads and downloads.  

---

### **2.6 Assumptions and Dependencies**  
- Users will access the system through a browser.  
- A reliable LAN connection exists for communication.  
- Server machine has sufficient disk storage for uploaded files.  
- The system will use **Spring Boot**, **React**, and a relational database (SQLite).  

---

## **3. Functional Requirements**

### **3.1 Authentication & Authorization**  
- **FR1**: The system must allow users to register and log in using secure credentials.  
- **FR2**: Guests can browse public files without authentication.  
- **FR3**: The system must issue JWT tokens for authenticated sessions.  

---

### **3.2 File Management for Registered Users**  
- **FR4**: Users must be able to upload files to their root directory or folders.  
- **FR5**: Users must be able to create, rename, move, and delete files/folders.  
- **FR6**: Files uploaded must default to "private" visibility.  
- **FR7**: Users must be able to toggle files or folders between **public** and **private**.  

---

### **3.3 Public File Access**  
- **FR8**: Users can browse public files of other registered users.  
- **FR9**: Guests and registered users can stream and download public files.  

---

### **3.4 Search Functionality**  
- **FR10**: The system must allow users to search for registered users by username.  
- **FR11**: Users can view the public file structure of other users.  

---

### **3.5 File Streaming**  
- **FR12**: Users must be able to stream supported media files (audio/video).  

---

## **4. Non-Functional Requirements**

### **4.1 Performance**  
- **NFR1**: The system must handle multiple concurrent uploads and downloads efficiently.  
- **NFR2**: Large file uploads must be supported without performance degradation.  

### **4.2 Security**  
- **NFR3**: All passwords must be stored in a hashed format.  
- **NFR4**: JWT tokens must secure registered user sessions.  
- **NFR5**: Private files must not be accessible to unauthorized users.  

### **4.3 Usability**  
- **NFR6**: The system must have an intuitive UI for file and folder operations.  
- **NFR7**: The system must be accessible on common browsers (Chrome, Firefox, Edge, Safari).  

---

## **5. System Models**

### **5.1 Use Case Diagram**
The following use cases will be included:  
1. **Guest User**: Browse public files, search users, stream/download files.  
2. **Registered User**: Authenticate, manage files/folders, toggle privacy, access public files.  

---

### **5.2 Class Diagram**  
| **Class**        | **Attributes**                 | **Methods**                            |  
|-------------------|--------------------------------|---------------------------------------|  
| **User**         | id, username, email, password  | register(), login(), searchUsers()     |  
| **File**         | id, name, path, ownerId, isPublic | upload(), delete(), rename(), move()   |  
| **Folder**       | id, name, path, ownerId        | createFolder(), deleteFolder(), move() |  

---

### **6. External Interface Requirements**

#### **6.1 User Interface**  
1. **Login/Register Page**: User authentication.  
2. **Dashboard**: File/folder operations for registered users.  
3. **Public File Page**: Browse and access public content.  

#### **6.2 API Endpoints**  
| **Endpoint**                  | **Method** | **Description**                          |  
|-------------------------------|------------|------------------------------------------|  
| `/api/auth/register`          | POST       | Register a new user.                     |  
| `/api/auth/login`             | POST       | Authenticate a user and issue JWT.       |  
| `/api/files/upload`           | POST       | Upload a file.                           |  
| `/api/files/create-folder`    | POST       | Create a folder.                         |  
| `/api/files/{id}`             | DELETE     | Delete a file or folder.                 |  
| `/api/files/toggle-privacy`   | PUT        | Change file/folder privacy setting.      |  
| `/api/files/public`           | GET        | List all public files.                   |  

---

## **7. Appendices**  
- **Technology Stack**: Spring Boot 3.4.0, SQLite, React, JWT, RESTful APIs.  
- **Tools**: Maven, VS Code, Postman, Git.  

---