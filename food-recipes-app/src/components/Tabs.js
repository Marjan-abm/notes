import { useState } from 'react';
import '../styles/Tabs.css';
import List from './List';
import SearchForm from './SearchForm';
import UpdateForm from './UpdateForm';
import Chart from './Chart';

/**
 * Four tabs which are recipes, favourites, Update, Visualization.
 * @returns Tabs react component with List, SearchForm, UpdateForm, Chart as its children components
 */
const Tabs = () => {
  // number indicating the current tab to show
  const [toggleState, setToggleState] = useState(1);
  // list of all recipes dict and favourite recipe dict to display
  const [state, setState] = useState({allRecipeList: [], favRecipeList: []});
  // list of all recipes from the search results
  const [allRecipes, setAllRecipes] = useState(null);
  // list of favourite recipes from the search results
  const [favRecipes, setFavRecipes] = useState(null);
  // size of all recipes list to display
  const [countAll, setCountAll] = useState(0);
  // size of favourite recipes list to display
  const [countFav, setCountFav] = useState(0);

  const toggleTab = (index) => {
    setToggleState(index);
  };

  return (
    <div className='container'>
      {/* title for the tabs */}
      <div className='title-tabs'>
        <button
          className={toggleState === 1 ? 'tabs active-tabs' : 'tabs'}
          onClick={() => toggleTab(1)}
        >
          Recipes
        </button>
        <button
          className={toggleState === 2 ? 'tabs active-tabs' : 'tabs'}
          onClick={() => toggleTab(2)}
        >
          Favourites
        </button>
        <button
          className={toggleState === 3 ? 'tabs active-tabs' : 'tabs'}
          onClick={() => toggleTab(3)}
        >
          Update
        </button>
        <button
          className={toggleState === 4 ? 'tabs active-tabs' : 'tabs'}
          onClick={() => toggleTab(4)}
        >
          Visualization
        </button>
      </div>

      {/* content for the tabs */}
      <div className='content-tabs'>
        {/* all recipes tab */}
        <div
          className={toggleState === 1 ? 'content  active-content' : 'content'}
        >
          {/* component for search */}
          <SearchForm tab={1} allRecipes={allRecipes} favRecipes={favRecipes} countAll={countAll} countFav={countFav}
          setState={setState} setAllRecipes={setAllRecipes} setFavRecipes={setFavRecipes} setCountAll={setCountAll} setCountFav={setCountFav}/>
          
          <hr />

          {/* component for display list of recipes */}
          <List tab={1} state={state} allRecipes={allRecipes} favRecipes={favRecipes} countAll={countAll} countFav={countFav} 
          setState={setState} setAllRecipes={setAllRecipes} setFavRecipes={setFavRecipes} setCountAll={setCountAll} setCountFav={setCountFav}/>
        </div>

        {/* favourite recipes tab */}
        <div
          className={toggleState === 2 ? 'content  active-content' : 'content'}
        >
          {/* component for search */}
          <SearchForm tab={2} allRecipes={allRecipes} favRecipes={favRecipes} countAll={countAll} countFav={countFav}
          setState={setState} setAllRecipes={setAllRecipes} setFavRecipes={setFavRecipes} setCountAll={setCountAll} setCountFav={setCountFav}/>
          
          <hr />

          {/* component for display list of recipes */}
          <List tab={2} state={state} allRecipes={allRecipes} favRecipes={favRecipes} countAll={countAll} countFav={countFav}
           setState={setState} setAllRecipes={setAllRecipes} setFavRecipes={setFavRecipes} setCountAll={setCountAll} setCountFav={setCountFav}/>
        </div>

        {/* update form tab */}
        <div
          className={toggleState === 3 ? 'content  active-content' : 'content'}
        >
          <h3>Update Recipe</h3>
          <hr />
          <UpdateForm/>
        </div>

        {/* bar chart tab */}
        <div
          className={toggleState === 4 ? 'content  active-content' : 'content'}
        >
          <h3>Chart</h3>
          <hr />
          <Chart/>
        </div>
      </div>

    </div>
  )
}
export default Tabs;
