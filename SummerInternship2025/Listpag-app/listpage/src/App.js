// import logo from './logo.svg';
// import './App.css';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import ListPage from "./pages/list";
import EditPage from "./pages/editpage";
function App() {
  return (
    // <div className="App">
    //  <ListPage/>
    // </div>
    <BrowserRouter>
    <Routes>
      <Route path="/" element={<ListPage/>}/>
      <Route path="/editpage" element={<EditPage/>}/>
    </Routes>
    </BrowserRouter>
  );
}

export default App;
