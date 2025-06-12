// changepassword.js page
import '../styles/ChangePasscode.css'
import Button from '@mui/material/Button';
import { Box,TextField,FormControl} from '@mui/material';
import { useLocation,useNavigate } from 'react-router-dom';
import { useState } from 'react';
function ChangePassword(){
   const location= useLocation()
   const autofillvalue=location.state
   const [Email1,setEmail1]=useState('')
   const [Password3,setPassword3]=useState('')
   const [rPassword3,setrPassword3]=useState('')
   const [message,setMessage]=useState('')
   const history= useNavigate();
   const Reset1 = async() =>{
       fetch("http://127.0.0.1:8081/reset",
        {
            method:"POST",
            headers:{
                'Content-Type':'application/json'
            },
            body: JSON.stringify({Email1,Password3,rPassword3})
        })
        .then(response=>response.json())
        .then(data=>setMessage(data.message))
        .catch((error)=>console.error(error))
         
        setTimeout(() => {
            history("/");
    }, 1000*2);

}
    return(<Box className="Page-Details"> 
                <h2 id='Heading'>Change Password</h2>
            <FormControl id='Form Details'>
                {/* <label className='Txtlab'>Username</label> */}
                <TextField className='input' id='Email' value={Email1} onClick={(e)=>setEmail1(autofillvalue)} label='Enter Email' required></TextField>
                <br></br><br></br>
                <TextField className='input' id='Passwordt' value={Password3} onChange={(e)=>setPassword3(e.target.value)}   type='Password' label='Type Password' required></TextField>
                <br></br><br></br>
                {/* <label className='Txtlab'>Password</label> */}
                <TextField className='input' id='Passwordr' value={rPassword3} onChange={(e)=>setrPassword3(e.target.value)}  type='Password' label='Retype Password' required></TextField>
                <Button id='Change' onClick={Reset1}  variant="contained" color="primary">Change Password</Button>
                <h5 id='message'>{message}</h5>
            </FormControl>
            </Box>)
}
export default ChangePassword;