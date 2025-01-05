# Certificate Validation Using Blockchain

## **Overview**
This project leverages blockchain technology to provide a secure and efficient solution for validating academic certificates. The system ensures the authenticity and integrity of certificates by integrating cryptographic hashing, a tamper-proof ledger, and a web-based interface. It prevents forgery and provides an automated method for certificate verification.

---

## **Features**
- **Blockchain Integration**: Securely stores certificate data on a blockchain ledger.
- **File Hashing**: Generates unique identifiers for certificates using the SHA-256 hashing algorithm.
- **Admin Upload**: Enables authorized users to upload and store certificates with metadata.
- **Certificate Verification**: Validates the authenticity of certificates by comparing file hashes against blockchain records.

---

## **Technologies Used**
- **Programming Language**: Python
- **Framework**: Flask (for web application development)
- **Cryptographic Algorithm**: SHA-256 for file hashing
- **Blockchain**: Custom implementation with JSON-based data storage

---

## **Project Workflow**

### **Certificate Upload**
- Admin uploads the certificate file and metadata (e.g., student name and roll number).
- The system generates a SHA-256 hash of the file and creates a blockchain block with the file hash and metadata.

### **Blockchain Storage**
- The block is added to the blockchain, ensuring immutability and secure storage.
- The blockchain is saved to a JSON file for persistence.

### **Verification Process**
- Users can upload a certificate file for verification.
- The system generates a hash of the uploaded file and compares it with the hashes stored in the blockchain.
- The certificate is deemed valid if a match is found; otherwise, it is marked as fake.

