import React, { useEffect, useState } from "react";
import { api } from "../api";
import "./HistoryPage.css"; // make sure the CSS file exists

export default function HistoryPage({ setPage, setSelectedId }) {
  const [items, setItems] = useState([]);

  const load = async () => {
    try {
      const res = await api.get("/history/");
      setItems(res.data);
    } catch (err) {
      console.error(err);
      alert("Failed to load history");
    }
  };

  useEffect(() => { load(); }, []);

  return (
    <div className="history-container">
      <h2>Last 5 Uploaded Datasets</h2>
      {items.length === 0 ? (
        <p>No datasets uploaded yet.</p>
      ) : (
        items.map((d) => (
          <div key={d.id} className="history-item">
            <div>
              <b>{d.original_filename}</b>
              <span className="row-count">({d.row_count} rows)</span>
            </div>
            <button 
              className="view-btn"
              onClick={() => { setSelectedId(d.id); setPage("detail"); }}
            >
              View Details
            </button>
          </div>
        ))
      )}
    </div>
  );
}
