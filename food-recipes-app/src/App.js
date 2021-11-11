import './styles/App.css';
import Tabs from './components/Tabs';
import Detail from './components/Detail';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

function App() {
  return (
    <Router>
      <div className='App'>
        <div className='h1'>Food Recipes</div>
          <div className='tabs-container'>
            <Routes>
              <Route path='/' exact element={<Tabs/>}/>
              <Route path='/:table/:id' element={<Detail/>}/>
            </Routes>
          </div>
      </div>
    </Router>
  );
}

export default App;
