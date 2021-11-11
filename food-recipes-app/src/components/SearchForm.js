import { useRef, useState, useEffect } from 'react';
import FetchData from '../FetchData';
import '../styles/SearchForm.css';

/**
 * Search form with select of logic operators and inputs for name, yields, prepTime, cookTime, mealTypes.
 * @returns Search form react component
 */
const SearchForm = (props) => {
  const [hasAllRecipeLoaded, setHasAllRecipeLoaded] = useState(false);
  const [hasFavRecipeLoaded, setHasFavRecipeLoaded] = useState(false);

  const logicOp1 = useRef();
  const name1 = useRef();
  const yields1 = useRef();
  const prepTime1 = useRef();
  const cookTime1 = useRef();
  const mealTypes1 = useRef();

  const logicOp2 = useRef();
  const name2 = useRef();
  const yields2 = useRef();
  const prepTime2 = useRef();
  const cookTime2 = useRef();
  const mealTypes2 = useRef();
  
  // function for search in all recipes table
  const searchAll = async () => {
    const logicOperator = logicOp1.current.value;
    let queryStr = '';
    queryStr += name1.current.value ? (!queryStr ? 'all.name:' + name1.current.value : logicOperator + 'all.name:' + name1.current.value) : '';
    queryStr += yields1.current.value ? (!queryStr ? 'all.yields:' + yields1.current.value : logicOperator + 'all.yields:' + yields1.current.value) : '';
    queryStr += prepTime1.current.value ? (!queryStr ? 'all.prep time:' + prepTime1.current.value : logicOperator + 'all.prep time:' + prepTime1.current.value) : '';
    queryStr += cookTime1.current.value ? (!queryStr ? 'all.cook time:' + cookTime1.current.value : logicOperator + 'all.cook time:' + cookTime1.current.value) : '';
    queryStr += mealTypes1.current.value ? (!queryStr ? 'all.meal types:' + mealTypes1.current.value : logicOperator + 'all.meal types:' + mealTypes1.current.value) : '';
    queryStr = queryStr ? queryStr : 'all.name:';
    console.log(queryStr);

    const dataAll = await FetchData('search?q=' + queryStr, 'GET');
    if (!Object.prototype.hasOwnProperty.call(dataAll, 'GET error')) {
      props.setAllRecipes(dataAll);
    } else {
      props.setAllRecipes([{id: '-1', name: 'GET error: ' + dataAll['GET error']}]);
    }
    props.setState(prevState => ({allRecipeList: [],
                                  favRecipeList: [...prevState.favRecipeList]}));
    props.setCountAll(0);
    props.setCountAll(0);
    setHasAllRecipeLoaded(true);
  }

  // function for search in favourite recipes table
  const searchFav = async () => {
    const logicOperator = logicOp2.current.value;
    let queryStr = '';
    queryStr += name2.current.value ? (!queryStr ? 'fav.name:' + name2.current.value : logicOperator + 'fav.name:' + name2.current.value) : '';
    queryStr += yields2.current.value ? (!queryStr ? 'fav.yields:' + yields2.current.value : logicOperator + 'fav.yields:' + yields2.current.value) : '';
    queryStr += prepTime2.current.value ? (!queryStr ? 'fav.prep time:' + prepTime2.current.value : logicOperator + 'fav.prep time:' + prepTime2.current.value) : '';
    queryStr += cookTime2.current.value ? (!queryStr ? 'fav.cook time:' + cookTime2.current.value : logicOperator + 'fav.cook time:' + cookTime2.current.value) : '';
    queryStr += mealTypes2.current.value ? (!queryStr ? 'fav.meal types:' + mealTypes2.current.value : logicOperator + 'fav.meal types:' + mealTypes2.current.value) : '';
    queryStr = queryStr ? queryStr : 'fav.name:';
    console.log(queryStr);

    const dataFav = await FetchData('search?q=' + queryStr, 'GET');
    if (!Object.prototype.hasOwnProperty.call(dataFav, 'GET error')) {
      props.setFavRecipes(dataFav);
    } else {
      props.setFavRecipes([{id: '-2', name: 'GET error: no match recipes'}]);
    }
    props.setState(prevState => ({allRecipeList: [...prevState.allRecipeList],
                                  favRecipeList: []}));
    props.setCountFav(0);
    props.setCountFav(0);
    setHasFavRecipeLoaded(true);
  }

  // add 10 list recipes from all recipes table to state.allRecipeList to display after data is loaded
  useEffect(() => {
    if (hasAllRecipeLoaded) {
      if (props.allRecipes && props.countAll === 0) {
        for (let i = props.countAll; i < props.countAll + 10 && i < props.allRecipes.length; i += 1) {
          props.setState(prevState => ({allRecipeList: [...prevState.allRecipeList, props.allRecipes[i]],
            favRecipeList: [...prevState.favRecipeList]}));
        }
        props.setCountAll(props.countAll + 10);
      }
    }
    setHasAllRecipeLoaded(false);
  }, [hasAllRecipeLoaded, props]);

  // add 10 list recipes from favourite recipes table to state.favRecipeList to display after data is loaded
  useEffect(() => {
    if (hasFavRecipeLoaded) {
      if (props.favRecipes && props.countFav === 0) {
        for (let i = props.countFav; i < props.countFav + 10 && i < props.favRecipes.length; i += 1) {
          props.setState(prevState => ({allRecipeList: [...prevState.allRecipeList],
            favRecipeList: [...prevState.favRecipeList, props.favRecipes[i]]}));
        }
        props.setCountFav(props.countFav + 10);
      }
    }
    setHasFavRecipeLoaded(false);
  }, [hasFavRecipeLoaded, props]);


  // html content to display the form for search
  if (props.tab === 1) {
    // search form for all recipes
    return (
      <div className='form-container'>
        All Recipes&nbsp;&nbsp;
        <select name='select-search-option' id='select-all' ref={logicOp1}>
          <option value='AND'>Match All</option>
          <option value='OR'>Match Any</option>
        </select>
        <form className='form-search'>
          <label className='label-search'>Name: </label>
          <input className='input-search' type='text' id='name1' name='name' ref={name1}/>
          <label className='label-search'>Yield: </label>
          <input className='input-search' type='text' id='yields1' name='yields' ref={yields1}/>
          <label className='label-search'>Prep Time: </label>
          <input className='input-search' type='text' id='prep-time1' name='prep time' ref={prepTime1}/>
          <label className='label-search'>Cook Time: </label>
          <input className='input-search' type='text' id='cook-time1' name='cook time' ref={cookTime1}/>
          <label className='label-search'>Meal Types: </label>
          <input className='input-search' type='text' id='meal-types1' name='meal types' ref={mealTypes1}/>
          <button className='button-search' onClick={(e) => {
            e.preventDefault();
            searchAll();
          }}>Search</button>
        </form>
      </div>
    )
  }

  // search form for favourite recipes
  return (
    <div className='form-container'>
      Favourite Recipes&nbsp;&nbsp;
      <select name='select-search-option' id='select-fav' ref={logicOp2}>
        <option value='AND'>Match All</option>
        <option value='OR'>Match Any</option>
      </select>
      <form className='form-search'>
        <label className='label-search'>Name: </label>
        <input className='input-search' type='text' id='name2' name='name' ref={name2}/>
        <label className='label-search'>Yield: </label>
        <input className='input-search' type='text' id='yields2' name='yields' ref={yields2}/>
        <label className='label-search'>Prep Time: </label>
        <input className='input-search' type='text' id='prep-time2' name='prep time' ref={prepTime2}/>
        <label className='label-search'>Cook Time: </label>
        <input className='input-search' type='text' id='cook-time2' name='cook time' ref={cookTime2}/>
        <label className='label-search'>Meal Types: </label>
        <input className='input-search' type='text' id='meal-types2' name='meal types' ref={mealTypes2}/>
        <button className='button-search' onClick={(e) => {
          e.preventDefault();
          searchFav();
        }}>Search</button>
      </form>
    </div>
  )
}

export default SearchForm;