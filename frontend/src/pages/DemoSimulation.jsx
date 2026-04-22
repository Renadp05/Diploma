import React, { useState } from "react";
import API from "../services/api";

function DemoSimulation() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [toAddress, setToAddress] = useState("");
  const [amountSun, setAmountSun] = useState(1000000);
  const [error, setError] = useState("");

  const runAction = async (action) => {
    try {
      setLoading(true);
      setError("");
      const data = await action();
      setResult(data);
    } catch (err) {
      setError(err.message);
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Demo Simulation</h2>

      <div
        style={{
          display: "flex",
          gap: "10px",
          flexWrap: "wrap",
          marginBottom: "20px",
        }}
      >
        <button onClick={() => runAction(API.fakeSimulation)}>Fake</button>
        <button onClick={() => runAction(API.realSimulation)}>Real</button>
        <button onClick={() => runAction(API.compareSimulation)}>Compare</button>
        <button onClick={() => runAction(API.walletInfo)}>Wallet</button>
        <button onClick={() => runAction(() => API.sendDemo(toAddress, amountSun))}>
          Send Demo
        </button>
      </div>

      <div style={{ marginBottom: "20px" }}>
        <h3>Send Demo TRX</h3>
        <input
          type="text"
          placeholder="TRON address"
          value={toAddress}
          onChange={(e) => setToAddress(e.target.value)}
          style={{ width: "320px", marginRight: "10px" }}
        />
        <input
          type="number"
          value={amountSun}
          onChange={(e) => setAmountSun(Number(e.target.value))}
          style={{ width: "120px", marginRight: "10px" }}
        />
        <button
          onClick={() => runAction(() => API.sendDemo(toAddress, amountSun))}
        >
          Send Demo
        </button>
      </div>

      {loading && <p>Loading...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {result && (
        <pre
          style={{
            background: "#111",
            color: "#0f0",
            padding: "16px",
            borderRadius: "8px",
            overflowX: "auto",
          }}
        >
          {JSON.stringify(result, null, 2)}
        </pre>
      )}
    </div>
  );
}

export default DemoSimulation;