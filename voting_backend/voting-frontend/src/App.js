import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./Login";
import Verify from "./Verify";
import Ballot from "./Ballot";
import Results from "./Results";
import VoterActivity from "./VoterActivity";


function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
	<Route path="/login" element={<Login />} />
        <Route path="/verify/:token" element={<Verify />} />
        <Route path="/ballot" element={<Ballot />} />
	<Route path="/results/:ballot_id" element={<Results />} />
	<Route path="/admin/voter-activity" element={<VoterActivity />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
