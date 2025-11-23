import React, { useEffect, useState } from "react";
import { api } from "../api";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import "./DetailPage.css"; // create this CSS file for styling

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const BASE_URL = "http://127.0.0.1:8000/api";
const TOKEN = "6a5788d528d4768b63df56c2911f500879bedab7";

export default function DetailPage({ selectedId, setPage }) {
  const [dataset, setDataset] = useState(null);

  const loadDataset = async () => {
    try {
      const res = await api.get(`/datasets/${selectedId}/`);
      setDataset(res.data);
    } catch (err) {
      console.error(err);
      alert("Failed to load dataset details");
    }
  };

  useEffect(() => {
    if (selectedId) loadDataset();
  }, [selectedId]);

  const downloadPDF = async () => {
    try {
      const res = await fetch(`${BASE_URL}/download_pdf/${selectedId}/`, {
        method: "GET",
        headers: {
          Authorization: `Token ${localStorage.getItem("token") || TOKEN}`,
        },
      });

      if (!res.ok) throw new Error("Failed to fetch PDF");

      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", `report_${selectedId}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      console.error(err);
      alert("Failed to download PDF: " + err.message);
    }
  };

  if (!dataset) return <p>Loading...</p>;

  const summary = dataset.summary || {};
  const averages = summary.averages || {};
  const typeDist = summary.type_distribution || {};

  const typeChartData = {
    labels: Object.keys(typeDist),
    datasets: [
      {
        label: "Count by Type",
        data: Object.values(typeDist),
        backgroundColor: "rgba(54, 162, 235, 0.6)",
      },
    ],
  };

  return (
    <div className="detail-container">
      <button className="back-btn" onClick={() => setPage("history")}>← Back</button>

      <div className="detail-card">
        <h2>{dataset.original_filename}</h2>
        <p>Total Rows: <b>{dataset.row_count}</b></p>

        <section className="averages-section">
          <h3>Averages</h3>
          {Object.keys(averages).length ? (
            <ul>
              {Object.entries(averages).map(([k, v]) => (
                <li key={k}>
                  {k}: {v !== null ? v.toFixed(2) : "N/A"}
                </li>
              ))}
            </ul>
          ) : <p>No numeric columns found.</p>}
        </section>

        <section className="chart-section">
          {Object.keys(typeDist).length ? (
            <>
              <h3>Type Distribution</h3>
              <Bar data={typeChartData} />
            </>
          ) : <p>No type data found.</p>}
        </section>

        <button className="download-btn" onClick={downloadPDF}>
          Download PDF Report
        </button>
      </div>
    </div>
  );
}
