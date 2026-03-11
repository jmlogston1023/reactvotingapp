import axios from "axios";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

function Login() {

  const [email, setEmail] = useState("");
  const [code, setCode] = useState("");
  const [step, setStep] = useState(1);

  const navigate = useNavigate();

  const requestCode = async () => {
    try {
      await axios.post(
        "/api/auth/request-code/",
        { email }
      );

      alert("Code sent to your email");
      setStep(2);

    } catch (err) {
      alert("Email not registered");
    }
  };

  const verifyCode = async () => {
    try {
      const res = await axios.post(
        "/api/auth/verify-code/",
        { email, code }
      );

      localStorage.setItem("user_id", res.data.user_id);
      navigate("/ballot");

    } catch (err) {
      alert("Invalid or expired code");
    }
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        background: "linear-gradient(135deg,#1e3c72,#2a5298)",
        fontFamily: "Arial"
      }}
    >
      <div
        style={{
          background: "white",
          padding: "35px",
          borderRadius: "10px",
          width: "350px",
          textAlign: "center",
          boxShadow: "0 10px 25px rgba(0,0,0,0.2)"
        }}
      >

        {/* Voting Icon */}
        <img
          src="https://cdn-icons-png.flaticon.com/512/3135/3135768.png"
          alt="Voting Icon"
          style={{
            width: "70px",
            marginBottom: "10px"
          }}
        />

        <h2 style={{color:"#1e3c72"}}>Briarwood Oaks Estates Online Voting</h2>

        {step === 1 && (
          <>
            <input
              type="email"
              placeholder="Enter your email"
              value={email}
              onChange={(e)=>setEmail(e.target.value)}
              style={{
                width:"100%",
                padding:"10px",
                marginTop:"15px",
                borderRadius:"5px",
                border:"1px solid #ccc"
              }}
            />

            <button
              onClick={requestCode}
              style={{
                width:"100%",
                marginTop:"15px",
                padding:"10px",
                background:"#2a5298",
                color:"white",
                border:"none",
                borderRadius:"5px",
                fontWeight:"bold",
                cursor:"pointer"
              }}
            >
              Send Login Code
            </button>
          </>
        )}

        {step === 2 && (
          <>
            <input
              type="text"
              placeholder="Enter email code"
              value={code}
              onChange={(e)=>setCode(e.target.value)}
              style={{
                width:"100%",
                padding:"10px",
                marginTop:"15px",
                borderRadius:"5px",
                border:"1px solid #ccc"
              }}
            />

            <button
              onClick={verifyCode}
              style={{
                width:"100%",
                marginTop:"15px",
                padding:"10px",
                background:"#2a5298",
                color:"white",
                border:"none",
                borderRadius:"5px",
                fontWeight:"bold",
                cursor:"pointer"
              }}
            >
              Login
            </button>
          </>
        )}

      </div>
    </div>
  );
}

export default Login;
