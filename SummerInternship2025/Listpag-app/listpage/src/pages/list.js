import Navbar from "../components/Navbar";
import SearchAppBar from "../components/Searchbar";
import Tablefunc from "../components/Table";
import Divider from "@mui/material/Divider";
function ListPage(){
    return(<div id="Page">
        <Navbar/>
        <Divider sx={{ bgcolor: 'background.paper'}} />
        <SearchAppBar />
        <Divider sx={{ bgcolor: 'background.paper'}} />
        <br></br><br></br><br></br>
        <Tablefunc/>
    </div>)
}

export default ListPage;