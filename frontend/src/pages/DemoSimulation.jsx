import { useEffect, useState } from "react";
import { getCompareSimulation } from "../services/simulationService";

export default function DemoSimulation() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSimulation = async () => {
      try {
        const result = await getCompareSimulation();
        setData(result);
      } catch (error) {
        console.error("Simulation error:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchSimulation();
  }, []);

  if (loading) return <p>Loading simulation...</p>;
  if (!data) return <p>No simulation data available.</p>;

  return (
    <div>
      <h2>Comparative Simulation</h2>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: "20px",
          marginTop: "20px",
        }}
      >
        <div style={cardStyle}>
          <h3>Valid Scenario</h3>
          <pre style={preStyle}>{JSON.stringify(data.real, null, 2)}</pre>
        </div>

        <div style={cardStyle}>
          <h3>High-Risk Scenario</h3>
          <pre style={preStyle}>{JSON.stringify(data.fake, null, 2)}</pre>
        </div>
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

const preStyle = {
  whiteSpace: "pre-wrap",
  wordBreak: "break-word",
  margin: 0,
};