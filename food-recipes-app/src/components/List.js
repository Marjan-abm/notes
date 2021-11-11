import { useEffect, useState } from 'react';
import FetchData from '../FetchData';
import '../styles/List.css'
import { Link } from 'react-router-dom';

/**
 * List of recipes with image and name displayed in tab 1 and tab 2.
 * @returns List react component
 */
const List = (props) => {
  const [hasLoadedAll, setHasLoadedAll] = useState(false);
  const [hasLoadedFav, setHasLoadedFav] = useState(false);
  // number of recipes to append when click button more
  const NUMBER_ITEM_APPEND = 10;
  // image showed with get error
  const ERROR_IMAGE_URL = 'https://i3.wp.com/simpleandseasonal.com/wp-content/uploads/2018/02/Crockpot-Express-E6-Error-Code.png'

  // fetch data
  useEffect(() => {
    if (props.tab === 1 && !hasLoadedAll) {
    async function getData() {
      const dataAll = await FetchData('search?q=all.name:', 'GET');
      if (!Object.prototype.hasOwnProperty.call(dataAll, 'GET error')) {
        props.setAllRecipes(dataAll);

        for (let i = props.countAll; i < props.countAll + NUMBER_ITEM_APPEND && i < dataAll.length; i += 1) {
          props.setState(prevState => ({allRecipeList: [...prevState.allRecipeList, dataAll[i]],
            favRecipeList: [...prevState.favRecipeList]}));
        }
        props.setCountAll(props.countAll + NUMBER_ITEM_APPEND);
      }
    }
    getData();
    setHasLoadedAll(true);
  }
  }, [hasLoadedAll, setHasLoadedAll, props]);

  useEffect(() => {
    if (props.tab === 2 && !hasLoadedFav) {
      async function getData() {
        const dataFav = await FetchData('search?q=fav.name:', 'GET');
        if (!Object.prototype.hasOwnProperty.call(dataFav, 'GET error')) {
          props.setFavRecipes(dataFav);

          for (let i = props.countFav; i < props.countFav + NUMBER_ITEM_APPEND && i < dataFav.length; i += 1) {
          props.setState(prevState => ({allRecipeList: [...prevState.allRecipeList],
            favRecipeList: [...prevState.favRecipeList, dataFav[i]]}));
          }
          props.setCountFav(props.countFav + NUMBER_ITEM_APPEND);
        }
      }
      getData();
      setHasLoadedFav(true);
    }
  }, [hasLoadedFav, setHasLoadedFav, props]);

  /**
   * append more list of recipes from all recipes table to display
   */
  const appendAllData = () => {
    if (!props.allRecipes) return;
    for (let i = props.countAll; i < props.countAll + NUMBER_ITEM_APPEND && i < props.allRecipes.length; i += 1) {
      props.setState(prevState => ({allRecipeList: [...prevState.allRecipeList, props.allRecipes[i]],
        favRecipeList: [...prevState.favRecipeList]}));
    }
    props.setCountAll(props.countAll + NUMBER_ITEM_APPEND);
  }

  /**
   * append more list of recipes from favourite recipes table to display
   */
  const appendFavData = () => {
    if (!props.favRecipes) return;
    for (let i = props.countFav; i < props.countFav + NUMBER_ITEM_APPEND && i < props.favRecipes.length; i += 1) {
      props.setState(prevState => ({allRecipeList: [...prevState.allRecipeList],
      favRecipeList: [...prevState.favRecipeList, props.favRecipes[i]]}));
    }
    props.setCountFav(props.countFav + NUMBER_ITEM_APPEND);
  }

  // html content to display list of recipes or error message
  if (props.tab === 1) {
    if (!props.allRecipes || !props.state.allRecipeList) {
      // no data in all recipes table
      return (
        <div>
          <div className='list-item'>
            No data found
          </div>
          <button className='button-more' onClick={appendAllData}>More</button>
        </div>
      )
    }
    // list of recipes
    return (
      <div>
        {props.state.allRecipeList.map(recipe => {
          if (recipe.id < 0) {
            // error message
            return (
              <div className='list-item' key={recipe.id}>
              <img className='food-image' src={ERROR_IMAGE_URL} alt='' />
                {recipe.name}
              </div>
            )
          }
          // item of a recipe
          return (
            <div className='list-item' key={recipe.id}>
              <img className='food-image' src={recipe['image url']} alt='' />
              <Link className='link-recipe' to={`/food/${recipe.id}`} target='_blank' rel='noopener noreferrer'>{recipe.name}</Link>
            </div>
          )
        })}
        <button className='button-more' onClick={appendAllData}>More</button>
      </div>
    )
  }

  // content to display favourite recipes
  if (!props.favRecipes || !props.state.favRecipeList) {
    // no data in favourite recipes table
    return (
      <div>
        <div className='list-item'>
          No data found
        </div>
        <button className='button-more' onClick={appendFavData}>More</button>
      </div>
    )
  }
  // list of recipes
  return (
    <div>
      {props.state.favRecipeList.map(recipe => {
        if (recipe.id < 0) {
          // error message
          return (
            <div className='list-item' key={recipe.id}>
              <img className='food-image' src={ERROR_IMAGE_URL} alt='' />
                {recipe.name}
              </div>
          )
        }
        // item of a recipe
        return (
          <div className='list-item' key={recipe.id}>
            <img className='food-image' src={recipe['image url']} alt='' />
            <Link className='link-recipe' to={`/favourite/${recipe.id}`} target='_blank' rel='noopener noreferrer'>{recipe.name}</Link>
          </div>
        )
      })}
      <button className='button-more' onClick={appendFavData}>More</button>
    </div>
  )
}

export default List;