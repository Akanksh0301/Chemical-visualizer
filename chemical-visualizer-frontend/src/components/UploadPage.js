// UploadPage.js
import React, { useState } from "react";
import { api } from "../api";
import "./UploadPage.css"; // import CSS for styling

export default function UploadPage({ setPage }) {
  const [file, setFile] = useState(null);

  const uploadFile = async () => {
    if (!file) {
      alert("Please select a file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      await api.post("/upload/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      alert("Upload Successful!");
      setPage("history"); // go to history page automatically
    } catch (err) {
      console.error(err);
      alert("Upload Failed!");
    }
  };

  return (
    <div className="upload-card">
      <h2>Upload Chemical Equipment CSV</h2>
      <input
        type="file"
        accept=".csv"
        onChange={(e) => setFile(e.target.files[0])}
      />
      {file && <p>Selected File: {file.name}</p>}
      <button onClick={uploadFile}>Upload</button>
    </div>
  );
}
