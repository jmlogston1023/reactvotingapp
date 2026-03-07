import { useEffect, useState } from "react";
import axios from "axios";

function VoterActivity(){

  const [voters,setVoters] = useState([]);

  useEffect(()=>{

    axios.get("http://127.0.0.1:8000/api/admin/voter-activity/")
      .then(res => setVoters(res.data))

  },[])

  return(

    <div style={{width:"600px",margin:"auto"}}>

      <h2>Voting Activity</h2>

      <table border="1" width="100%">
        <thead>
          <tr>
            <th>Email</th>
            <th>Ballot</th>
            <th>Voted At</th>
          </tr>
        </thead>

        <tbody>

          {voters.map((v,i)=>(
            <tr key={i}>
              <td>{v.email}</td>
              <td>{v.ballot}</td>
              <td>{v.voted_at}</td>
            </tr>
          ))}

        </tbody>

      </table>

    </div>

  )

}

export default VoterActivity
