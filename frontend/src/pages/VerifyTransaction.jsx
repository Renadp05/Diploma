
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getRiskAnalysis } from "../services/transactionService";

export default function VerifyTransaction() {
  const [txId, setTxId] = useState("");
  const [walletAddress, setWalletAddress] = useState("TMx9B8xLz36g41CR9X6C7dd5PBxKFYDUfS");
  const [result, setResult] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      navigate("/login");
    }
  }, [navigate]);

  const handleVerify = async () => {
    try {
      const data = await getRiskAnalysis(txId, walletAddress);
      setResult(data);
    } catch (err) {
      console.error(err);
      alert("Request failed");
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Verify Transaction</h2>
      <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
  <img src={logo} style={{ width: "30px", borderRadius: "50%" }} />
  <span>TRC-20 Token (USDT)</span>
</div>

      <input
        type="text"
        placeholder="Enter TX Hash"
        value={txId}
        onChange={(e) => setTxId(e.target.value)}
        style={{ display: "block", marginBottom: "10px", padding: "10px", width: "320px" }}
      />

      <input
        type="text"
        placeholder="Enter Wallet Address"
        value={walletAddress}
        onChange={(e) => setWalletAddress(e.target.value)}
        style={{ display: "block", marginBottom: "10px", padding: "10px", width: "320px" }}
      />

      <button onClick={handleVerify}>Verify</button>

      {result && (
        <pre style={{ marginTop: "20px", whiteSpace: "pre-wrap" }}>
          {JSON.stringify(result, null, 2)}
        </pre>
      )}
    </div>
  );
}