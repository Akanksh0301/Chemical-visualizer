import React, { useState } from "react";
import UploadPage from "./components/UploadPage";
import HistoryPage from "./components/HistoryPage";
import DetailPage from "./components/DetailPage";
import Navbar from "./components/Navbar";
import "./App.css";

function App() {
  const [page, setPage] = useState("upload");
  const [selectedId, setSelectedId] = useState(null);

  return (
    <div>
      <Navbar setPage={setPage} />

      <div className="container">
        {page === "upload" && <UploadPage setPage={setPage} />}
        {page === "history" && (
          <HistoryPage setPage={setPage} setSelectedId={setSelectedId} />
        )}
        {page === "detail" && (
          <DetailPage selectedId={selectedId} setPage={setPage} />
        )}
      </div>
    </div>
  );
}

export default App;
