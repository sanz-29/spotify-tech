# Problem Statement

## 1. Title

**Music Streaming Platform with Playlist & AI-Based Music Discovery**

---

## 2. Domain

**Entertainment Technology (Music Streaming), Artificial Intelligence, Cybersecurity, and Cloud Computing**

---

## 3. Who is the User?

### 1. Listener (User)
**Role:**
- Register and log in to the platform.
- Search and stream songs.
- Create, edit, and manage playlists.
- Receive AI-powered music recommendations.
- View listening history and favorite songs.

### 2. Artist
**Role:**
- Upload songs and albums.
- Manage uploaded content.
- Update song details.
- View song statistics and listener analytics.

### 3. Administrator
**Role:**
- Manage users and artists.
- Approve or remove uploaded songs.
- Monitor platform activities.
- Generate reports.
- Ensure platform security and performance.

---

## 4. What Problem Are We Solving?

Many music streaming platforms offer limited personalization and playlist management for users. Independent artists also face challenges in uploading and managing their music efficiently. Additionally, protecting user accounts and streaming services from unauthorized access is an important concern.

For example, a user who enjoys Tamil melodies and English pop music often spends a significant amount of time searching for suitable songs manually. This project solves the problem by providing AI-based music recommendations, secure streaming, playlist management, and artist content management within a single platform.

---

## 5. Proposed Solution

The proposed system is a web-based music streaming platform that allows users to discover, stream, and organize music efficiently.

### Features
- User registration and secure login
- Music search by title, artist, album, or genre
- Online music streaming
- Playlist creation and management
- Listening history tracking
- Favorite songs collection
- AI-powered music recommendations
- Artist dashboard for uploading and managing songs
- Admin dashboard for monitoring users and content
- JWT-based authentication
- Cloud-ready deployment architecture

---

## 6. Core Entities / Database Tables

1. Users
2. Artists
3. Songs
4. Albums
5. Playlists
6. PlaylistSongs
7. ListeningHistory
8. Favorites
9. Genres
10. Recommendations
11. UserSessions
12. AdminLogs

---

## 7. User Roles & Permissions

### Admin
- Manage users and artists
- Approve or remove songs
- Manage albums and genres
- View reports and analytics
- Monitor platform security

### Listener (User)
- Register and log in
- Search and stream songs
- Create and manage playlists
- Add songs to favorites
- View listening history
- Receive AI recommendations

### Artist
- Upload songs and albums
- Edit uploaded content
- Delete own songs
- View song analytics
- Manage artist profile

---

## 8. Success Criteria

The project will be considered successful if:

- A new user can register and log in within **1 minute**.
- Users can search and play a song in **less than 5 seconds**.
- Playlist creation can be completed in **under 1 minute**.
- AI recommendations accurately suggest songs based on listening history.
- Artists can successfully upload and manage songs.
- User data is protected through secure authentication and authorization.

---

## 9. Out of Scope

The following features are **not included** in this project:

- Music licensing and royalty payment system
- Live audio streaming or concerts
- Video streaming
- Chat or messaging features
- Offline music downloads
- Advanced DRM (Digital Rights Management)
- Mobile applications (Android/iOS)
- Subscription payment gateway integration

---

## 10. Chosen Track

**Python – FastAPI**

### Reason

FastAPI is a modern, high-performance Python framework that provides excellent support for REST APIs, JWT authentication, asynchronous programming, automatic API documentation, and AI integration. It is well-suited for developing a secure, scalable, and cloud-ready music streaming platform.