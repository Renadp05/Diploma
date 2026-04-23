import React from "react";

function TokenCard({
  name = "Tether",
  symbol = "USDT",
  decimals = 6,
  network = "mainnet",
  contractAddress = "PASTE_CONTRACT_ADDRESS_HERE",
  logoURI = "/assets/usdt-logo.png",
  website = "https://diploma-1-eb6y.onrender.com",
}) {
  return (
    <div
      style={{
        border: "1px solid #ddd",
        borderRadius: "16px",
        padding: "20px",
        maxWidth: "460px",
        margin: "20px auto",
        background: "#fff",
        boxShadow: "0 6px 20px rgba(0,0,0,0.08)",
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: "16px" }}>
        <img
          src={logoURI}
          alt={`${symbol} logo`}
          style={{
            width: "72px",
            height: "72px",
            objectFit: "contain",
            borderRadius: "12px",
            background: "#f8f8f8",
            padding: "8px",
          }}
        />

        <div>
          <h2 style={{ margin: 0 }}>{name}</h2>
          <p style={{ margin: "6px 0", color: "#666" }}>
            <strong>Symbol:</strong> {symbol}
          </p>
          <p style={{ margin: "6px 0", color: "#666" }}>
            <strong>Decimals:</strong> {decimals}
          </p>
        </div>
      </div>

      <div style={{ marginTop: "18px", lineHeight: "1.7" }}>
        <p>
          <strong>Network:</strong> {network}
        </p>
        <p style={{ wordBreak: "break-all" }}>
          <strong>Contract:</strong> {contractAddress}
        </p>
        <p style={{ wordBreak: "break-all" }}>
          <strong>Website:</strong>{" "}
          <a href={website} target="_blank" rel="noreferrer">
            {website}
          </a>
        </p>
      </div>
    </div>
  );
}

export default TokenCard;