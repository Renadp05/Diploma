import { useEffect, useState } from "react";
import { getDashboardData } from "../services/dashboardService";

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const result = await getDashboardData();
        setData(result);
      } catch (error) {
        console.error("Dashboard error:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboard();
  }, []);

  if (loading) return <p>Loading dashboard...</p>;
  if (!data) return <p>No dashboard data available.</p>;

  return (
    <div>
      <h2>Fraud Detection Dashboard</h2>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(4, 1fr)",
          gap: "16px",
          marginTop: "20px",
          marginBottom: "24px",
        }}
      >
        <div style={cardStyle}>
          <h3>Total</h3>
          <p style={numberStyle}>{data.total}</p>
        </div>

        <div style={cardStyle}>
          <h3>Verified</h3>
          <p style={{ ...numberStyle, color: "green" }}>{data.verified}</p>
        </div>

        <div style={cardStyle}>
          <h3>Suspicious</h3>
          <p style={{ ...numberStyle, color: "orange" }}>{data.suspicious}</p>
        </div>

        <div style={cardStyle}>
          <h3>High Risk</h3>
          <p style={{ ...numberStyle, color: "red" }}>{data.high_risk}</p>
        </div>
      </div>

      <div style={cardStyle}>
        <h3>Latest Transactions</h3>

        {data.latest_transactions?.length === 0 ? (
          <p>No recent transactions.</p>
        ) : (
          <table style={{ width: "100%", borderCollapse: "collapse", marginTop: "16px" }}>
            <thead>
              <tr>
                <th style={thStyle}>User ID</th>
                <th style={thStyle}>Action</th>
                <th style={thStyle}>Timestamp</th>
                <th style={thStyle}>Risk Score</th>
                <th style={thStyle}>Risk Category</th>
              </tr>
            </thead>
            <tbody>
              {data.latest_transactions?.map((item, index) => (
                <tr key={index}>
                  <td style={tdStyle}>{item.user_id}</td>
                  <td style={tdStyle}>{item.action}</td>
                  <td style={tdStyle}>{item.timestamp}</td>
                  <td style={tdStyle}>{item.risk_score}</td>
                  <td style={tdStyle}>{item.risk_category}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

const cardStyle = {
  backgroundColor: "#f9fafb",
  border: "1px solid #ddd",
  borderRadius: "12px",
  padding: "20px",
};

const numberStyle = {
  fontSize: "28px",
  fontWeight: "bold",
  margin: 0,
};

const thStyle = {
  border: "1px solid #ddd",
  padding: "12px",
  backgroundColor: "#111827",
  color: "white",
  textAlign: "left",
};

const tdStyle = {
  border: "1px solid #ddd",
  padding: "12px",
};