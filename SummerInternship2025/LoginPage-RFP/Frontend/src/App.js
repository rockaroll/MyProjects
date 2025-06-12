// import logo from './logo.svg';
import './App.css';
import Formtemp from './pages/login';
import FPassword from './pages/ForgetPassword';
import { BrowserRouter,Routes, Route } from "react-router-dom";
import ChangePassword from './pages/ChangePassword';
function App() {
  return (
    <BrowserRouter>
    <Routes>
    <Route path='/' element={<Formtemp/>}/>
    <Route path='/ForgetPassword' element={<FPassword/>}/>  
    <Route path='/ChangePassword' element={<ChangePassword/>}/> 
    </Routes>
    </BrowserRouter>
  );
}

export default App;
