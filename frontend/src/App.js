import './App.css';
import { useState } from 'react';
import toast, { Toaster } from 'react-hot-toast';

function App() {
  const [responseData, setResponseData] = useState(null);
  const [file, setFile] = useState(null);

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      toast.success("File selected successfully!");
    }
  };

  const handleFileUpload = async () => {
    if (!file) {
      toast.error("Please choose a file first!");
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('/api/extract', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setResponseData(data);
        toast.success("File uploaded successfully!");
      } else {
        toast.error('Error processing the file.');
      }
    } catch (error) {
      toast.error('Error uploading the file.');
      console.error('Error:', error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>PDF Extract System</h1>

        {/* Toast Notifications */}
        <Toaster />

        {/* File Upload Input */}
        <div className="file-upload-container">
          <label htmlFor="file-upload" className="file-upload-label">
            Choose a file
          </label>
          <input
            type="file"
            id="file-upload"
            className="file-upload-input"
            onChange={handleFileChange}
          />
          {/* Display the selected file name next to the "Choose a file" label */}
          {file && <span className="file-name">{file.name}</span>}
        </div>

        {/* Upload Button positioned just below the "Choose a file" button */}
        <button className="upload-btn" onClick={handleFileUpload}>
          Upload
        </button>

        {/* Display Extracted Data */}
        <div className="info">
          <div className="field">
            <label><strong>Name:</strong></label>
            <span>{responseData?.name || ''}</span>
          </div>
          <div className="field">
            <label><strong>Phone:</strong></label>
            <span>{responseData?.phoneNumber || ''}</span>
          </div>
          <div className="field">
            <label><strong>Email:</strong></label>
            <span>{responseData?.email || ''}</span>
          </div>
        </div>
      </header>
    </div>
  );
}

export default App;
