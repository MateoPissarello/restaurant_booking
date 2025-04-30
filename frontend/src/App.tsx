import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import AdminMenu from "./pages/AdminMenu";
import BookingManagement from "./pages/BookingManagement";
import CreateRestaurantPage from "./pages/CreateRestaurantPage";
import LoginAdmin from "./pages/LoginAdmin";
import LoginClient from "./pages/LoginClient";
import MainMenu from "./pages/MainMenu";
import MakeReservation from "./pages/MakeReservation";
import MyBookings from "./pages/MyBookings";
import MyProfile from "./pages/MyProfile";
import RestaurantManagementPage from "./pages/RestaurantManagementPage";
import UserManagementPage from "./pages/UserManagementPage";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login-client" element={<LoginClient />} />
        <Route path="/menu-client" element={<MainMenu />} />
        <Route path="/make-reservation" element={<MakeReservation />} />
        <Route path="/my-reservations" element={<MyBookings />} />
        <Route path="/my-profile" element={<MyProfile />} />
        <Route path="/login-admin" element={<LoginAdmin />} />
        <Route path="/admin-menu" element={<AdminMenu />} />
        <Route path="/admin/bookings" element={<BookingManagement />} />
        <Route
          path="/admin/create-restaurant"
          element={<CreateRestaurantPage />}
        />
        <Route path="/admin/users" element={<UserManagementPage />} />
        <Route
          path="/admin/restaurants"
          element={<RestaurantManagementPage />}
        />

        {/* Aquí irán después las otras rutas */}
        {/* <Route path="/my-reservations" element={<MyReservations />} /> */}
        {/* <Route path="/my-profile" element={<MyProfile />} /> */}
        {/* Aquí irán después las otras rutas */}
      </Routes>
    </Router>
  );
}

export default App;
