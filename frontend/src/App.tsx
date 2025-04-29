import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import LoginClient from "./pages/LoginClient";
import MainMenu from "./pages/MainMenu";
import MakeReservation from "./pages/MakeReservation";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login-client" element={<LoginClient />} />
        <Route path="/menu-client" element={<MainMenu />} />
        <Route path="/make-reservation" element={<MakeReservation />} />
        {/* Aquí irán después las otras rutas */}
        {/* <Route path="/my-reservations" element={<MyReservations />} /> */}
        {/* <Route path="/my-profile" element={<MyProfile />} /> */}
        {/* Aquí irán después las otras rutas */}
      </Routes>
    </Router>
  );
}

export default App;
