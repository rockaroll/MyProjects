// forgotpassword.js page
import '../styles/Fp.css'
import Button from '@mui/material/Button';
import { Box,TextField,FormControl} from '@mui/material';
import { Link ,useNavigate} from "react-router-dom";
import { useState } from 'react';
function FPassword(){
    const [Email2,setEmail2]= useState('')
    const history= useNavigate();
    const histdata = () =>{
        history('/ChangePassword',{state:Email2})
    } 
    return (
            <Box className="Page-Details">
            <h2 id='heading'>Reset your Password</h2>  
            <p id='textexp'>Enter your email  and we will send you instructions to reset <br/> your password</p>
            <br></br>
            <FormControl id='Form-Details'>
            <TextField className='input' id='Email' value={Email2} onChange={(e) => setEmail2(e.target.value)}  label='Enter Email' required></TextField>
            <br></br>
            <Button id='Send' onClick={histdata} variant="contained" color="primary">Sending Reset instructions</Button>
            </FormControl>
            <Link id='fp1' to='/' ><h5 id='return'>Return to Login</h5></Link>
           </Box>
    )
}

export default FPassword;