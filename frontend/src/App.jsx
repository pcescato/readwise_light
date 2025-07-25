import { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [documents, setDocuments] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);

  useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {
    const response = await axios.get('/api/documents/');
    setDocuments(response.data);
  };

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append('file', selectedFile);
    await axios.post('/api/upload/', formData);
    fetchDocuments();
  };

  const handleSearch = async () => {
    const response = await axios.get(`/api/search/?query=${searchQuery}`);
    setDocuments(response.data);
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">Readwise Light</h1>

      <div className="mb-4">
        <input type="file" onChange={handleFileChange} />
        <button onClick={handleUpload} className="bg-blue-500 text-white px-4 py-2 rounded">Upload</button>
      </div>

      <div className="mb-4">
        <input
          type="text"
          placeholder="Search..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="border p-2"
        />
        <button onClick={handleSearch} className="bg-gray-500 text-white px-4 py-2 rounded">Search</button>
      </div>

      <div>
        {documents.map((doc) => (
          <div key={doc.id} className="border p-4 mb-4">
            <h2 className="text-xl font-bold">{doc.filename}</h2>
            <p className="text-gray-600">{doc.summary}</p>
            <div className="mt-2">
              {doc.keywords && JSON.parse(doc.keywords).map((keyword) => (
                <span key={keyword} className="bg-gray-200 text-gray-700 px-2 py-1 rounded-full text-sm mr-2">{keyword}</span>
              ))}
            </div>
            <div className="mt-2">
              <a href={`/api/download/${doc.id}`} className="text-blue-500">Download</a>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;