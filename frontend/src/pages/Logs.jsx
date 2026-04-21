import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getLogs } from "../services/logService";

export default function Logs() {
  const [data, setData] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      navigate("/login");
      return;
    }

    const fetchLogs = async () => {
      try {
        const res = await getLogs();
        setData(res);
      } catch (err) {
        console.error(err);
        alert("Could not load logs");
      }
    };

    fetchLogs();
  }, [navigate]);

  return (
    <div style={{ padding: "20px" }}>
      <h2>Logs</h2>
      <pre style={{ whiteSpace: "pre-wrap" }}>
        {JSON.stringify(data, null, 2)}
      </pre>
    </div>
  );
}