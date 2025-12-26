# Day 02: Core Logic - File Uploads, UUIDs & Redis Metadata

## Curriculum Overview
Today's session focuses on implementing the **core file handling logic** of OneTimeShare. We move beyond "Hello World" to actually processing, storing, and tracking files.

### Topics Covered

#### Part 1: Flask File Handling
1.  **Flask File Uploads Deep Dive**: Understanding `request.files`, `FileStorage` objects, and the multipart/form-data encoding.
2.  **Werkzeug Utilities**: The `secure_filename()` function and why we go further with UUIDs.
3.  **File Streams & Binary Data**: How files move from HTTP request to disk.

#### Part 2: Security & Identification
4.  **UUID Generation**: Why randomness matters for security, and the different UUID versions.
5.  **Path Traversal Attacks**: A critical security concept and how we prevent them.

#### Part 3: Data Persistence
6.  **Redis Data Structures**: Deep dive into Redis Hashes for storing structured metadata.
7.  **Designing a Data Schema**: How to organize file metadata in Redis.

#### Part 4: Robustness
8.  **File Validation**: Size limits, type checking, and defensive programming.
9.  **Configuration Management**: Using environment variables and Flask config patterns.

## How to use these notes
Read the files in numerical order. Each file builds upon the concepts of the previous one.
- **Theory sections** explain the "why" – read these first!
- **Code examples** show the "how" – type these out yourself, don't copy-paste!
- **Practice exercises** at the end of each file help you internalize the concepts.
