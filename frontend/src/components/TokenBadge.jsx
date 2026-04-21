// src/components/TokenBadge.jsx
//
// Simple, clean token badge for TRX / USD₮ / SCT.
// Uses official brand colors and the SVG/PNG logos placed under
// frontend/public/assets/.
//
// Usage:
//   <TokenBadge type="TRX"  amount="0.01"  />
//   <TokenBadge type="USDT" amount="15.00" />
//   <TokenBadge type="SCT"  amount="1000"  />

export default function TokenBadge({ type, amount }) {
  const config = {
    TRX: {
      label: "TRX",
      icon: "/assets/trx-logo.svg",
    },
    USDT: {
      label: "USD\u20AE",        // USD₮  (Tether's stylised mark)
      icon: "/assets/usdt-logo.png",
    },
    SCT: {
      label: "SCT",
      icon: "/assets/sct-logo.png",
    },
  };

  const token = config[type];
  if (!token) return null;

  return (
    <div
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: "8px",
        padding: "8px 12px",
        border: "1px solid #ddd",
        borderRadius: "10px",
        background: "#fff",
        fontFamily: "Inter, system-ui, sans-serif",
      }}
    >
      <img
        src={token.icon}
        alt={`${token.label} logo`}
        style={{ width: "22px", height: "22px", objectFit: "contain" }}
      />
      <span style={{ fontWeight: 600 }}>{token.label}</span>
      {amount !== undefined && <span>{amount}</span>}
    </div>
  );
}
