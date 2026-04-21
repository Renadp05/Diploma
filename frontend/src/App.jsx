import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import VerifyTransaction from "./pages/VerifyTransaction";
import Logs from "./pages/Logs";
import DemoSimulation from "./pages/DemoSimulation";

function App() {
  const logout = () => {
    localStorage.removeItem("token");
    window.location.href = "/login";
  };

  return (
    <BrowserRouter>
      <div style={{ padding: "20px" }}>
        <h1>SecureChain Platform</h1>

        <nav style={{ marginBottom: "20px" }}>
          <Link to="/login">Login</Link> |{" "}
          <Link to="/">Dashboard</Link> |{" "}
          <Link to="/verify">Verify</Link> |{" "}
          <Link to="/logs">Logs</Link> |{" "}
          <Link to="/simulation">Simulation</Link> |{" "}
          <button onClick={logout}>Logout</button>
        </nav>

        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<Dashboard />} />
          <Route path="/verify" element={<VerifyTransaction />} />
          <Route path="/logs" element={<Logs />} />
          <Route path="/simulation" element={<DemoSimulation />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;