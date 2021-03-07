import './App.css';
import {
  BrowserRouter as Router,
  Switch,
  Route
} from "react-router-dom";
import Home from './comp/Home';
import NotFound from './comp/NotFound';
import Login from './comp/Login';
import Certificate from './comp/Certificate';



const App = props => {

  return (
    <Router>
      <Switch>
        
        <Route exact path="/" component={Home} />
        <Route exact path="/cert/:id" component={Certificate}/>
        <Route exact path="/login" component={Login}  />
        <Route component={NotFound} />
        
      </Switch>
    </Router>
  );
}

export default App;
