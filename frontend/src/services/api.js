const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

async function apiRequest(path, options = {}) {
  const response = await fetch(`${API_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  const contentType = response.headers.get("content-type") || "";
  const data = contentType.includes("application/json")
    ? await response.json()
    : await response.text();

  if (!response.ok) {
    throw new Error(
      typeof data === "string" ? data : data?.message || "Request failed"
    );
  }

  return data;
}

export const api = {
  root: () => apiRequest("/"),
  fakeSimulation: () => apiRequest("/simulation/fake"),
  realSimulation: () => apiRequest("/simulation/real"),
  compareSimulation: () => apiRequest("/simulation/compare"),
  walletInfo: () => apiRequest("/simulation/wallet"),
  sendDemo: (to_address, amount_sun = 1000000) =>
    apiRequest(
      `/simulation/send-demo?to_address=${encodeURIComponent(
        to_address
      )}&amount_sun=${amount_sun}`,
      {
        method: "POST",
      }
    ),
};