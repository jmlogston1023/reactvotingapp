import axios from "axios";
import { useParams, useNavigate } from "react-router-dom";
import { useEffect } from "react";

function Verify() {
  const { token } = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    async function verify() {
      const res = await axios.post("http://localhost:8000/api/auth/verify/", { token });
      localStorage.setItem("user_id", res.data.user_id);
      navigate("/ballot");
    }
    verify();
  }, []);

  return <div>Verifying...</div>;
}

export default Verify;
